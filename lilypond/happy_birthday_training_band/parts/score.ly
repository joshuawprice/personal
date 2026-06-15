\version "2.26.0"

\include "defs.ily"

\include "cornet-solo.ily"
\include "cornet-two.ily"
\include "cornet-three.ily"
\include "horn-one.ily"
\include "euphonium.ily"

\paper {
  ragged-last-bottom = ##f
  #(set-paper-size "a4" 'landscape)
}

\score {
  <<
    \new Staff = "cornetSolo" \with {
      instrumentName = \markup {
        \center-column { "Solo Cornet"
          \line { in \concat { B \raise #0.5 \tiny \flat } }
        }
      }
    } {
      \cornetSolo
    }
    \new Staff = "cornetTwo" \with {
      instrumentName = \markup {
        \center-column { "2nd Cornet"
          \line { in \concat { B \raise #0.5 \tiny \flat } }
        }
      }
    } {
      \cornetTwo
    }
    \new Staff = "cornetThree" \with {
      instrumentName = \markup {
        \center-column { "3rd Cornet"
          \line { in \concat { B \raise #0.5 \tiny \flat } }
        }
      }
    } {
      \cornetThree
    }
    \new Staff = "hornOne" \with {
      instrumentName = \markup {
        \center-column { "1st Horn"
          \line { in \concat { E \raise #0.5 \tiny \flat } }
        }
      }
    } {
      \hornOne
    }
    \new Staff = "euphonium" \with {
      instrumentName = \markup {
        \center-column { "Euphonium"
          \line { in \concat { B \raise #0.5 \tiny \flat } }
        }
      }
    } {
      \euphonium
    }
  >>
  \layout { 
      indent = 2.2\cm
  }
  \midi { }
}

% vim: sts=2 sw=2 et
