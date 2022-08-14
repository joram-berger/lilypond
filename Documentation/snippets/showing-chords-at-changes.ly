%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "chords"

  texidoc = "
By default, every chord entered is printed; this behavior can be
modified so that chord names are printed only at the start of lines and
when the chord changes.

"
  doctitle = "Showing chords at changes"
} % begin verbatim

harmonies = \chordmode {
  c1:m c:m \break c:m c:m d
}

<<
  \new ChordNames {
    \set chordChanges = ##t
    \harmonies
  }
  \new Staff {
    \relative c' { \harmonies }
  }
>>
