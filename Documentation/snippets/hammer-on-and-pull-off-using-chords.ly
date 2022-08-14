%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "editorial-annotations, fretted-strings"

  texidoc = "
When using hammer-on or pull-off with chorded notes, only a single arc
is drawn. However @qq{double arcs} are possible by setting the
@code{doubleSlurs} property to @code{#t}.

"
  doctitle = "Hammer on and pull off using chords"
} % begin verbatim

\new TabStaff {
  \relative c' {
    % chord hammer-on and pull-off
    \set doubleSlurs = ##t
    <g' b>8( <a c> <g b>)
  }
}
