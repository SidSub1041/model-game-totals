import { GameCard } from "@/components/game-card"
import { StatsCard } from "@/components/stats-card"
import { ModelMetrics } from "@/components/model-metrics"
import { PlayoffBranding } from "@/components/playoff-branding"
import { TrendingUpIcon, TargetIcon, CalendarIcon, ActivityIcon } from "lucide-react"
import { analysisData } from "@/lib/sample-data"
import { loadAnalysisData } from "@/lib/data-loader"

export default async function Home() {
  // Load actual data from generated JSON files, fallback to sample data
  let displayData = analysisData
  
  try {
    const actualData = await loadAnalysisData()
    if (actualData) {
      displayData = actualData
    }
  } catch (error) {
    console.warn("Could not load actual analysis data, using sample data:", error)
  }

  const { games, modelMetrics, summaryStats, season, generatedAt, playoffWeekend } = displayData
  
  // Format date on server side to avoid hydration mismatch
  const formattedDate = new Date(generatedAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
  
  return (
    <main className="min-h-screen relative overflow-hidden bg-gradient-to-br from-blue-400 via-purple-400 to-pink-300">
      {/* Vibrant background with animated pattern */}
      <div 
        className="fixed inset-0 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-400 z-0"
        style={{
          background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 25%, #ec4899 50%, #f97316 75%, #eab308 100%)',
          animation: 'gradientShift 15s ease infinite',
          backgroundSize: '200% 200%'
        }}
      >
        {/* Overlay for depth - semi-transparent white */}
        <div className="absolute inset-0 bg-white/10 backdrop-blur-sm" />
        
        {/* Accent circles for dynamic look */}
        <div className="absolute top-10 left-10 w-64 h-64 bg-blue-300 rounded-full opacity-20 blur-3xl" />
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-pink-300 rounded-full opacity-20 blur-3xl" />
        <div className="absolute top-1/2 left-1/3 w-72 h-72 bg-purple-300 rounded-full opacity-20 blur-3xl" />
      </div>

      {/* Playoff Branding - Logos and Bracket */}
      <PlayoffBranding />

      {/* Animated background decorations */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-5">
        <div className="absolute top-10 left-10 text-8xl opacity-5 animate-bounce">🏈</div>
        <div className="absolute top-40 right-20 text-7xl opacity-5 animate-pulse">🏈</div>
        <div className="absolute bottom-32 left-1/4 text-6xl opacity-5">🏈</div>
        <div className="absolute bottom-16 right-1/3 text-7xl opacity-5 animate-bounce" style={{ animationDelay: "1s" }}>🏈</div>
        <div className="absolute top-1/3 right-10 text-5xl opacity-5">⭐</div>
        <div className="absolute bottom-40 left-32 text-6xl opacity-5">⭐</div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 relative z-10">
        {/* Header */}
        <div className="mb-10">
          <div className="inline-block mb-4">
            <div className="flex items-center gap-3 bg-gradient-to-r from-orange-500 to-red-600 px-6 py-3 rounded-full shadow-xl hover:shadow-2xl transition">
              <span className="text-3xl">🏈</span>
              <h1 className="text-3xl font-black text-white">NFL Game Totals Analysis</h1>
            </div>
          </div>
          <p className="text-lg font-bold text-white drop-shadow-lg mt-4">{playoffWeekend || `Divisional Round ${season + 1}`}</p>
          <p className="text-sm text-white drop-shadow-md mt-1">Model vs Vegas Projections • Data from nflfastR • Updated {formattedDate}</p>
          <p className="text-xs text-white/70 drop-shadow-md mt-3 italic">Designed by Sid Subramanian</p>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <StatsCard
            label="Games Analyzed"
            value={summaryStats.gamesAnalyzed}
            subValue="Divisional Round"
            icon={<CalendarIcon className="w-5 h-5" />}
          />
          <StatsCard
            label="Avg Edge"
            value={`${summaryStats.avgEdge >= 0 ? "+" : ""}${summaryStats.avgEdge.toFixed(1)}`}
            subValue="Points vs Vegas"
            icon={<TrendingUpIcon className="w-5 h-5" />}
          />
          <StatsCard
            label="Over Picks"
            value={summaryStats.overPicks}
            subValue="Model favors high"
            icon={<TargetIcon className="w-5 h-5" />}
          />
          <StatsCard
            label="Under Picks"
            value={summaryStats.underPicks}
            subValue="Model favors low"
            icon={<ActivityIcon className="w-5 h-5" />}
          />
        </div>

        {/* Model Metrics */}
        <div className="mb-10">
          <ModelMetrics
            r2Score={modelMetrics.r2_score}
            mae={modelMetrics.mae}
            rmse={modelMetrics.rmse}
            trainingSamples={modelMetrics.training_samples}
          />
        </div>

        {/* Games Grid */}
        <div className="mb-8">
          <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
            <span className="text-4xl">🎯</span>
            Game Projections
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {games.map((game, index) => (
              <GameCard
                key={index}
                homeTeam={game.homeTeam}
                awayTeam={game.awayTeam}
                homeAbbr={game.homeAbbr}
                awayAbbr={game.awayAbbr}
                gameDate={game.gameDate}
                gameTime={game.gameTime}
                vegasTotal={game.vegasTotal}
                modelTotal={game.modelTotal}
                homeScore={game.homeScore}
                awayScore={game.awayScore}
                edge={game.edge}
                recommendation={game.recommendation}
                homeOffEpa={game.homeOffEpa}
                homeDefEpa={game.homeDefEpa}
                awayOffEpa={game.awayOffEpa}
                awayDefEpa={game.awayDefEpa}
                homeMoneyline={game.homeMoneyline}
                awayMoneyline={game.awayMoneyline}
              />
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-700 pt-12 border-t-2 border-gray-300 bg-gradient-to-r from-orange-100 to-amber-100 rounded-lg p-6 mt-12">
          <p className="font-semibold">🏈 Model trained on {season} regular season data using EPA and scoring metrics from nflfastR</p>
          <p className="mt-2 text-gray-600">Edge threshold: ±2.0 points for recommendations • Live Vegas odds powered by The-Odds-API</p>
        </div>
      </div>
    </main>
  )
}
