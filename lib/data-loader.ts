/**
 * Data Loader - Loads actual analysis data from JSON files
 * Falls back to sample data if files don't exist
 */

import { readFile } from "fs/promises"
import { join } from "path"

export interface Game {
  homeTeam: string
  awayTeam: string
  homeAbbr: string
  awayAbbr: string
  gameDate: string
  gameTime: string
  vegasTotal: number
  modelTotal: number
  homeScore: number
  awayScore: number
  edge: number
  recommendation: string
  homeOffEpa?: number
  homeDefEpa?: number
  awayOffEpa?: number
  awayDefEpa?: number
  homeMoneyline?: number | null
  awayMoneyline?: number | null
}

export interface AnalysisData {
  generatedAt: string
  season?: number
  playoffWeekend?: string
  trainingSeasons?: number[]
  modelMetrics: {
    r2_score: number
    mae: number
    rmse: number
    training_samples: number
  }
  summaryStats: {
    gamesAnalyzed: number
    avgEdge: number
    overPicks: number
    underPicks: number
    holdPicks: number
    avgModelTotal: number
    avgVegasTotal: number
  }
  games: Game[]
}

export async function loadAnalysisData(): Promise<AnalysisData | null> {
  try {
    const dataPath = join(process.cwd(), "public/data/nfl_analysis.json")
    const fileContent = await readFile(dataPath, "utf-8")
    const data = JSON.parse(fileContent)

    // Transform the data to match our expected format
    return transformAnalysisData(data)
  } catch (error) {
    console.error("Error loading analysis data:", error)
    return null
  }
}

function transformAnalysisData(rawData: any): AnalysisData | null {
  try {
    // Load Vegas lines data if available
    let vegasLinesMap: Record<string, any> = {}
    // Note: In a real implementation, you'd load the vegas_lines.json here
    // For now, the data doesn't include moneyline, so we'll leave it as null
    
    // Transform games from nflfastr format to display format
    const transformedGames: Game[] = (rawData.games || []).map((game: any) => ({
      homeTeam: game.homeTeam,
      awayTeam: game.awayTeam,
      homeAbbr: game.homeAbbr,
      awayAbbr: game.awayAbbr,
      gameDate: game.gameDate,
      gameTime: game.gameTime,
      vegasTotal: game.vegasTotal,
      modelTotal: game.modelTotal,
      homeScore: game.homeScore,
      awayScore: game.awayScore,
      edge: game.edge,
      recommendation: game.recommendation,
      homeOffEpa: game.homeOffEpa,
      homeDefEpa: game.homeDefEpa,
      awayOffEpa: game.awayOffEpa,
      awayDefEpa: game.awayDefEpa,
      homeMoneyline: game.homeMoneyline || null,
      awayMoneyline: game.awayMoneyline || null,
    }))

    return {
      generatedAt: rawData.generatedAt,
      season: 2025, // 2025-26 season
      playoffWeekend: rawData.playoffWeekend,
      trainingSeasons: rawData.trainingSeasons,
      modelMetrics: rawData.modelMetrics,
      summaryStats: rawData.summaryStats,
      games: transformedGames,
    }
  } catch (error) {
    console.error("Error transforming analysis data:", error)
    return null
  }
}

export async function loadInjuryData(): Promise<any> {
  try {
    const dataPath = join(process.cwd(), "public/data/injury_report.json")
    const fileContent = await readFile(dataPath, "utf-8")
    return JSON.parse(fileContent)
  } catch (error) {
    console.warn("Could not load injury data from file:", error)
    return { advisory: { high_impact: [] } }
  }
}
