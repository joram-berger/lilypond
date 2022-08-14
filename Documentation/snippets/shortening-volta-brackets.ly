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
By default, the volta brackets will be drawn over all of the
alternative music, but it is possible to shorten them by setting
@code{voltaSpannerDuration}.  In the next example, the bracket only
lasts one measure, which is a duration of 3/4.

"
  doctitle = "Shortening volta brackets"
} % begin verbatim

\relative c'' {
  \time 3/4
  c4 c c
  \set Score.voltaSpannerDuration = #(ly:make-moment 3/4)
  \repeat volta 5 { d4 d d }
  \alternative {
    {
      e4 e e
      f4 f f
    }
    { g4 g g }
  }
}
