\version "2.23.7"

#(ly:set-option 'warning-as-error #t)

\header {
  texidoc = "This piece consists of three consecutive sections using
@code{\\repeat segno 1}.  Because of the count, no repeat notation
should appear."
}

piece = \fixed c' {
  \repeat segno 1 f1
  \repeat segno 1 g1
  \repeat segno 1 { a1 \alternative { b1 } }
}

\new Score {
  \new Staff \with { instrumentName = "segno" } { \piece }
}

\new Score \with { \omit RehearsalMark } {
  \new Staff \with { instrumentName = "unfolded" } { \unfoldRepeats \piece }
}
