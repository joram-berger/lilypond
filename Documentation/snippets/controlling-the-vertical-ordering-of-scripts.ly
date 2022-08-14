%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "expressive-marks, tweaks-and-overrides"

  texidoc = "
The vertical ordering of scripts is controlled with the
@code{'script-priority} property. The lower this number, the closer it
will be put to the note. In this example, the @code{TextScript} (the
@emph{sharp} symbol) first has the lowest priority, so it is put lowest
in the first example. In the second, the @emph{prall trill} (the
@code{Script}) has the lowest, so it is on the inside. When two objects
have the same priority, the order in which they are entered determines
which one comes first.

"
  doctitle = "Controlling the vertical ordering of scripts"
} % begin verbatim

\relative c''' {
  \once \override TextScript.script-priority = #-100
  a2^\prall^\markup { \sharp }

  \once \override Script.script-priority = #-100
  a2^\prall^\markup { \sharp }
}
