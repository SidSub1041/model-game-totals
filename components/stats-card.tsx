import type React from "react"
import { Card, CardContent } from "@/components/ui/card"

interface StatsCardProps {
  label: string
  value: string | number
  subValue?: string
  icon?: React.ReactNode
}

export function StatsCard({ label, value, subValue, icon }: StatsCardProps) {
  return (
    <Card className="bg-card border-border">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">{label}</p>
            <p className="text-2xl font-mono font-bold text-primary">{value}</p>
            {subValue && <p className="text-xs text-muted-foreground mt-1">{subValue}</p>}
          </div>
          {icon && <div className="text-muted-foreground">{icon}</div>}
        </div>
      </CardContent>
    </Card>
  )
}
