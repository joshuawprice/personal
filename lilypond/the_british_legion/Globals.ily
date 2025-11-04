\version "2.24.1"
\language "english"

\header {
  title = "THE BRITISH LEGION"
  subtitle = "The Official March of the British Legion"
  subsubtitle = \markup { \raise #1.5 { "March" } }
  composer = \markup { \raise #1.5 { "T. Bidgood" } }

  % Remove default LilyPond tagline
  tagline = ##f
  %copyright = "After Hawkes & Sons, 1922"
  %ismn = "Re-engraved 2025 by J. Price"
  %copyright = "© Copyright 1922 by Hawkes & Sons (London) Ltd"
  %ismn = "ISMN: M-050-00756-2"
  %publisher = "Boosey & Hawkes Music Publishers Ltd., London"
  %rights = "All rights reserved"

}

\layout {
  \context {
    \Score
    \remove "Bar_number_engraver"
  }
  \context {
    \Voice
    \consists "Melody_engraver"
  }
}

\paper {
  #(set-paper-size "a4" 'landscape)
  ragged-last-bottom = ##f
  bookTitleMarkup = \markup \center-column {
    \fill-line {
      \fromproperty #'header:subtitle
    }
    \fill-line {
      \pad-around #1 \bold \fontsize #7 \fromproperty #'header:title
    }
    \fill-line {
      \fromproperty #'header:instrument
      \fromproperty #'header:subsubtitle
      \fromproperty #'header:composer
    }
  }
  oddFooterMarkup = \markup \center-column {
    \fill-line {
      \fromproperty #'header:copyright
      \fromproperty #'header:ismn
    }
    \fill-line {
      \fromproperty #'header:publisher
      \fromproperty #'header:rights
    }
  }
  indent = #8
}

pieceTime = {
  % For the midi playback speed to be reasonable.
  \set Score.tempoHideNote = ##t
  \tempo 4 = 180

  \time 6/8
}

keyBb = {
  \key bf \major
  \transposition bf
}

keyEb = {
  \key f \major
  \transposition ef
}

endFermata = {
  \once \override Score.RehearsalMark.break-visibility = #begin-of-line-invisible
  \mark \markup \smaller \fermata
}

mBreak = {
  \break
}
