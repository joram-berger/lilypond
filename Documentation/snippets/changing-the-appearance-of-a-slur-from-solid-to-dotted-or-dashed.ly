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
  lsrtags = "connecting-notes, editorial-annotations, expressive-marks, really-simple"

  texidoc = "
The appearance of slurs may be changed from solid to dotted or dashed.
"

  doctitle = "Changing the appearance of a slur from solid to dotted or dashed"
} % begin verbatim


\relative c' {
  c4( d e c)
  \slurDotted
  c4( d e c)
  \slurSolid
  c4( d e c)
  \slurDashed
  c4( d e c)
  \slurSolid
  c4( d e c)
}
