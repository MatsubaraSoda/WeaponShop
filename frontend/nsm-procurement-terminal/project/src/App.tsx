import { WeaponCard } from "@/components/WeaponCard"
import { useWeapons } from "@/hooks/useWeapons"

export function App() {
  const { data, isLoading, error } = useWeapons()

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black font-mono text-cyan-400/90">
        <p className="animate-pulse tracking-[0.35em]">终端同步中 ···</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-2 bg-black px-6 text-center font-mono text-red-400">
        <p className="text-sm uppercase tracking-widest text-red-500/80">
          链路异常
        </p>
        <p>{error.message}</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(34,211,238,0.12),transparent)]" />

      <main className="relative mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <header className="mb-10 flex flex-col gap-2 border-b border-zinc-800/80 pb-8">
          <p className="font-mono text-xs uppercase tracking-[0.45em] text-cyan-500/70">
            DHS // WEAPON TERMINAL
          </p>
          <h1 className="bg-linear-to-r from-cyan-200 via-white to-fuchsia-300 bg-clip-text text-3xl font-bold tracking-tight text-transparent drop-shadow-[0_0_24px_rgba(34,211,238,0.35)] sm:text-4xl">
            DHS 武器库终端
          </h1>
          <p className="max-w-xl text-sm text-zinc-500">
            废土市场实时报价 · 神经链路已加密
          </p>
        </header>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {data?.map((weapon) => (
            <WeaponCard key={weapon.id} weapon={weapon} />
          ))}
        </div>
      </main>
    </div>
  )
}

export default App
