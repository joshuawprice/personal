\version "2.26.0"

\header {
  title = "Happy Birthday"

  % Remove default LilyPond tagline
  tagline = ##f
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
  #(set-paper-size "a4")
  ragged-right = ##f
  bookTitleMarkup = \markup \center-column {
    \fill-line {
      \bold \fontsize #4 \fromproperty #'header:title
    }
    \fill-line {
      \fromproperty #'header:instrument
      \fromproperty #'header:subsubtitle
      \fromproperty #'header:composer
    }
  }
  indent = #0
}

mBreak = {
  \break
}
