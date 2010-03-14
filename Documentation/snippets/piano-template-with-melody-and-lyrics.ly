%% Do not edit this file; it is automatically
%% generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.13.10"

\header {
  lsrtags = "vocal-music, keyboards, template"

%% Translation of GIT committish: 45fc8488655f9ea122d1ec6e3328892618bd6971
  texidoces = "
He aquí el típico formato dde una canción: un pentagrama con la
melodía y la letra, y el acompañamiento de piano por debajo.

"
  doctitlees = "Plantilla de piano con melodía y letra"

%% Translation of GIT committish: 06d99c3c9ad1c3472277b4eafd7761c4aadb84ae
  texidocja = "
これは一般的な歌曲のフォーマットです: 旋律と歌詞を持つ譜表と、その下にピアノ伴奏譜があります。
"
%% Translation of GIT committish: d96023d8792c8af202c7cb8508010c0d3648899d
  texidocde = "
Das nächste Beispiel ist typisch für ein Lied: Im oberen System die
Melodie mit Text, darunter Klavierbegleitung.
"

  doctitlede = "Vorlage für Klavier und Gesangsstimme"

%% Translation of GIT committish: 9ba35398048fdf1ca8c83679c7c144b1fd48e75b
  texidocfr = "
Il s'agit du format classique pour le chant : une portée pour la mélodie
et les paroles au-dessus de l'accompagnement au piano.

"
  doctitlefr = "Piano mélodie et paroles"

  texidoc = "
Here is a typical song format: one staff with the melody and lyrics,
with piano accompaniment underneath.

"
  doctitle = "Piano template with melody and lyrics"
} % begin verbatim

melody = \relative c'' {
  \clef treble
  \key c \major
  \time 4/4

  a b c d
}

text = \lyricmode {
  Aaa Bee Cee Dee
}

upper = \relative c'' {
  \clef treble
  \key c \major
  \time 4/4

  a4 b c d
}

lower = \relative c {
  \clef bass
  \key c \major
  \time 4/4

  a2 c
}

\score {
  <<
    \new Voice = "mel" { \autoBeamOff \melody }
    \new Lyrics \lyricsto mel \text
    \new PianoStaff <<
      \new Staff = "upper" \upper
      \new Staff = "lower" \lower
    >>
  >>
  \layout {
    \context { \RemoveEmptyStaffContext }
  }
  \midi { }
}

