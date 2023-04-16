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
Hairpin dynamics may be printed with a circled tip (@qq{al niente}
notation) by setting the @code{circled-tip} property of the
@code{Hairpin} object to @code{#t}.
"

  doctitle = "Printing hairpins using al niente notation"
} % begin verbatim


\relative c'' {
  \override Hairpin.circled-tip = ##t
  c2\< c\!
  c4\> c\< c2\!
}
