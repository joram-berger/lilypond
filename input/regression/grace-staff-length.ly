\version "1.7.18"
\header{
texidoc = "Stripped version of trip.ly.  Staffs should be of correct length."
}
\score{
  \context PianoStaff \notes \relative c'' <
    \context Staff = treble {
       r1
       r1
       \bar "|."
    }
    \context Staff = bass {
      r1
      \context Staff {
	\grace { c16 } c1
      }
    }
  > 
  \paper { }
}

