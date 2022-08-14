%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "editorial-annotations, really-simple, simultaneous-notes, specific-notation, tweaks-and-overrides"

  texidoc = "
Individual note heads in a chord can be modified with the
@code{\\tweak} command inside a chord, by altering the @code{font-size}
property.

Inside the chord (within the brackets @code{< >}), before the note to
be altered, place the @code{\\tweak} command, followed by
@code{font-size} and define the proper size like @code{#-2} (a tiny
note head).

"
  doctitle = "Changing a single note's size in a chord"
} % begin verbatim

\relative c' {
  <\tweak font-size #+2 c e g c
   \tweak font-size #-2 e>1
   ^\markup { A tiny e }_\markup { A big c }
}
