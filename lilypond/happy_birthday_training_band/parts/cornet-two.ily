\version "2.26.0"
\language "english"

cornetTwo = \relative c' {
  \transposition bf
  \key bf \major
  \time 3/4

  \partial 4 r4 |
  g'4 f f |
  f2 8 8 |
  g4 f a |

  f2 8 8 |
  r4 f f |
  r4 ef\fermata 4 |
  f d ef |
  d2\fermata
  \bar "|."
  \barNumberCheck 8
}

% vim: sts=2 sw=2 et
