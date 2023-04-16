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
  lsrtags = "pitches, tweaks-and-overrides"

  texidoc = "
The following example shows how to force a natural sign before an
accidental.
"

  doctitle = "Force a cancellation natural before accidentals"
} % begin verbatim


\relative c' {
  \key es \major
  bes c des
  \tweak Accidental.restore-first ##t
  eis
}
