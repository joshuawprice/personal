\version "2.26.0"

\include "defs.ily"
\include "cornet-two.ily"

\header {
  instrument = \markup { 2nd \concat { B \raise #0.5 \tiny \flat } Cornet }
}

\score {
  \new Staff = "cornetTwo" {
    \cornetTwo
  }
  \layout { }
  \midi { }
}

% vim: sts=2 sw=2 et
