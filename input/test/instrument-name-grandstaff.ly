\version "2.1.29"
\header { texidoc = "@cindex Instrument Name Grandstaff
You can have a name for the whole @code{GrandStaff} in addition to 
individual @code{Staff}s. " }

\score {
  \notes
  \notes \context GrandStaff <<
    \context Staff = treble    {
      \set GrandStaff.instrument = "Violini  "
      \set Staff.instrument = " vn I" { c''4 }}
    \context Staff = bass { \set Staff.instrument = " vn II" c''4 }>>


\paper {
raggedright = ##t
\context { \GrandStaffContext \consists "Instrument_name_engraver" }
}}

