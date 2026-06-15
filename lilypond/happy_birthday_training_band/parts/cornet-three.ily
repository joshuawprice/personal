\version "2.26.0"
\language "english"

cornetThree = \relative c' {
  \transposition bf
  \key bf \major
  \time 3/4

  \partial 4 r4 |
  d4 d d |
  ef2 8 8 |
  ef4 4 4 |

  d2 c8 8 |
  r4 d d |
  r4 bf\fermata 4 |
  d f f |
  f2\fermata
  \bar "|."
  \barNumberCheck 8
}
