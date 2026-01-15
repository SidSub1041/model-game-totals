'use client'

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowUpIcon, ArrowDownIcon, MinusIcon } from "lucide-react"
import { getTeamDisplay } from "@/lib/team-logos-cdn"

interface GameCardProps {
  homeTeam: string
  awayTeam: string
  homeAbbr?: string
  awayAbbr?: string
  gameDate: string
  gameTime: string
  vegasTotal: number
  modelTotal: number
  homeScore: number
  awayScore: number
  edge?: number
  recommendation: "over" | "under" | "hold"
  homeOffEpa?: number
  homeDefEpa?: number
  awayOffEpa?: number
  awayDefEpa?: number
  homeMoneyline?: number | null
  awayMoneyline?: number | null
}

export function GameCard({
  homeTeam,
  awayTeam,
  homeAbbr,
  awayAbbr,
  gameDate,
  gameTime,
  vegasTotal,
  modelTotal,
  homeScore,
  awayScore,
  edge: edgeProp,
  recommendation,
  homeOffEpa,
  homeDefEpa,
  awayOffEpa,
  awayDefEpa,
  homeMoneyline,
  awayMoneyline,
}: GameCardProps) {
  const edge = edgeProp ?? modelTotal - vegasTotal
  const edgePercent = ((edge / vegasTotal) * 100).toFixed(1)

  const homeDisplayAbbr = homeAbbr || homeTeam.substring(0, 3).toUpperCase()
  const awayDisplayAbbr = awayAbbr || awayTeam.substring(0, 3).toUpperCase()
  
  const homeTeamDisplay = getTeamDisplay(homeDisplayAbbr)
  const awayTeamDisplay = getTeamDisplay(awayDisplayAbbr)
  
  const formatOdds = (odds: number | null | undefined) => {
    if (!odds) return "—"
    return odds > 0 ? `+${odds}` : `${odds}`
  }

  return (
    <div className="relative overflow-hidden rounded-lg border-2 shadow-lg hover:shadow-xl transition-all bg-gradient-to-br from-sky-50 via-white to-amber-50">
      {/* Decorative footballs in background */}
      <div className="absolute -top-8 -right-8 text-6xl opacity-10">🏈</div>
      <div className="absolute -bottom-8 -left-8 text-5xl opacity-10">🏈</div>
      <div className="absolute top-1/2 right-4 text-4xl opacity-5">🏈</div>
      
      <CardContent className="p-6 relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-r from-amber-400 to-orange-500 px-3 py-1 rounded-full">
              <span className="text-xs font-bold text-white">{gameDate}</span>
            </div>
            <span className="text-sm font-semibold text-gray-600">{gameTime}</span>
          </div>
          <Badge
            className={`px-3 py-1.5 font-bold text-sm gap-2 ${
              recommendation === "over"
                ? "bg-gradient-to-r from-green-500 to-emerald-600 text-white"
                : recommendation === "under"
                  ? "bg-gradient-to-r from-red-500 to-rose-600 text-white"
                  : "bg-gradient-to-r from-gray-500 to-slate-600 text-white"
            }`}
          >
            {recommendation === "over" && <ArrowUpIcon className="w-4 h-4" />}
            {recommendation === "under" && <ArrowDownIcon className="w-4 h-4" />}
            {recommendation === "hold" && <MinusIcon className="w-4 h-4" />}
            {recommendation.toUpperCase()}
          </Badge>
        </div>

        {/* Teams and Scores */}
        <div className="space-y-3 mb-5">
          {/* Away Team */}
          <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition">
            <div className="flex items-center gap-3">
              <div className={`w-14 h-14 rounded-full ${awayTeamDisplay.bgColor} ${awayTeamDisplay.color} flex items-center justify-center shadow-md font-bold text-sm`}>
                {awayTeamDisplay.logo}
              </div>
              <div>
                <p className="text-xs text-gray-500 font-semibold uppercase">Away</p>
                <p className="font-bold text-gray-900">{awayTeam}</p>
                {awayOffEpa !== undefined && awayDefEpa !== undefined && (
                  <div className="flex gap-3 text-xs mt-1">
                    <span className={`font-semibold ${awayOffEpa > 0 ? "text-green-600" : "text-red-600"}`}>
                      O: {awayOffEpa > 0 ? "+" : ""}{awayOffEpa.toFixed(3)}
                    </span>
                    <span className={`font-semibold ${awayDefEpa < 0 ? "text-green-600" : "text-red-600"}`}>
                      D: {awayDefEpa > 0 ? "+" : ""}{awayDefEpa.toFixed(3)}
                    </span>
                  </div>
                )}
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-black text-sky-600">{awayScore.toFixed(1)}</div>
              <div className="text-xs text-gray-500 mt-1">pts</div>
            </div>
          </div>

          {/* Home Team */}
          <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition">
            <div className="flex items-center gap-3">
              <div className={`w-14 h-14 rounded-full ${homeTeamDisplay.bgColor} ${homeTeamDisplay.color} flex items-center justify-center shadow-md font-bold text-sm`}>
                {homeTeamDisplay.logo}
              </div>
              <div>
                <p className="text-xs text-gray-500 font-semibold uppercase">Home</p>
                <p className="font-bold text-gray-900">{homeTeam}</p>
                {homeOffEpa !== undefined && homeDefEpa !== undefined && (
                  <div className="flex gap-3 text-xs mt-1">
                    <span className={`font-semibold ${homeOffEpa > 0 ? "text-green-600" : "text-red-600"}`}>
                      O: {homeOffEpa > 0 ? "+" : ""}{homeOffEpa.toFixed(3)}
                    </span>
                    <span className={`font-semibold ${homeDefEpa < 0 ? "text-green-600" : "text-red-600"}`}>
                      D: {homeDefEpa > 0 ? "+" : ""}{homeDefEpa.toFixed(3)}
                    </span>
                  </div>
                )}
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-black text-orange-600">{homeScore.toFixed(1)}</div>
              <div className="text-xs text-gray-500 mt-1">pts</div>
            </div>
          </div>
        </div>

        {/* Odds and Totals */}
        <div className="mt-5 pt-5 border-t-2 border-gray-200">
          <div className="grid grid-cols-4 gap-3 text-center">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-3 rounded-lg border border-blue-200">
              <p className="text-xs text-gray-700 font-semibold mb-1">Vegas O/U</p>
              <p className="font-mono font-black text-lg text-blue-700">{vegasTotal.toFixed(1)}</p>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-3 rounded-lg border border-purple-200">
              <p className="text-xs text-gray-700 font-semibold mb-1">Model O/U</p>
              <p className="font-mono font-black text-lg text-purple-700">{modelTotal.toFixed(1)}</p>
            </div>
            <div className={`bg-gradient-to-br ${edge > 0 ? "from-emerald-50 to-emerald-100 border-emerald-200" : "from-rose-50 to-rose-100 border-rose-200"} p-3 rounded-lg border`}>
              <p className="text-xs text-gray-700 font-semibold mb-1">Edge</p>
              <p className={`font-mono font-black text-lg ${edge > 0 ? "text-emerald-700" : "text-rose-700"}`}>
                {edge > 0 ? "+" : ""}{edge.toFixed(1)}
              </p>
            </div>
            <div className="bg-gradient-to-br from-amber-50 to-amber-100 p-3 rounded-lg border border-amber-200">
              <p className="text-xs text-gray-700 font-semibold mb-1">% Edge</p>
              <p className="font-mono font-black text-lg text-amber-700">{edgePercent}%</p>
            </div>
          </div>
        </div>

        {/* Moneyline Odds (if available) */}
        {(homeMoneyline || awayMoneyline) && (
          <div className="mt-4 pt-4 border-t-2 border-gray-200">
            <p className="text-xs font-semibold text-gray-600 mb-3">Moneyline</p>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-sky-100 p-2 rounded-lg border border-sky-300 text-center">
                <p className="text-xs text-gray-600 mb-1">{awayTeam}</p>
                <p className="font-mono font-black text-sky-700">{formatOdds(awayMoneyline)}</p>
              </div>
              <div className="bg-orange-100 p-2 rounded-lg border border-orange-300 text-center">
                <p className="text-xs text-gray-600 mb-1">{homeTeam}</p>
                <p className="font-mono font-black text-orange-700">{formatOdds(homeMoneyline)}</p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </div>
  )
}
