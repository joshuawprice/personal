\version "2.26.0"
\language "english"

euphonium = \relative c' {
  \transposition bf
  \key bf \major
  \time 3/4

  \partial 4 f8 8 |
  g4 f bf |
  a2 f8 8 |
  g4 f c' |

  bf2 f8 8 |
  \shiftOnn
  <f f'>4 f <d d'> |
  <f f'>( <ef ef'>)\fermata <g g'> |
  <f f'>2 <ef ef'>4 |
  <d d'>2\fermata
  \bar "|."
  \barNumberCheck 8
}
