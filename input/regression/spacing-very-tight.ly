\version "1.3.148"
\header {
 When tightly spaced, hinterfleisch -> 0.
 Stems may touch the bar lines, opposite stems may touch eachother.
 We need a mininum of about a note-width/interline space in these
 situations, so that in tightly spaced music all vertical lines
 are about equally spaced.
}
\score {
	\notes \relative c''{ 
		r1 e4 f, e' f,
	}
	\paper { 
		linewidth = 25.0 \mm
		indent = 0.0\mm
	}
}
