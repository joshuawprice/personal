\version "2.26.0"

\include "defs.ily"
\include "horn-one.ily"

\header {
  instrument = \markup {
    \column \center-align {
      \line { 1st \concat { E \raise #0.5 \tiny \flat } Horn }
      \line { \concat { E \raise #0.5 \tiny \flat } Mini P. Bone  }
    }
  }
}

\score {
  \new Staff = "hornOne" {
    \hornOne
  }
  \layout { }
  \midi { }
}

% vim: sts=2 sw=2 et
