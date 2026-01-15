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
    <Alert className="border-l-4 border-l-red-500 bg-red-50 mb-6">
      <AlertTriangle className="h-4 w-4 text-red-600" />
      <AlertTitle className="text-red-900 font-bold">⚠️ Key Injuries to Monitor</AlertTitle>
      <AlertDescription className="text-red-800 mt-2">
        <p className="mb-3 text-sm">
          The following high-impact injuries may significantly affect team performance:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {highImpactInjuries.map((injury, idx) => (
            <div key={idx} className="bg-white/50 p-2 rounded border border-red-200">
              <p className="font-semibold text-sm">{injury.player}</p>
              <p className="text-xs text-gray-700">
                {injury.team} • {injury.position} • {injury.status}
              </p>
            </div>
          ))}
        </div>
        <p className="text-xs text-red-700 mt-3 italic">
          Consider these injuries when interpreting model predictions. Check ESPN.com/nfl/injuries for real-time updates.
        </p>
      </AlertDescription>
    </Alert>
  )
}
