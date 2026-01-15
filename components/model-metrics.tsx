import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ModelMetricsProps {
  r2Score: number
  mae: number
  rmse: number
  trainingSamples: number
}

export function ModelMetrics({ r2Score, mae, rmse, trainingSamples }: ModelMetricsProps) {
  return (
    <Card className="bg-card border-border">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
          Model Performance
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-xs text-muted-foreground mb-1">R² Score</p>
            <p className="text-xl font-mono font-bold text-primary">{r2Score.toFixed(3)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-1">MAE</p>
            <p className="text-xl font-mono font-bold">{mae.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-1">RMSE</p>
            <p className="text-xl font-mono font-bold">{rmse.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-1">Training Samples</p>
            <p className="text-xl font-mono font-bold">{trainingSamples}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
