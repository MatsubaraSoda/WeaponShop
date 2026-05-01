import { useCallback, useEffect, useState } from "react"

import { supabase } from "@/lib/supabase"

/** Aligns with `weapons` table (see supabase migration). JSONB `features` is parsed by PostgREST. */
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Weapon {
  id: string
  world_shell: string
  title: string
  short_description: string | null
  price_value: number
  currency_type: string
  features: Json
  created_at: string
}

async function fetchWeaponsRows(): Promise<{
  data: Weapon[] | null
  error: Error | null
}> {
  const { data: rows, error: queryError } = await supabase
    .from("weapons")
    .select("*")

  if (queryError) {
    return { data: null, error: new Error(queryError.message) }
  }

  return { data: (rows ?? []) as Weapon[], error: null }
}

export function useWeapons() {
  const [data, setData] = useState<Weapon[] | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const refetch = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    const { data: next, error: nextError } = await fetchWeaponsRows()
    if (nextError) {
      setData(null)
      setError(nextError)
    } else {
      setData(next)
    }
    setIsLoading(false)
  }, [])

  useEffect(() => {
    let active = true

    queueMicrotask(() => {
      if (!active) return
      void refetch()
    })

    return () => {
      active = false
    }
  }, [refetch])

  return { data, isLoading, error, refetch }
}
