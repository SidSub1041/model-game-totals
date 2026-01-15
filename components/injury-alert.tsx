'use client'

import { AlertCircle, AlertTriangle, Info } from 'lucide-react'
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
  // Show info alert when no injuries detected
  if (highImpactInjuries.length === 0) {
    return (
      <Alert className="border-l-4 border-l-blue-500 bg-blue-50 mb-6 border-blue-200">
        <Info className="h-4 w-4 text-blue-700" />
        <AlertTitle className="text-blue-900 font-semibold">No Major Injuries Detected</AlertTitle>
        <AlertDescription className="text-blue-800 mt-2">
          <p className="text-sm mb-2">
            All playoff teams appear to have no significant injury concerns at this time.
          </p>
          <p className="text-xs text-blue-700">
            Injury data auto-updated. Status types: <strong>Out</strong> (will not play), <strong>Doubtful</strong> (unlikely), <strong>Questionable</strong> (game-time decision), <strong>IR</strong> (season-ending). Retired/inactive players excluded. For real-time updates, check{' '}
            <a 
              href="https://www.espn.com/nfl/injuries" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="underline hover:text-blue-900 font-medium"
            >
              ESPN.com/nfl/injuries
            </a>
          </p>
        </AlertDescription>
      </Alert>
    )
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
                {injury.team} • {injury.position} • <strong>{injury.status}</strong>
              </p>
            </div>
          ))}
        </div>
        <p className="text-xs text-rose-700 mt-3">
          Status types: <strong>Out</strong> (will not play), <strong>Doubtful</strong> (unlikely), <strong>Questionable</strong> (game-time decision), <strong>IR</strong> (season-ending). For real-time updates, check{' '}
          <a 
            href="https://www.espn.com/nfl/injuries" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="underline hover:text-rose-900"
          >
            ESPN.com/nfl/injuries
          </a>
        </p>
      </AlertDescription>
    </Alert>
  )
}
