% Toplevel initialisation file. 

#(define-public point-and-click #f)
#(define-public midi-debug #f)


\version "1.9.8"

\include "declarations-init.ly"


#(ly:set-option 'new-relative)
#(ly:set-point-and-click #f)

\maininput

#(if (and (ly:get-option 'old-relative)
      (not (ly:get-option 'old-relative-used)))
  (ly:warn (string-append
	    "\n"
	    input-file-name ": old relative compatibility was not used.")))


#(if (ly:get-option 'verbose)
  (begin
   (gc)
   (write (gc-stats) (current-error-port))
   (flush-all-ports)))

