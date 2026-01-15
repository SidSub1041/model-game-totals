// NFL Team logos and colors
export const teamLogos: Record<string, { emoji: string; color: string; bgColor: string }> = {
  ARI: { emoji: "🐦", color: "text-red-600", bgColor: "bg-red-100" },
  ATL: { emoji: "🦅", color: "text-red-600", bgColor: "bg-red-100" },
  BAL: { emoji: "🐦", color: "text-purple-700", bgColor: "bg-purple-100" },
  BUF: { emoji: "🦬", color: "text-blue-700", bgColor: "bg-blue-100" },
  CAR: { emoji: "🐆", color: "text-blue-700", bgColor: "bg-blue-100" },
  CHI: { emoji: "🐻", color: "text-blue-900", bgColor: "bg-orange-100" },
  CIN: { emoji: "🐯", color: "text-orange-700", bgColor: "bg-orange-100" },
  CLE: { emoji: "🟤", color: "text-orange-700", bgColor: "bg-orange-100" },
  DAL: { emoji: "⭐", color: "text-blue-600", bgColor: "bg-blue-100" },
  DEN: { emoji: "🐴", color: "text-orange-600", bgColor: "bg-orange-100" },
  DET: { emoji: "🦁", color: "text-blue-700", bgColor: "bg-blue-100" },
  GB: { emoji: "🧀", color: "text-green-700", bgColor: "bg-green-100" },
  HOU: { emoji: "🤠", color: "text-blue-900", bgColor: "bg-blue-100" },
  IND: { emoji: "🐴", color: "text-blue-700", bgColor: "bg-blue-100" },
  JAX: { emoji: "🐆", color: "text-teal-700", bgColor: "bg-teal-100" },
  KC: { emoji: "👑", color: "text-red-600", bgColor: "bg-red-100" },
  LAC: { emoji: "⚡", color: "text-blue-600", bgColor: "bg-blue-100" },
  LAR: { emoji: "🐏", color: "text-blue-700", bgColor: "bg-blue-100" },
  LV: { emoji: "🎰", color: "text-gray-900", bgColor: "bg-gray-100" },
  MIA: { emoji: "🐬", color: "text-cyan-600", bgColor: "bg-cyan-100" },
  MIN: { emoji: "👽", color: "text-purple-700", bgColor: "bg-purple-100" },
  NE: { emoji: "🪖", color: "text-blue-600", bgColor: "bg-blue-100" },
  NO: { emoji: "⚜️", color: "text-yellow-600", bgColor: "bg-yellow-100" },
  NYG: { emoji: "🗽", color: "text-blue-600", bgColor: "bg-blue-100" },
  NYJ: { emoji: "✈️", color: "text-green-700", bgColor: "bg-green-100" },
  PHI: { emoji: "🦅", color: "text-green-700", bgColor: "bg-green-100" },
  PIT: { emoji: "🖼️", color: "text-yellow-600", bgColor: "bg-yellow-100" },
  SEA: { emoji: "🦅", color: "text-blue-900", bgColor: "bg-blue-100" },
  SF: { emoji: "🏃", color: "text-red-600", bgColor: "bg-red-100" },
  TB: { emoji: "🏴", color: "text-red-700", bgColor: "bg-red-100" },
  TEN: { emoji: "🎸", color: "text-blue-700", bgColor: "bg-blue-100" },
  WAS: { emoji: "🪖", color: "text-red-600", bgColor: "bg-red-100" },
}

export function getTeamDisplay(abbr: string) {
  return teamLogos[abbr] || { emoji: "🏈", color: "text-gray-600", bgColor: "bg-gray-100" }
}
