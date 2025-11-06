\version "2.24.1"

\include "../globals.ily"

\header {
  instrument = \markup {
    \raise #1.5 {
      \column {
        "Repiano / Flugel /"
        \line { 1 \super {\hspace #-0.6 st } B \tiny { \hspace #-0.5 { \raise #0.5 { \flat } } } "Cornet"  }
      }
    }
  }
}

cornetOne = \relative c'' {
  \set Staff.midiInstrument = "trumpet"

  d8.\ff-> d16 d8 d8 a d |
  c8 a c d4.-> |
  c8 bf a d4 d8 |
  g,4 r8 r4 r8 |
  r4 r8 d'4\< d8 | \mark \default
  \repeat volta 2 {
    g4.->\f^"Marcato" d4.-> |
    bf8 c d bf4 a8 |
    g2.~ |
    g4 r8 bf4-> bf8 |
    ef4.-> bf4.-> |
    g8 af bf g4 f8

    % Uncomment to remove the clef and key key signature from the beginning of each line.
    %\override Score.Clef.break-visibility = #all-invisible
    %\override Score.KeySignature.break-visibility = #all-invisible
    \mBreak

    ef2.~ |
    ef4 r8 ef4\mf ef8 |
    d8[ r8 d'8]\<_~ \slashedGrace ef8 d8 cs d |
    ef4->\sf( d8) ef4->( d8) |
    g,8[ r d'_~] \slashedGrace ef8 d8 cs d |
    ef4\<( d8) d4( e8) |
    fs4.\f \shape #'((-0.1 . 2) (0.5 . 1.5) (0.8 . 0.5) (0.4 . 0)) Slur a,4( fs'8) |
    e4.-> a,-> |
  }
  \alternative {
    {
      d8[ r d->\ff] ef->[ r d->] |
      c8-> bf-> a-> d->[ r d->] |
    }
    {
      d8->[ r a->] d->[ r a->] |
      d8-> r d \repeat tremolo 3 d | \mark \default
    }
  }
  \mBreak

  \repeat volta 2 {
    ef4.->\ff^"Con vigore" d-> |
    c4.-> b8 c d |
    c8[ r f,\mf] f a c |
    f8[ r c] a[ r f] |
    f'4.->\ff ef-> |
    d4.-> c8 d ef |
    d8[ r f,] f bf d |
    f8[ r d] bf4(\> a8) |
    g4.\mf\( bf |
    a4. g\) |
    f8[ r bf\<] d[ r f] |
    a4._>\sf( g4) r8 |
    \mBreak

    f8\ff d f d4.-> |
    d8 bf d bf4-> bf16( c) |
    d8[ r f,] d'[ r c] |
  }
  \alternative {
    {
      bf8 f' f f f f |
    }
    {
      bf,8 d d \repeat tremolo 3 d\< |
    }
  }
  \repeat tremolo 3 d \repeat tremolo 3 d \mark \default \bar "||"
  \repeat percent 2 {
    \repeat tremolo 3 d\ff \repeat tremolo 3 d |
  }
  r8 ef ef \repeat tremolo 3 ef |
  \repeat tremolo 3 ef8 \repeat tremolo 3 ef |
  r8 \repeat tremolo 2 ef8 r \repeat tremolo 2 ef |
  r8 \repeat tremolo 2 ef r \repeat tremolo 2 c |
  \mBreak

  d8 f, g a^[ bf c] |
  \repeat tremolo 3 d8 \repeat tremolo 3 d |
  r8 d d bf c d |
  \repeat tremolo 3 ef8 \repeat tremolo 3 ef |
  r8 e e c d e |
  \repeat tremolo 3 f8 \repeat tremolo 3 ef |
  \repeat tremolo 3 d8 \repeat tremolo 3 d |
  c8 c c ef ef ef |
  d4 r8 r4 bf8-> |
  d4-> r8 f4-> r8 |
  << bf4-> bf, >> r8 r4 r8
  \endFermata
  \mBreak


  \section
  \sectionLabel "Trio."
  % "|.:"
  \repeat volta 2 {
    \key c \minor
    g2.\p\(^"Cantabile" |
    \acciaccatura bf8 af4 g8 af4 f8\) |
    bf4.\<\( ef\! |
    d4.\> c\!\) |
    bf4.-- c-- |
    bf4.-- g-- |
    bf8-.[ r a-.\<] af4.^>~ |
    af4\!\> r8 af4( g8)\! |
    f4.\( e |
    f8\) r e\( f4 fs8\) |
    g4.\( bf |
    c4. ef\) |
    \mBreak

    d4.\( f,4 d'8\) |
    \acciaccatura d8 c4\( b8 c4 d8\) |
    bf8\<[ r g'-.]  g-.[ r f-.\!] |
    ef8-.\>[ r d-.] c-.[ r bf-.] \mark \default |
    bf8-.\p^"Leggiero"[ r bf-.] bf-.[ r bf-.] |
    bf8-.[ r bf-.] bf-. d-. c-. |
    bf8-.[ r ef-.] ef-. d-. c-. |
    bf4 bf8\( a4 bf8\) |
    \override DynamicTextSpanner.style = #'none c4.\cresc b4 c8 |
    d4. d |
    \mBreak

    d8 g, b d b d |
    g4 r8 g4->\ff f8 |
    ef4.-> ef-> |
    e4.-> e-> |
    f4-> e8-> f4-> g8-> |
    af4-> c,8-. d4->( c8) |
    bf8-. g-. bf-. ef-. bf-. ef-. |
    g4-. r8 f4.->\sf |
  }
  \alternative {
    {
      ef4\< \shape #'((-0.6 . 1.2) (0 . 0.4) (0 . 0) (0 . 0)) PhrasingSlur g,8\( d'4 c8\)\! |
      bf8\> af g f4( fs8)\!
    }
    {
      ef'8\< g, af bf c d |
      ef4\! r8 << ef4\sf-> g, >> r8_\markup { \bold \fontsize #1 "D.C." } \bar "|."
    }
  }
}


\score {
  \new Staff = "1st cornet" {
    \pieceTime
    \keyBb
    \autoPageBreaksOff

    \cornetOne
  }
  \layout { }
  \midi { }
}
