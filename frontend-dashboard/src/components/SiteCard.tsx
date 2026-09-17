import { Shield, ShieldAlert, Timer, X } from 'lucide-react'

interface SiteProps {
  id: number
  name: string
  url: string
  is_active: boolean  
  last_status?: number
  latency?: number
  onDelete?: (id: number) => void
}

export default function SiteCard({ name, 
  url, 
  is_active, 
  last_status, 
  latency, 
  id, 
  onDelete }: SiteProps) {
  
  const isOnline = last_status === 200
  const hasData = last_status !== null && last_status !== undefined

  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5 shadow-lg transition-all hover:border-zinc-700">
      <div className="flex items-center justify-between">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-bold text-zinc-100 truncate">{name}</h3>
          <p className="text-sm text-zinc-400 truncate">{url}</p>
        </div>
        
        <div className="flex items-center gap-3 flex-shrink-0">
          <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
            isOnline ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
          }`}>
            <span className={`h-1.5 w-1.5 rounded-full ${isOnline ? 'bg-emerald-400' : 'bg-rose-400'}`} />
            {hasData ? (isOnline ? 'Operational' : 'Down') : 'Pendiente'}
          </span>
          
          <button
            onClick={() => onDelete?.(id)}
            className="text-zinc-500 hover:text-rose-400 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 border-t border-zinc-800 pt-4 text-sm text-zinc-400">
        <div className="flex items-center gap-2">
          <Timer className="h-4 w-4 text-teal-400" />
          <span>{latency !== null && latency !== undefined ? `${latency.toFixed(2)} ms` : '--'}</span>
        </div>
        <div className="flex items-center gap-2">
          {url.startsWith('https') ? (
            <Shield className="h-4 w-4 text-emerald-400" />
          ) : (
            <ShieldAlert className="h-4 w-4 text-amber-400" />
          )}
          <span>{url.startsWith('https') ? 'SSL Secure' : 'No SSL'}</span>
        </div>
      </div>
    </div>
  )
}
