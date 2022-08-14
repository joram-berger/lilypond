%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "rhythms"

  texidoc = "
Setting the property @code{'strict-grace-spacing} makes the musical
columns for grace notes 'floating', i.e., decoupled from the non-grace
notes: first the normal notes are spaced, then the (musical columns of
the) graces are put left of the musical columns for the main notes.

"
  doctitle = "Positioning grace notes with floating space"
} % begin verbatim

\relative c'' {
  <<
    \override Score.SpacingSpanner.strict-grace-spacing = ##t
    \new Staff \new Voice {
      \afterGrace c4 { c16[ c8 c16] }
      c8[ \grace { b16 d } c8]
      c4 r
    }
    \new Staff {
      c16 c c c c c c c c4 r
    }
  >>
}
