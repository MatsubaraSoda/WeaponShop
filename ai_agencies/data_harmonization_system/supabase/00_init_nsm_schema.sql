-- =============================================================================
-- NSM / DHS Supabase 初始化脚本（对齐 docs/schema/all.dbml）
-- 说明：
-- 1) 本脚本仅负责 schema 初始化，不包含业务数据写入。
-- 2) 依赖 Supabase 内置 auth.users（本脚本不创建 auth.users）。
-- 3) 建议以 service_role 或数据库 owner 执行。
-- =============================================================================

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- -----------------------------------------------------------------------------
-- 通用更新时间触发器
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- -----------------------------------------------------------------------------
-- public.wallets
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.wallets (
  id uuid PRIMARY KEY REFERENCES auth.users(id),
  balance_qc bigint NOT NULL DEFAULT 0 CHECK (balance_qc >= 0),
  status varchar(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'FROZEN')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

DROP TRIGGER IF EXISTS trg_wallets_set_updated_at ON public.wallets;
CREATE TRIGGER trg_wallets_set_updated_at
BEFORE UPDATE ON public.wallets
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.universes
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.universes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code varchar(64) NOT NULL UNIQUE,
  name varchar(255) NOT NULL,
  description text,
  cover_image_url text,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

DROP TRIGGER IF EXISTS trg_universes_set_updated_at ON public.universes;
CREATE TRIGGER trg_universes_set_updated_at
BEFORE UPDATE ON public.universes
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.weapons
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.weapons (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sku_code varchar(64) NOT NULL UNIQUE,
  native_universe_id uuid NOT NULL REFERENCES public.universes(id),
  list_price_qc bigint NOT NULL CHECK (list_price_qc >= 0),
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_weapons_native_universe
  ON public.weapons (native_universe_id);
CREATE INDEX IF NOT EXISTS idx_weapons_catalog_filter
  ON public.weapons (is_active, native_universe_id);

DROP TRIGGER IF EXISTS trg_weapons_set_updated_at ON public.weapons;
CREATE TRIGGER trg_weapons_set_updated_at
BEFORE UPDATE ON public.weapons
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.weapon_armament_spec
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.weapon_armament_spec (
  weapon_id uuid PRIMARY KEY REFERENCES public.weapons(id) ON DELETE CASCADE,
  armament_name varchar(255) NOT NULL,
  description text NOT NULL,
  physical_dimensions text NOT NULL,
  construction_feedstock text NOT NULL,
  usage_dependency text NOT NULL,
  operation_principle text NOT NULL,
  extended_spec jsonb,
  defects_and_risks text,
  design_constraints text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

DROP TRIGGER IF EXISTS trg_weapon_armament_spec_set_updated_at ON public.weapon_armament_spec;
CREATE TRIGGER trg_weapon_armament_spec_set_updated_at
BEFORE UPDATE ON public.weapon_armament_spec
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.weapon_merchandising
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.weapon_merchandising (
  weapon_id uuid PRIMARY KEY REFERENCES public.weapons(id) ON DELETE CASCADE,
  product_title varchar(255),
  short_description varchar(512),
  key_features jsonb,
  promo_copy text,
  suggested_price_qc bigint CHECK (suggested_price_qc >= 0),
  updated_at timestamptz NOT NULL DEFAULT now()
);

DROP TRIGGER IF EXISTS trg_weapon_merchandising_set_updated_at ON public.weapon_merchandising;
CREATE TRIGGER trg_weapon_merchandising_set_updated_at
BEFORE UPDATE ON public.weapon_merchandising
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.wormhole_protocols
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.wormhole_protocols (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  wallet_id uuid NOT NULL REFERENCES public.wallets(id),
  protocol_name varchar(255) NOT NULL,
  target_universe_id uuid NOT NULL REFERENCES public.universes(id),
  coord_x double precision NOT NULL DEFAULT 0,
  coord_y double precision NOT NULL DEFAULT 0,
  coord_z double precision NOT NULL DEFAULT 0,
  total_cost_qc bigint NOT NULL DEFAULT 0 CHECK (total_cost_qc >= 0),
  status varchar(20) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'PENDING', 'COMPLETED')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_wormhole_protocols_wallet_protocol_name UNIQUE (wallet_id, protocol_name)
);

DROP TRIGGER IF EXISTS trg_wormhole_protocols_set_updated_at ON public.wormhole_protocols;
CREATE TRIGGER trg_wormhole_protocols_set_updated_at
BEFORE UPDATE ON public.wormhole_protocols
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.wormhole_items
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.wormhole_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  wormhole_protocol_id uuid NOT NULL REFERENCES public.wormhole_protocols(id) ON DELETE CASCADE,
  weapon_id uuid NOT NULL REFERENCES public.weapons(id),
  price_snapshot_qc bigint CHECK (price_snapshot_qc IS NULL OR price_snapshot_qc >= 0),
  quantity int NOT NULL DEFAULT 1 CHECK (quantity > 0),
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_wormhole_items_protocol_weapon UNIQUE (wormhole_protocol_id, weapon_id)
);

CREATE INDEX IF NOT EXISTS idx_wormhole_items_protocol
  ON public.wormhole_items (wormhole_protocol_id);
CREATE INDEX IF NOT EXISTS idx_wormhole_items_weapon
  ON public.wormhole_items (weapon_id);

-- -----------------------------------------------------------------------------
-- public.black_hole_protocols
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.black_hole_protocols (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  wallet_id uuid NOT NULL REFERENCES public.wallets(id),
  protocol_name varchar(255) NOT NULL,
  target_universe_id uuid NOT NULL REFERENCES public.universes(id),
  coord_x double precision NOT NULL DEFAULT 0,
  coord_y double precision NOT NULL DEFAULT 0,
  coord_z double precision NOT NULL DEFAULT 0,
  credited_amount_qc bigint,
  status varchar(20) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'PENDING', 'COMPLETED')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_black_hole_protocols_wallet_protocol_name UNIQUE (wallet_id, protocol_name),
  CONSTRAINT ck_black_hole_credited_amount
    CHECK (
      (status = 'COMPLETED' AND credited_amount_qc IS NOT NULL AND credited_amount_qc >= 0)
      OR
      (status IN ('DRAFT', 'PENDING') AND credited_amount_qc IS NULL)
    )
);

