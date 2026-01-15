'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { BookOpen } from 'lucide-react'

export function ModelExplanationModal() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Button 
        onClick={() => setOpen(true)}
        variant="outline"
        className="w-full justify-start text-blue-600 border-blue-200 hover:bg-blue-50 hover:text-blue-700"
      >
        Learn more →
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <BookOpen size={24} className="text-blue-600" />
              How the Model Works
            </DialogTitle>
            <DialogDescription>
              Understanding the NFL game totals prediction model
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 mt-4 text-sm text-slate-700">
            <section>
              <h3 className="font-semibold text-slate-900 mb-2">📊 Data Sources</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-600">
                <li><strong>nflfastR:</strong> 49,000+ plays from 2024-25 seasons (70% current, 30% historical weight)</li>
                <li><strong>Vegas Lines:</strong> Real-time odds from The-Odds-API</li>
                <li><strong>Injury Data:</strong> Automated weekly scrape from ESPN</li>
              </ul>
            </section>

            <section>
              <h3 className="font-semibold text-slate-900 mb-2">🔬 Model Features (16 total)</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-600">
                <li><strong>EPA Metrics:</strong> Expected Points Added per play (passing, rushing, defensive)</li>
                <li><strong>Advanced Stats:</strong> Yards, TDs, turnovers, sack rates</li>
                <li><strong>Matchup History:</strong> Head-to-head records and seasonal patterns</li>
                <li><strong>Injury Adjustments:</strong> 15% EPA reduction per high-impact injury</li>
                <li><strong>Seasonal Weighting:</strong> Recent games weighted more heavily</li>
              </ul>
            </section>

            <section>
              <h3 className="font-semibold text-slate-900 mb-2">🎯 Model Type</h3>
              <p className="text-slate-600">
                <strong>Linear Regression</strong> trained on historical game totals. The model learns to predict total points from 16 input features. Mean Absolute Error (MAE) and R² score shown in the dashboard above.
              </p>
            </section>

            <section>
              <h3 className="font-semibold text-slate-900 mb-2">💡 Interpretation</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-600">
                <li><strong>Edge:</strong> Difference between model prediction and Vegas line (±2.0 threshold for recommendation)</li>
                <li><strong>Over/Under:</strong> Whether model predicts above or below Vegas total</li>
                <li>Green "OVER" = Model predicts high-scoring game vs Vegas</li>
                <li>Red "UNDER" = Model predicts low-scoring game vs Vegas</li>
              </ul>
            </section>

            <section className="bg-blue-50 p-3 rounded-lg border border-blue-200">
              <p className="text-xs text-slate-600">
                <strong>Disclaimer:</strong> This model is for educational purposes. Past performance does not guarantee future results. Always verify against official Vegas lines before placing any bets.
              </p>
            </section>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
