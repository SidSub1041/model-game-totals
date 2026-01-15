'use client'

import { AlertCircle, AlertTriangle } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

interface Injury {
  team: string
  player: string
  position: string
  status: string
}

interface InjuryAlertProps {
  highImpactInjuries?: Injury[]
}

export function InjuryAlert({ highImpactInjuries = [] }: InjuryAlertProps) {
  if (highImpactInjuries.length === 0) {
    return null
  }

  return (
    <Alert className="border-l-4 border-l-rose-600 bg-rose-50 mb-6 border-rose-200">
      <AlertTriangle className="h-4 w-4 text-rose-700" />
      <AlertTitle className="text-rose-900 font-semibold">Key Injuries to Monitor</AlertTitle>
      <AlertDescription className="text-rose-800 mt-2">
        <p className="mb-3 text-sm">
          High-impact injuries detected for playoff games:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {highImpactInjuries.map((injury, idx) => (
            <div key={idx} className="bg-white p-2 rounded border border-rose-200">
              <p className="font-semibold text-sm text-slate-900">{injury.player}</p>
              <p className="text-xs text-slate-600">
                {injury.team} • {injury.position} • {injury.status}
              </p>
            </div>
          ))}
        </div>
        <p className="text-xs text-rose-700 mt-3">
          For real-time updates, check <a href="https://www.espn.com/nfl/injuries" target="_blank" rel="noopener noreferrer" className="underline hover:text-rose-900">ESPN.com/nfl/injuries</a>
        </p>
      </AlertDescription>
    </Alert>
  )
}
