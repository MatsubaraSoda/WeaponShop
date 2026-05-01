import { Badge } from "@/components/ui/badge"
import type { Weapon } from "@/hooks/useWeapons"

function featureLabels(features: Weapon["features"]): string[] {
  if (!Array.isArray(features)) return []
  return features.flatMap((item) => {
    if (typeof item === "string") return [item]
    if (typeof item === "number" || typeof item === "boolean") {
      return [String(item)]
    }
    if (item === null || item === undefined) return []
    return [JSON.stringify(item)]
  })
}

export interface WeaponCardProps {
  weapon: Weapon
}

export function WeaponCard({ weapon }: WeaponCardProps) {
  const labels = featureLabels(weapon.features)

  return (
    <article
      className={[
        "group relative flex min-h-70 flex-col gap-4 rounded-xl border border-zinc-800",
        "bg-linear-to-b from-zinc-950 to-black p-5 shadow-lg transition-all duration-300",
        "hover:border-cyan-400/60 hover:shadow-[0_0_28px_rgba(34,211,238,0.35)]",
        "hover:ring-2 hover:ring-cyan-400/40",
      ].join(" ")}
    >
      <header className="flex flex-col gap-2">
        <span className="inline-flex w-fit rounded-md border border-zinc-700/80 bg-zinc-900/80 px-2 py-0.5 font-mono text-[10px] uppercase tracking-[0.2em] text-zinc-500">
          {weapon.world_shell}
        </span>
        <h2
          className={[
            "font-semibold tracking-tight text-white",
            "drop-shadow-[0_0_12px_rgba(255,255,255,0.18)]",
          ].join(" ")}
        >
          {weapon.title}
        </h2>
      </header>

      <div className="font-mono text-lg font-semibold tabular-nums text-amber-300 drop-shadow-[0_0_10px_rgba(251,191,36,0.35)]">
        {weapon.price_value.toLocaleString()} {weapon.currency_type}
      </div>

      {weapon.short_description ? (
        <p className="flex-1 text-sm leading-relaxed text-zinc-400">
          {weapon.short_description}
        </p>
      ) : (
        <p className="flex-1 text-sm italic text-zinc-600">暂无描述</p>
      )}

      {labels.length > 0 ? (
        <div className="flex flex-wrap gap-2 border-t border-zinc-800/80 pt-4">
          {labels.map((text, i) => (
            <Badge
              key={`${weapon.id}-feat-${i}`}
              variant="outline"
              className="border-emerald-500/45 bg-emerald-950/70 font-mono text-[11px] font-medium text-emerald-300 shadow-[inset_0_1px_0_rgba(52,211,153,0.12)]"
            >
              {text}
            </Badge>
          ))}
        </div>
      ) : null}
    </article>
  )
}
