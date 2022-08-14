%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "expressive-marks, symbols-and-glyphs, tweaks-and-overrides"

  texidoc = "
A caesura is sometimes denoted by a double @qq{railtracks} breath mark
with a fermata sign positioned above. This snippet shows an optically
pleasing combination of railtracks and fermata.

"
  doctitle = "Caesura (\"railtracks\") with fermata"
} % begin verbatim

\relative c'' {
  c2.
  % construct the symbol
  \override BreathingSign.text = \markup {
    \override #'(direction . 1)
    \override #'(baseline-skip . 1.8)
    \dir-column {
      \translate #'(0.155 . 0)
        \center-align \musicglyph "scripts.caesura.curved"
      \center-align \musicglyph "scripts.ufermata"
    }
  }
  \breathe c4
  % set the breathe mark back to normal
  \revert BreathingSign.text
  c2. \breathe c4
  \bar "|."
}
