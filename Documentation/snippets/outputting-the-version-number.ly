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
  lsrtags = "really-simple, scheme-language, text, titles"

  texidoc = "
It is possible to print the version number of LilyPond in markup.
"

  doctitle = "Outputting the version number"
} % begin verbatim


\markup { Processed with LilyPond version #(lilypond-version) }
