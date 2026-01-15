import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ModelMetricsProps {
  r2Score: number
  mae: number
  rmse: number
  trainingSamples: number
}

export function ModelMetrics({ r2Score, mae, rmse, trainingSamples }: ModelMetricsProps) {
  return (
    <Card className="bg-white border-slate-200 shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-slate-700 uppercase tracking-wider">
          Model Performance
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-xs text-slate-600 mb-1 font-medium">R² Score</p>
            <p className="text-xl font-semibold text-slate-900">{r2Score.toFixed(3)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-600 mb-1 font-medium">MAE</p>
            <p className="text-xl font-semibold text-slate-900">{mae.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-600 mb-1 font-medium">RMSE</p>
            <p className="text-xl font-semibold text-slate-900">{rmse.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-600 mb-1 font-medium">Training Samples</p>
            <p className="text-xl font-semibold text-slate-900">{trainingSamples}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
