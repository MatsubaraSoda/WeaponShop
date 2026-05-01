import { useWeapons } from "@/hooks/useWeapons"

export function App() {
  const { data, isLoading, error } = useWeapons()

  if (isLoading) {
    return <p>Loading</p>
  }

  if (error) {
    return <p>Error: {error.message}</p>
  }

  return (
    <div className="p-4">
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

export default App
