%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "specific-notation, winds"

  texidoc = "
The following music shows all of the woodwind diagrams currently
defined in LilyPond.

"
  doctitle = "Woodwind diagrams listing"
} % begin verbatim

\layout {
  indent = 0
}

\relative c' {
  \textLengthOn
  c1^
  \markup {
    \center-column {
      'tin-whistle
      " "
       \woodwind-diagram
                  #'tin-whistle
                  #'()
    }
  }

  c1^
  \markup {
    \center-column {
      'piccolo
      " "
       \woodwind-diagram
                  #'piccolo
                  #'()
    }
  }

  c1^
  \markup {
    \center-column {
       'flute
       " "
       \woodwind-diagram
          #'flute
          #'()
    }
  }
  c1^\markup {
    \center-column {
      'oboe
      " "
      \woodwind-diagram
        #'oboe
        #'()
    }
  }

  c1^\markup {
    \center-column {
      'clarinet
      " "
      \woodwind-diagram
        #'clarinet
        #'()
    }
  }

  c1^\markup {
    \center-column {
      'bass-clarinet
      " "
      \woodwind-diagram
        #'bass-clarinet
        #'()
    }
  }

  c1^\markup {
    \center-column {
      'saxophone
      " "
      \woodwind-diagram
        #'saxophone
        #'()
    }
  }

  c1^\markup {
    \center-column {
      'bassoon
      " "
      \woodwind-diagram
        #'bassoon
        #'()
    }
  }

  c1^\markup {
    \center-column {
      'contrabassoon
      " "
      \woodwind-diagram
        #'contrabassoon
        #'()
    }
  }
}
