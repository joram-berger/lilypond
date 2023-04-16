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
  lsrtags = "expressive-marks, scheme-language, tweaks-and-overrides"

  texidoc = "
Using @code{\\override Slur.positions} it is possible to set the
vertical position of the start and end points of a slur to absolute
values (or rather, forcing LilyPond's slur algorithm to consider these
values as desired).  In many cases, this means a lot of trial and error
until good values are found.  You probably have tried the
@code{\\offset} command next just to find out that it doesn't work for
slurs, emitting a warning instead.

The code in this snippet allows you to tweak the vertical start and end
positions by specifying @emph{relative} changes, similar to
@code{\\offset}.

Syntax: @code{\\offsetPositions #'(@var{dy1} . @var{dy2})}
"

  doctitle = "Adjusting slur positions vertically"
} % begin verbatim


offsetPositions =
#(define-music-function (offsets) (number-pair?)
  #{
     \once \override Slur.control-points =
       #(lambda (grob)
          (match-let ((((_ . y1) _ _ (_ . y2))
                       (ly:slur::calc-control-points grob))
                      ((off1 . off2) offsets))
            (set! (ly:grob-property grob 'positions)
                  (cons (+ y1 off1) (+ y2 off2)))
            (ly:slur::calc-control-points grob)))
  #})

\relative c'' {
  c4(^"default" c, d2)
  \offsetPositions #'(0 . 1)
  c'4(^"(0 . 1)" c, d2)
  \offsetPositions #'(0 . 2)
  c'4(^"(0 . 2)" c, d2)
  \bar "||"
  g4(^"default" a d'2)
  \offsetPositions #'(1 . 0)
  g,,4(^"(1 . 0)" a d'2)
  \offsetPositions #'(2 . 0)
  g,,4(^"(2 . 0)" a d'2)
}
