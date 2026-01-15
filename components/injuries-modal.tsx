'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { AlertTriangle } from 'lucide-react'

interface Injury {
  team: string
  player: string
  position: string
  status: string
  impact?: 'high' | 'medium' | 'low'
}

interface InjuriesModalProps {
  injuries: Injury[]
}

export function InjuriesModal({ injuries = [] }: InjuriesModalProps) {
  const [open, setOpen] = useState(false)

  const highImpact = injuries.filter(i => i.impact === 'high')
  const mediumImpact = injuries.filter(i => i.impact === 'medium')
  const lowImpact = injuries.filter(i => i.impact === 'low')

  return (
    <>
      <Button 
        onClick={() => setOpen(true)}
        variant="outline"
        className="w-full justify-start text-blue-600 border-blue-200 hover:bg-blue-50 hover:text-blue-700"
      >
        View injuries →
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle size={24} className="text-rose-600" />
              Playoff Injury Report
            </DialogTitle>
            <DialogDescription>
              High-impact injuries that may affect team performance
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 mt-4">
            {/* High Impact */}
            {highImpact.length > 0 && (
              <div>
                <h3 className="font-semibold text-rose-900 text-sm mb-3 flex items-center gap-2">
                  <span className="inline-block w-2 h-2 bg-rose-600 rounded-full"></span>
                  High Impact ({highImpact.length})
                </h3>
                <div className="space-y-2">
                  {highImpact.map((injury, idx) => (
                    <div key={idx} className="bg-rose-50 border border-rose-200 p-3 rounded-lg">
                      <p className="font-semibold text-slate-900">{injury.player}</p>
                      <p className="text-sm text-slate-600">
                        <strong>{injury.team}</strong> • {injury.position} • <span className="text-rose-600 font-medium">{injury.status}</span>
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Medium Impact */}
            {mediumImpact.length > 0 && (
              <div>
                <h3 className="font-semibold text-amber-900 text-sm mb-3 flex items-center gap-2">
                  <span className="inline-block w-2 h-2 bg-amber-600 rounded-full"></span>
                  Medium Impact ({mediumImpact.length})
                </h3>
                <div className="space-y-2">
                  {mediumImpact.map((injury, idx) => (
                    <div key={idx} className="bg-amber-50 border border-amber-200 p-3 rounded-lg">
                      <p className="font-semibold text-slate-900">{injury.player}</p>
                      <p className="text-sm text-slate-600">
                        <strong>{injury.team}</strong> • {injury.position} • <span className="text-amber-600 font-medium">{injury.status}</span>
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Low Impact */}
            {lowImpact.length > 0 && (
              <div>
                <h3 className="font-semibold text-blue-900 text-sm mb-3 flex items-center gap-2">
                  <span className="inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
                  Low Impact ({lowImpact.length})
                </h3>
                <div className="space-y-2">
                  {lowImpact.map((injury, idx) => (
                    <div key={idx} className="bg-blue-50 border border-blue-200 p-3 rounded-lg">
                      <p className="font-semibold text-slate-900">{injury.player}</p>
                      <p className="text-sm text-slate-600">
                        <strong>{injury.team}</strong> • {injury.position} • <span className="text-blue-600 font-medium">{injury.status}</span>
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {injuries.length === 0 && (
              <div className="text-center py-8">
                <p className="text-slate-600 mb-2">No major injuries currently reported for playoff teams</p>
                <p className="text-xs text-slate-500">All teams appear healthy. Retired/inactive players excluded.</p>
              </div>
            )}

            <div className="bg-blue-50 p-3 rounded-lg border border-blue-200 text-xs text-slate-600">
              <p className="mb-1"><strong>Status Types:</strong> <strong>Out</strong> (will not play) • <strong>Doubtful</strong> (unlikely to play) • <strong>Questionable</strong> (game-time decision) • <strong>IR</strong> (season-ending)</p>
              <p><strong>Data Source:</strong> Auto-updated from ESPN with retired/inactive players filtered. For real-time updates, visit <a href="https://www.espn.com/nfl/injuries" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline hover:text-blue-800">ESPN.com/nfl/injuries</a></p>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}