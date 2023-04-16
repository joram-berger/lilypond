%% DO NOT EDIT this file manually; it was automatically
%% generated from the LilyPond Snippet Repository
%% (http://lsr.di.unimi.it).
%%
%% Make any changes in the LSR itself, or in
%% `Documentation/snippets/new/`, then run
%% `scripts/auxiliar/makelsr.pl`.
%%
%% This file is in the public domain.

\version "2.24.0"

\header {
  lsrtags = "staff-notation, syntax-and-expressions, tweaks-and-overrides"

  texidoc = "
For @code{TrillSpanner}, the @code{minimum-length} property becomes
effective only if the @code{set-spacing-rods} procedure is called
explicitly.

To do this, the @code{springs-and-rods} property should be set to
@code{ly:spanner::set-spacing-rods}.
"

  doctitle = "Extending a TrillSpanner"
} % begin verbatim


\relative c' {
  \key c\minor
  \time 2/4
  c16( as') c,-. des-.
  \once\override TrillSpanner.minimum-length = #15
  \once\override TrillSpanner.springs-and-rods = #ly:spanner::set-spacing-rods
  \afterGrace es4
  \startTrillSpan { d16[( \stopTrillSpan es)] }
  c( c' g es c g' es d
  \hideNotes
  c8)
}
