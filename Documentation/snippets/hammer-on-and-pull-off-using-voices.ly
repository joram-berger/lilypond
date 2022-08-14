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
The arc of hammer-on and pull-off is upwards in voices one and three
and downwards in voices two and four:

"
  doctitle = "Hammer on and pull off using voices"
} % begin verbatim

\new TabStaff {
  \relative c' {
    << { \voiceOne g2( a) }
    \\ { \voiceTwo a,( b) }
    >> \oneVoice
  }
}
