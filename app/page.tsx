import { GameCard } from "@/components/game-card"
import { StatsCard } from "@/components/stats-card"
import { ModelMetrics } from "@/components/model-metrics"
import { InjuryAlert } from "@/components/injury-alert"
import { ModelExplanationModal } from "@/components/model-explanation-modal"
import { InjuriesModal } from "@/components/injuries-modal"
import { TrendingUpIcon, TargetIcon, CalendarIcon, ActivityIcon, Github, BookOpen } from "lucide-react"
import { analysisData } from "@/lib/sample-data"
import { loadAnalysisData } from "@/lib/data-loader"

async function loadInjuryData() {
  try {
    const response = await fetch(new URL('public/data/injury_report.json', process.env.VERCEL_URL || 'http://localhost:3000').toString())
    if (response.ok) {
      return await response.json()
    }
  } catch (e) {
    console.warn("Could not load injury data:", e)
  }
  return { advisory: { high_impact: [] } }
}

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

  const injuryData = await loadInjuryData()
  const highImpactInjuries = injuryData.advisory?.high_impact || []

  const { games, modelMetrics, summaryStats, season, generatedAt, playoffWeekend } = displayData
  
  // Format date on server side to avoid hydration mismatch
  const formattedDate = new Date(generatedAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
  
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Subtle animated background pattern */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" />
        <div className="absolute -bottom-8 right-1/4 w-96 h-96 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 relative z-10">
        {/* Header */}
        <div className="mb-12">
          <div className="inline-block mb-4">
            <div className="flex items-center gap-3 bg-white px-6 py-3 rounded-lg shadow-sm border border-slate-200">
              <span className="text-3xl">🏈</span>
              <h1 className="text-3xl font-light text-slate-900" style={{ fontFamily: 'system-ui, -apple-system, sans-serif' }}>NFL Game Predictions</h1>
            </div>
          </div>
          <p className="text-lg font-light text-slate-700 mt-4">{playoffWeekend || `Divisional Round ${season + 1}`}</p>
          <p className="text-sm text-slate-600 mt-1">Data from nflfastR • Vegas Lines from The-Odds-API • Updated {formattedDate}</p>
          <p className="text-xs text-slate-500 mt-3 italic">Designed by Sid Subramanian</p>
        </div>

        {/* Injury Alert */}
        {highImpactInjuries.length > 0 && (
          <InjuryAlert highImpactInjuries={highImpactInjuries} />
        )}

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
          <h2 className="text-2xl font-semibold text-slate-900 mb-6 flex items-center gap-3">
            <span className="text-3xl">🎯</span>
            Divisional Round Predictions
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

        {/* Footer Info */}
        <div className="mt-16 pt-8 border-t border-slate-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* GitHub Link */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200 hover:shadow-md transition">
              <div className="flex items-center gap-3 mb-3">
                <Github size={20} className="text-slate-700" />
                <h3 className="font-semibold text-slate-900">View on GitHub</h3>
              </div>
              <p className="text-sm text-slate-600 mb-4">
                Check out the complete source code, data pipeline, and model training code.
              </p>
              <a
                href="https://github.com/SidSub1041/model-game-totals"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm"
              >
                github.com/SidSub1041/model-game-totals
                <span>→</span>
              </a>
            </div>

            {/* Model Explanation */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200 hover:shadow-md transition">
              <div className="flex items-center gap-3 mb-3">
                <BookOpen size={20} className="text-slate-700" />
                <h3 className="font-semibold text-slate-900">How It Works</h3>
              </div>
              <p className="text-sm text-slate-600 mb-4">
                Linear regression model trained on 49K+ plays from nflfastR data with EPA metrics, injury adjustments, and head-to-head records.
              </p>
              <ModelExplanationModal />
            </div>

            {/* Injury Reports */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200 hover:shadow-md transition">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-lg">⚠️</span>
                <h3 className="font-semibold text-slate-900">Injury Reports</h3>
              </div>
              <p className="text-sm text-slate-600 mb-4">
                High-impact injuries scraped from ESPN with automated updates each week.
              </p>
              <InjuriesModal injuries={highImpactInjuries.map(injury => ({
                team: injury.team,
                player: injury.player,
                position: injury.position,
                status: injury.status,
                impact: 'high'
              }))} />
            </div>
          </div>

          {/* Footer bottom */}
          <div className="text-center py-4 border-t border-slate-200">
            <p className="text-xs text-slate-500">
              Last updated: {formattedDate} • <a href="#" className="hover:text-slate-700">Privacy</a> • <a href="#" className="hover:text-slate-700">Contact</a>
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
