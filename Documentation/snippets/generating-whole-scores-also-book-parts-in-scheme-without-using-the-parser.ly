%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.12"

\header {
  lsrtags = "automatic-notation, really-cool, scheme-language"

  texidoc = "
A LilyPond score internally is just a Scheme expression, generated by
the LilyPond parser.  Using Scheme, one can also automatically generate
a score without an input file.  If you have the music expression in
Scheme, a score can be generated by simply calling

@verbatim
(scorify-music music)
@end verbatim

on your music.  This generates a score object, for which you can then
set a custom layout block with

@verbatim
(let* ((layout (ly:output-def-clone $defaultlayout)))
   ; modify the layout here, then assign it:
   (ly:score-add-output-def! score layout)
  )
@end verbatim

Finally, all you have to do it to pass this score to LilyPond for
typesetting.  This snippet defines functions @code{(add-score score)},
@code{(add-text text)}, and @code{(add-music music)} to pass a complete
score, some markup, or some music to LilyPond for typesetting.

This snippet also works for typesetting scores inside a
@code{\\book @{...@}} block as well as top-level scores.  To achieve
this, each score scheduled for typesetting is appended to the list of
top-level scores, and the top-level book handler (which is a Scheme
function called to process a book once a @code{\\book@{...@}} block is
closed) is modified to insert all collected scores so far to the book.

"
  doctitle = "Generating whole scores (also book parts) in scheme without using the parser"
} % begin verbatim

%%

#(define-public (add-score score)
   (ly:parser-define! 'toplevel-scores
                      (cons score (ly:parser-lookup 'toplevel-scores))))

#(define-public (add-text text)
  (add-score (list text)))

#(define-public (add-music music)
  (collect-music-aux (lambda (score)
		       (add-score score))
		     music))

#(define-public (toplevel-book-handler book)
   (map (lambda (score)
          (ly:book-add-score! book score))
        (reverse! (ly:parser-lookup 'toplevel-scores)))
   (ly:parser-define! 'toplevel-scores (list))
   (print-book-with-defaults book))

#(define-public (book-score-handler book score)
   (add-score score))

#(define-public (book-text-handler book text)
   (add-text text))

#(define-public (book-music-handler book music)
   (add-music music))

%%%


%% Just some example score to show how to use these functions:
#(define add-one-note-score #f)
#(let ((pitch 0))
  (set! add-one-note-score
        (lambda (parser)
          (let* ((music (make-music 'EventChord
                          'elements (list (make-music 'NoteEvent
                                            'duration (ly:make-duration 2 0 1/1)
                                            'pitch (ly:make-pitch 0 pitch 0)))))
                 (score (scorify-music music))
                 (layout (ly:output-def-clone $defaultlayout))
                 (note-name (case pitch
                              ((0) "do")
                              ((1) "ré")
                              ((2) "mi")
                              ((3) "fa")
                              ((4) "sol")
                              ((5) "la")
                              ((6) "si")
                              (else "huh")))
                 (title (markup #:large #:line ("Score with a" note-name))))
            (ly:score-add-output-def! score layout)
            (add-text title)
            (add-score score))
            (set! pitch (modulo (1+ pitch) 7)))))

oneNoteScore =
#(define-music-function () ()
   (add-one-note-score (*parser*))
   (make-music 'Music 'void #t))

%%%

\book {
  \oneNoteScore
}


\book {
  \oneNoteScore
  \oneNoteScore
}

% Top-level scores are also handled correctly.
\oneNoteScore
\oneNoteScore
