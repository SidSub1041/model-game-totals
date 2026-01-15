'use client'

export function PlayoffBranding() {
  return (
    <>
      {/* Playoff Logo - Top Right */}
      <div className="fixed top-6 right-6 z-30 pointer-events-none">
        <img 
          src="/images/NFL_Playoff_Logo.webp" 
          alt="Playoff Logo" 
          className="h-24 w-auto drop-shadow-lg"
          onError={(e) => {
            e.currentTarget.style.opacity = '0.5'
          }}
        />
      </div>

      {/* Playoff Bracket - Centered in Middle */}
      <div className="fixed inset-0 flex items-center justify-center z-5 pointer-events-none">
        <div className="max-w-3xl w-full px-4 opacity-40 hover:opacity-60 transition-opacity">
          <img 
            src="/images/NFL_Playoff_Bracket.avif" 
            alt="Playoff Bracket" 
            className="w-full drop-shadow-2xl"
            onError={(e) => {
              e.currentTarget.style.display = 'none'
            }}
          />
        </div>
      </div>
    </>
  )
}
