import { useState, useEffect } from 'react'
import SiteForm from './components/SiteForm'
import SiteCard from './components/SiteCard'

interface WebSite {
  id: number
  name: string
  url: string
  is_active: boolean
  last_status?: number
  latency?: number
}

interface ApiError {
  message: string
  status?: number
}

export default function App() {
  const [sites, setSites] = useState<WebSite[]>([])
  const [error, setError] = useState<ApiError | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const API_URL = 'http://localhost:8000/api/v1/sites/'

  const handleApiError = async (response: Response): Promise<ApiError> => {
    try {
      const errorData = await response.json()
      return {
        message: errorData.detail || 'Error desconocido',
        status: response.status
      }
    } catch {
      return {
        message: response.statusText || 'Error de conexión',
        status: response.status
      }
    }
  }

  useEffect(() => {
    const fetchSites = async () => {
      try {
        const response = await fetch(API_URL)
        
        if (!response.ok) {
          const apiError = await handleApiError(response)
          setError(apiError)
          return
        }
        
        const data = await response.json()
        setSites(data.sort((a: WebSite, b: WebSite) => b.id - a.id))
        setError(null) 
      } catch (err) {
        setError({
          message: 'No se pudo conectar con el servidor',
          status: undefined
        })
      }
    }
    
    fetchSites()
    const interval = setInterval(fetchSites, 10000) // Actualizar cada 10 segundos
    
    return () => clearInterval(interval)
  }, [])

  const handleAddSite = async (name: string, url: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, url, check_interval: 60 })
      })

      if (response.ok) {
        const newSite = await response.json()
        setSites([newSite, ...sites])
        
        const reloadResponse = await fetch(API_URL)
        if (reloadResponse.ok) {
          const data = await reloadResponse.json()
          setSites(data.sort((a: WebSite, b: WebSite) => b.id - a.id))
        }
      } else {
        const apiError = await handleApiError(response)
        console.log('Error en handleAddSite:', apiError)
        setError(apiError)
      }
    } catch (err) {
      console.log('Error de conexión en handleAddSite:', err)
      setError({
        message: 'Error de conexión al registrar el sitio',
        status: undefined
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    setError(null)
    
    try {
      const response = await fetch(`${API_URL}${id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        setSites(sites.filter(site => site.id !== id))
      } else if (response.status === 404) {
        setError({
          message: 'El sitio que intentas eliminar no existe',
          status: 404
        })
      } else {
        const apiError = await handleApiError(response)
        setError(apiError)
      }
    } catch (err) {
      setError({
        message: 'Error de conexión al eliminar el sitio',
        status: undefined
      })
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 p-6 text-zinc-100 sm:p-12">
      <div className="mx-auto max-w-5xl">

        <header className="mb-10 flex flex-col gap-2 border-b border-zinc-900 pb-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-teal-400 sm:text-4xl">
              WebTracker Control Panel
            </h1>
            <p className="mt-1 text-sm text-zinc-400">
              Monitoreo asíncrono distribuido con Celery, Redis y Prometheus en tiempo real.
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-xl bg-zinc-900 px-4 py-2.5 border border-zinc-800 self-start sm:self-auto">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-semibold text-zinc-300">API Motor Online</span>
          </div>
        </header>

        <main>
          {error && (
            <div className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 p-4">
              <div className="flex items-center gap-3">
                <div className="h-2 w-2 rounded-full bg-rose-500" />
                <div className="flex-1">
                  <p className="font-semibold text-rose-400">
                    {error.status === 400 ? 'Error de validación' : 
                     error.status === 404 ? 'Recurso no encontrado' : 
                     error.status === 500 ? 'Error del servidor' : 'Error'}
                  </p>
                  <p className="text-sm text-rose-300">{error.message}</p>
                </div>
                <button 
                  onClick={() => setError(null)}
                  className="text-rose-400 hover:text-rose-300"
                >
                  ✕
                </button>
              </div>
            </div>
          )}
          
          {error && (
            <div className="mb-2 p-2 bg-yellow-500/10 border border-yellow-500/30 rounded text-xs text-yellow-300">
              DEBUG: Error state - {JSON.stringify(error)}
            </div>
          )}

          <SiteForm onAddSite={handleAddSite} isLoading={isLoading} />

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {sites.map((site) => (
              <SiteCard
                key={site.id}
                id={site.id}
                name={site.name}
                url={site.url}
                is_active={site.is_active}
                last_status={site.last_status}
                latency={site.latency}
                onDelete={handleDelete}
              />
            ))}
          </div>

          {sites.length === 0 && (
            <div className="mt-12 text-center text-zinc-600">
              <p className="text-lg">No hay canales de monitoreo registrados.</p>
              <p className="text-sm mt-1">Usa el formulario superior para lanzar tu primer ping HTTP.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
