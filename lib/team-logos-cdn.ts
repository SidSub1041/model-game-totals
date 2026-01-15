/**
 * NFL Team Display Configuration
 * Using team initials with brand colors for clean, reliable display
 */

export const teamLogos: Record<
  string,
  { logo: string; color: string; bgColor: string }
> = {
  ARI: {
    logo: "ARI",
    color: "text-red-600",
    bgColor: "bg-red-100",
  },
  ATL: {
    logo: "ATL",
    color: "text-red-600",
    bgColor: "bg-red-100",
  },
  BAL: {
    logo: "BAL",
    color: "text-purple-700",
    bgColor: "bg-purple-100",
  },
  BUF: {
    logo: "BUF",
    color: "text-blue-700",
    bgColor: "bg-blue-100",
  },
  CAR: {
    logo: "CAR",
    color: "text-blue-700",
    bgColor: "bg-blue-100",
  },
  CHI: {
    logo: "CHI",
    color: "text-orange-700",
    bgColor: "bg-orange-100",
  },
  CIN: {
    logo: "CIN",
    color: "text-orange-700",
    bgColor: "bg-orange-100",
  },
  CLE: {
    logo: "CLE",
    color: "text-orange-700",
    bgColor: "bg-orange-100",
  },
  DAL: {
    logo: "DAL",
    color: "text-blue-600",
    bgColor: "bg-blue-100",
  },
  DEN: {
    logo: "DEN",
    color: "text-orange-600",
    bgColor: "bg-orange-100",
  },
  DET: {
    logo: "DET",
    color: "text-blue-700",
    bgColor: "bg-blue-100",
  },
  GB: {
    logo: "GB",
    color: "text-green-700",
    bgColor: "bg-green-100",
  },
  HOU: {
    logo: "HOU",
    color: "text-blue-900",
    bgColor: "bg-blue-100",
  },
  IND: {
    logo: "IND",
    color: "text-blue-700",
    bgColor: "bg-blue-100",
  },
  JAX: {
    logo: "JAX",
    color: "text-teal-700",
    bgColor: "bg-teal-100",
  },
  KC: {
    logo: "KC",
    color: "text-red-600",
    bgColor: "bg-red-100",
  },
  LAC: {
    logo: "LAC",
    color: "text-blue-600",
    bgColor: "bg-blue-100",
  },
  LAR: {
    logo: "LAR",
    color: "text-blue-700",
    bgColor: "bg-blue-100",
  },
  LV: {
    logo: "LV",
    color: "text-gray-900",
    bgColor: "bg-gray-100",
  },
  MIA: {
    logo: "MIA",
    color: "text-cyan-600",
    bgColor: "bg-cyan-100",
  },
  MIN: {
    logo: "MIN",
    color: "text-purple-700",
    bgColor: "bg-purple-100",
  },
  NE: {
    logo: "NE",
    color: "text-blue-600",
    bgColor: "bg-blue-100",
  },
  NO: {
    logo: "NO",
    color: "text-yellow-600",
    bgColor: "bg-yellow-100",
  },
  NYG: {
    logo: "NYG",
    color: "text-blue-600",
    bgColor: "bg-blue-100",
  },
  NYJ: {
    logo: "NYJ",
    color: "text-green-700",
    bgColor: "bg-green-100",
  },
  PHI: {
    logo: "PHI",
    color: "text-green-700",
    bgColor: "bg-green-100",
  },
  PIT: {
    logo: "PIT",
    color: "text-yellow-600",
    bgColor: "bg-yellow-100",
  },
  SEA: {
    logo: "SEA",
    color: "text-blue-900",
    bgColor: "bg-blue-100",
  },
  SF: {
    logo: "SF",
    color: "text-red-600",
    bgColor: "bg-red-100",
  },
  TB: {
    logo: "TB",
    color: "text-red-700",
    bgColor: "bg-red-100",
  },
  TEN: {
    logo: "TEN",
    color: "text-blue-700",
    bgColor: "bg-blue-100",
  },
  WAS: {
    logo: "WAS",
    color: "text-red-600",
    bgColor: "bg-red-100",
  },
}

export function getTeamDisplay(abbr: string) {
  return (
    teamLogos[abbr] || {
      logo: abbr,
      color: "text-gray-600",
      bgColor: "bg-gray-100",
    }
  )
}