DROP TRIGGER IF EXISTS trg_black_hole_protocols_set_updated_at ON public.black_hole_protocols;
CREATE TRIGGER trg_black_hole_protocols_set_updated_at
BEFORE UPDATE ON public.black_hole_protocols
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- -----------------------------------------------------------------------------
-- public.wallet_transactions
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.wallet_transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  wallet_id uuid NOT NULL REFERENCES public.wallets(id),
  type varchar(32) NOT NULL CHECK (type IN ('BLACK_HOLE_INTAKE', 'WORMHOLE_CONSUME')),
  amount_qc bigint NOT NULL,
  related_black_hole_protocol_id uuid REFERENCES public.black_hole_protocols(id),
  related_wormhole_protocol_id uuid REFERENCES public.wormhole_protocols(id),
  audit_log text,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_wallet_transactions_link_and_sign
    CHECK (
      (
        type = 'BLACK_HOLE_INTAKE'
        AND amount_qc > 0
        AND related_black_hole_protocol_id IS NOT NULL
        AND related_wormhole_protocol_id IS NULL
      )
      OR
      (
        type = 'WORMHOLE_CONSUME'
        AND amount_qc < 0
        AND related_wormhole_protocol_id IS NOT NULL
        AND related_black_hole_protocol_id IS NULL
      )
    )
);

CREATE INDEX IF NOT EXISTS idx_wallet_transactions_wallet_id
  ON public.wallet_transactions (wallet_id);
CREATE INDEX IF NOT EXISTS idx_wallet_transactions_related_black_hole_protocol_id
  ON public.wallet_transactions (related_black_hole_protocol_id);
CREATE INDEX IF NOT EXISTS idx_wallet_transactions_related_wormhole_protocol_id
  ON public.wallet_transactions (related_wormhole_protocol_id);

COMMIT;

