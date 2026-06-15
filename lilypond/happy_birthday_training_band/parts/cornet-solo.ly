\version "2.26.0"

\include "defs.ily"
\include "cornet-solo.ily"

\header {
  instrument = \markup { Solo \concat { B \raise #0.5 \tiny \flat } Cornet }
}

\score {
  \new Staff = "cornetSolo" {
    \cornetSolo
  }
  \layout { }
  \midi { }
}

% vim: sts=2 sw=2 et
