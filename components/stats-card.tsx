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
    <Card className="bg-white border-slate-200 shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-1 font-medium">{label}</p>
            <p className="text-2xl font-semibold text-slate-900">{value}</p>
            {subValue && <p className="text-xs text-slate-600 mt-1">{subValue}</p>}
          </div>
          {icon && <div className="text-slate-400">{icon}</div>}
        </div>
      </CardContent>
    </Card>
  )
}
