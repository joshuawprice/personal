\version "2.26.0"
\language "english"

hornOne = \relative c' {
  \transposition ef
  \key f \major
  \time 3/4

  \partial 4 r4 |
  r4 a' a4 |
  r4 bf2 |
  r4 bf bf |
  r4 a bf8 8 |

  r4 a a |
  r4 bf\fermata <d d,> |
  c4 a bf |
  a2\fermata
  \bar "|."
  \barNumberCheck 8
}
