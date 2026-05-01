CREATE TABLE weapons (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    world_shell TEXT NOT NULL,
    title TEXT NOT NULL,
    short_description TEXT,
    price_value INTEGER NOT NULL,
    currency_type TEXT NOT NULL,
    features JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE weapons ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access" ON weapons FOR SELECT USING (true);