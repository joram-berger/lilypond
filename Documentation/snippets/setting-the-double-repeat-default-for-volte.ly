%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "repeats"

  texidoc = "
There are three different styles of double repeats for volte, that can
be set using @code{doubleRepeatBarType}.

"
  doctitle = "Setting the double repeat default for volte"
} % begin verbatim

\relative c'' {
  \repeat volta 2 { c1 }
  \set Score.doubleRepeatBarType = #":..:"
  \repeat volta 2 { c1 }
  \set Score.doubleRepeatBarType = #":|.|:"
  \repeat volta 2 { c1 }
  \set Score.doubleRepeatBarType = #":|.:"
  \repeat volta 2 { c1 }
}
