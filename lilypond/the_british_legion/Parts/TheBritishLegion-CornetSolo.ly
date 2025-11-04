\version "2.24.1"

\include "../Globals.ily"

\header {
  instrument = \markup {
    \raise #1.5 {
      \column {
        \line { "Solo B" \tiny { \hspace #-0.5 { \raise #0.5 { \flat } } } "Cornet" }
      }
    }
  }
}

cornetOne = \relative c'' {
  \set Staff.midiInstrument = "trumpet"

  d8.\ff-> d16 d8 d8 a d |
  c8 a c d4.-> |
  ef8 d c d4 d8 |
  <<
    {
      \voiceOne g,4 r8 r4 r8 |
      r4 r8
    }
    \new CueVoice {
      \voiceTwo s4 g='8 g4 g8 |
      g4 g8
    }
  >> \oneVoice
  d'4\f^"Marcato" d8 | \mark \default
  \repeat volta 2 {
    g=''4.-> d4.-> |
    bf8 c d bf4 a8 |
    g2.~ |
    g4 r8 bf4->\sf bf8 |
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
    ef4->\<( d8) d4( e8) |
    fs4.\ff \shape #'((-0.1 . 2) (0.5 . 1.5) (0.8 . 0.5) (0.4 . 0)) Slur a,4( fs'8) |
    e4. a, |
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
    f8[ r c]\< a[ r f] |
    f'4.->\ff ef-> |
    d4.-> c8 d ef |
    d8[ r f,]\mf\< f bf d |
    f8[\> r d] bf4( a8) |
    g4.\mf\( bf |
    a4. g\) |
    f8[ r bf\<] d[ r f] |
    a4._>\sf( g4) r8 |
    \mBreak

    f8\ff d f d4.-> |
    d8 bf d bf4-> bf16( c) |
    d4 f,8 d'4 c8 |
  }
  \alternative {
    {
      bf8 << { f'='' f \repeat tremolo 3 f }
         { f,=' f \repeat tremolo 3 f } >> |
    }
    {
      %bf='8 d d \repeat tremolo 3 d\< |
      bf='8 << { d d \repeat tremolo 3 d }
        { bf bf \repeat tremolo 3 bf } >> |
    }
  }
  <<
    % Top part at C
    {
      d8 d d \repeat tremolo 3 d\ff \mark \default \bar "||"

      \repeat tremolo 3 d \repeat tremolo 3 d |
      \repeat tremolo 3 d \repeat tremolo 3 d |

      r8 ef ef \repeat tremolo 3 ef |
      \repeat tremolo 3 ef8 \repeat tremolo 3 ef |
      r8 \repeat tremolo 2 ef8 r \repeat tremolo 2 ef |
      \mBreak

      r8 \repeat tremolo 2 ef r \repeat tremolo 2 c |
      d8 f, g a^[ bf c] |
      \repeat tremolo 3 d8 \repeat tremolo 3 d |
      r8 \repeat tremolo 2 d bf c d |
      \repeat tremolo 3 ef8 \repeat tremolo 3 ef |
      r8 \repeat tremolo 2 e c d e |
      \repeat tremolo 3 f8 \repeat tremolo 3 ef |
      \repeat tremolo 3 d8 \repeat tremolo 3 d |
      \repeat tremolo 3 c8 \repeat tremolo 3 ef |
      d4 \oneVoice r8 r4 \voiceOne bf8-> |
      d4-> \oneVoice r8 \voiceOne f4-> \oneVoice r8 \voiceOne |
      << bf4-> bf, >> \oneVoice r8 r4 r8
    }

    % Lower part at C
    {
      bf8 bf bf \repeat tremolo 3 bf |
      \repeat tremolo 3 bf8 \repeat tremolo 3 bf |
      \repeat tremolo 3 bf8 \repeat tremolo 3 bf |
      r8 bf bf \repeat tremolo 3 bf |
      \repeat tremolo 3 c \repeat tremolo 3 c |
      r8 \repeat tremolo 2 c r \repeat tremolo 2 c |
      \mBreak

      r8 \repeat tremolo 2 c r \repeat tremolo 2 a |
      bf8 s2 s8 |
      \repeat tremolo 3 bf8 \repeat tremolo 3 bf |
      r8 \repeat tremolo 2 bf8 s4 s8 |
      s2.*2 |
      \repeat tremolo 3 c8 \repeat tremolo 3 c8 |
      \repeat tremolo 3 bf8 \repeat tremolo 3 bf8 |
      \repeat tremolo 3 a \repeat tremolo 3 a |
      bf4 s2 |
      bf4
    }
    \\
    % Basses
    \new CueVoice {
      \voiceTwo s4. f8 g a_"Basses.Marcato" |
      bf2. |
      f4. d8 ef f |
      g4.~ g4 ef8 |
      c4. d4 ef8 |
      f4. a4 g8 |
      \mBreak

      f4. ef |
      d2.~ |
      d4 r8 f g a |
      bf4. af |
      g4. g8 a bf |
      c4. bf |
      a4. f8 g a |
      bf4 d,8 ef4 e8 |
      f4. f |
      bf,4 s8 s4 bf'8-> |
      f4-> s8 d4-> s8 |
      bf4->

    }
  >> \oneVoice
  \endFermata
  \mBreak


  \section
  \sectionLabel "Trio."
  % "|.:"
  \repeat volta 2 {
    \key c \minor
    g'='2.\p\(^"Cantabile" |
    \acciaccatura bf8 af4 g8 af4 f8\) |
    bf4.--\<\( ef--\! |
    d4.--\> c--\!\) |
    bf4.--\( c-- |
    bf4.-- g--\) |
    bf8-.[ r a-.] af4.^>~ |
    af4 r8 af4( g8) |
    f4.\( e |
    f8\) r e\( f4 fs8\) |
    g4.\( bf |
    c4. ef\) |
    \mBreak

    d4.\( f,4 d'8\) |
    \acciaccatura d8 c4\( b8 c4 d8\) |
    <<
      {
        \voiceTwo bf2.~\< |
        bf2.\> |
        af4.(\! g4.) |
        f4\( e8 f4 fs8\) |
        g4. bf~ |
      }


      \\
      \new CueVoice {
        \voiceOne r4 g'=''8-.  g-.[ r f-.] |
        ef8-.[ r d-.] c-.[ d8 \rest bf-.] \mark \default |
        bf8-.^"Leggiero"[ d8 \rest bf-.] bf-.[ r bf-.] |
        bf8-.[ r bf-.] bf-. d-. c-. |
        bf8-.[ r ef-.] ef-. d-. c-. |
      }
    >> \oneVoice
    << \once \override Stem.length = #4.5 bf4 \\ bf4 >> bf8\( a4 bf8\) |
    \override DynamicTextSpanner.style = #'none c4.\cresc b4 c8 |
    d4. d |

    d2.~\< |
    d4 r8 g4->\ff( f8) |
    \mBreak

    ef4.-> ef-> |
    e4.-> e-> |
    f4 e8 f4 g8 |
    af4-> c,8 d4( c8) |
    bf8 g bf ef bf ef |
    g4. f4. |
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
