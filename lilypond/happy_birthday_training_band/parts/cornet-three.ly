\version "2.26.0"

\include "defs.ily"
\include "cornet-three.ily"

\header {
  instrument = \markup { 3rd \concat { B \raise #0.5 \tiny \flat } Cornet }
}

\score {
  \new Staff = "cornetThree" {
    \cornetThree
  }
  \layout { }
  \midi { }
}

% vim: sts=2 sw=2 et
