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
  lsrtags = "expressive-marks"

  texidoc = "
Text style dynamic changes (such as @emph{cresc.} and @emph{dim.}) are
printed with a dashed line showing their extent.  This line can be
suppressed in the following way:
"

  doctitle = "Hiding the extender line for text dynamics"
} % begin verbatim


\relative c'' {
  \override DynamicTextSpanner.style = #'none
  \crescTextCresc
  c1\< | d | b | c\!
}
