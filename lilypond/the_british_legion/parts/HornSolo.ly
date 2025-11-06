\version "2.24.1"

\include "../Globals.ily"

\header {
  instrument = \markup {
    \raise #1.5 {
      \column \center-align {
        \line { "Solo" E \tiny { \hspace #-0.5 { \raise #0.5 { \flat } } } "Saxhorn" }
        \line { "(E" \tiny { \hspace #-0.5 { \raise #0.5 { \flat } } } "Alto)"  }
      }
    }
  }
}

cornetOne = \relative c'' {
  \set Staff.midiInstrument = "trumpet"
  
  \repeat segno 2 {
      cs4\ff-> r8 r4 r8 |
      d4.-> cs-> |
      g'8 f e e4 e8 |
      d4 a8 a4 a8 |
      a4 a8 a4 a8 |
      \repeat volta 2 {
        \mark \default
        a4.\f( d) |
        d4.( cs) |
        d4 r8\f f,-> g-> a-> |
        d,4^> r8 a'4^> a8 |
        bf2. |
        \stemDown bf4.( \stemNeutral a) |
        \mBreak
        
        bf4 r8\f d8-> e-> f-> |
        bf,4. bf4 bf8 |
        cs4.\mf~ cs4 d8 |
        e4.\<( cs) |
        d4.\!~ d4 e8 |
        f4.\<( d)
        cs4.\f~ cs4 e8 |
        d4.-> d->
        \alternative {
          {
            cs8[ r a->] \stemDown bf->[ r a->] \stemNeutral |
            g8-> f-> e-> a[ r a]
          }
          {
            cs8[ r e,->] a->[ r e->] |
            a\<[ r a] a4.:8 |
          }
        }
      }
      \mBreak
      
      \section
      \repeat volta 2 {
        \mark \default
        c!4.\ff^"Con vigore"-> c-> |
        c4.-> c8 c c |
        c8[ r c,\mf] c e g |
        c4 g8 c4 c8 |
        a4.\ff^> bf^> |
        a4.^> g8 a bf |
        a8[ r c,\mf] c f a |
        c4\> c8 a4 c8 |
        \shape #'((0.0 . 0.0) (0 . 0.7) (0 . 0.7) (0 . 0)) PhrasingSlur
        bf4.\mf\( d |
        c4. bf\) |
        \stemUp a8\<[ r a] a[ r c] \stemNeutral |
        e4.\sf->( d) |
        \mBreak
        
        c8 a c c4. |
        a8 f a a4 f16( g) |
        a4 a8 c4( bf8) |
        \alternative {
          {
            a8[ r c] c4.:8
          }
          {
            a8 c c c4.:8 |
          }
        }
      }
      c4.:8\< c:8
      \section
      \mark \default
      r8\ff c8 c c4.:8 |
      c4.:8 c:8 |
      r8 d d d4.:8 |
      d4.:8 d:8 |
      \repeat percent 2 {
        r8 e4:8 r8 e4:8 |
      }
      \mBreak

      f8 a, bf c d e |
      f4.:8 f:8 |
      r8 c c c4.:8 |
      d4.:8 d:8 |
      r8 d d d4.:8 |
      e4.:8 e:8 |
      f4.:8 f:8 |
      e4.:8 e:8 |
      f4 r8  r4 f,8-> |
      a4-> r8 c4-> r8 |
      f4-> r8 r4 r8 |
      \endFermata
      \mBreak
      
      \section
      \sectionLabel "Trio"
      \repeat volta 2 {
        \key bf \major
        r4 f,8\p\( bf4 f8\) |
        a4.( ef') |
        d4.\< d |
        d4.\>( ef) |
        \shape #'((0.0 . 0.0) (0 . 0.7) (0 . 0.7) (0 . 0)) PhrasingSlur
        bf2.\!\( |
        d4. bf\) |
        f8\<[ r g] a[ r bf] |
        c8\>[ r c] c[ r bf] |
        a4.\!( gs) |
        a4 a8 a4 a8 |
        bf2.\( |
        g4. bf\) |
        \mBreak
        
        c4.\( a4 c8\) |
        bf4. bf |
        a8\<[ r ef'] ef[ r ef] |
        ef2.\> |
        \mark \default
        f,2.\p~ |
        f4. f8 a g |
        f4 d'8 d4 bf8 |
        f4 f8\( e4 f8\) |
        \override DynamicTextSpanner.style = #'none g4. fs4\cresc g8 |
        a4. a |
        a2.~ |
        a4. d4\f-> c8 |
        \mBreak
        
        bf4.-> bf-> |
        b-> b->
        c4 b8 c4 d8 |
        ef4 g,8\<\( a4\> g8\!\) |
        f8 d f bf f bf |
        d4 r8 c4. |
        \alternative {
          {
            bf4 r8\sf bf4.\<-> |
            a8\> g f f4.\!
          }
          {
            bf4\< r8 ef4.-> |
            d4\! r8 d4\sf-> r8 |
          }
        }
      }
      
  }
}


\score {
  \new Staff = "Solo horn" {
    \pieceTime
    \keyEb
    \autoPageBreaksOff

    \cornetOne
  }
  \layout { }
  \midi { }
}
