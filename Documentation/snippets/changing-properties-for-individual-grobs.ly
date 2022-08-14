%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "really-cool, scheme-language, tweaks-and-overrides"

  texidoc = "
The @code{\\applyOutput} command allows the tuning of any layout
object, in any context. It requires a Scheme function with three
arguments.

"
  doctitle = "Changing properties for individual grobs"
} % begin verbatim

#(define (mc-squared grob grob-origin context)
   (let ((sp (ly:grob-property grob 'staff-position)))
     (ly:grob-set-property!
      grob 'stencil
      (grob-interpret-markup grob
			     #{ \markup \lower #0.5
				#(case sp
				   ((-5) "m")
				   ((-3) "c ")
				   ((-2) #{ \markup \teeny \bold 2 #})
				   (else "bla")) #}))))

\relative c' {
  <d f g b>2
  \applyOutput Voice.NoteHead #mc-squared
  <d f g b>2
}
