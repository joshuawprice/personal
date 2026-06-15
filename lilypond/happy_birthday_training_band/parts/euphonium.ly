\version "2.26.0"

\include "defs.ily"
\include "euphonium.ily"

\header {
  instrument = \markup { Euphonium }
}

\score {
  \new Staff = "euphonium" {
    \euphonium
  }
  \layout { }
  \midi { }
}

% vim: sts=2 sw=2 et
