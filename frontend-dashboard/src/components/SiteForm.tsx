import { useState } from 'react'
import type { FormEvent } from 'react'
import { PlusCircle } from 'lucide-react'

interface SiteFormProps {
  onAddSite: (name: string, url: string) => void
  isLoading?: boolean
}

export default function SiteForm({ onAddSite, isLoading = false }: SiteFormProps) {
  const [name, setName] = useState('')
  const [url, setUrl] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    
    if (!name.trim() || !url.trim()) return

    onAddSite(name, url)

    setName('')
    setUrl('')
  }

  return (
    <form onSubmit={handleSubmit} className="mb-8 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 shadow-lg">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-zinc-400">
            Nombre del Sitio
          </label>
          <input
            type="text"
            placeholder="Ej: Servidor Principal"
            value={name}

            onChange={(e) => setName(e.target.value)}
            className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 p-3 text-zinc-100 placeholder-zinc-600 outline-none transition-colors focus:border-teal-500"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-zinc-400">
            Dirección URL
          </label>
          <input
            type="text"
            placeholder="Ej: https://mi-app.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 p-3 text-zinc-100 placeholder-zinc-600 outline-none transition-colors focus:border-teal-500"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-teal-500 p-3 font-semibold text-zinc-950 transition-colors hover:bg-teal-400 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <>
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-950 border-t-transparent" />
            Procesando...
          </>
        ) : (
          <>
            <PlusCircle className="h-5 w-5" />
            Añadir Sitio al Monitor
          </>
        )}
      </button>
    </form>
  )
}
