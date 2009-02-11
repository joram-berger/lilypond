%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.12.0"

\header {
  lsrtags = "text, vocal-music, contexts-and-engravers, template"

  texidoces = "
Esta plantilla es, básicamente, la misma que la sencilla plantilla
\"Conjunto vocal\", excepto que aquí todas las líneas de letra se
colocan utilizando @code{alignAboveContext} y
@code{alignBelowContext}.

"
  doctitlees = "Plantilla para conjunto vocal con letras alineadas encima y debajo de los pentagramas"
  
  texidocde = "
In diesem Beispiel werden die Texte mit den Befehlen 
@code{alignAboveContext} und @code{alignBelowContext}
über und unter dem System angeordnet.
"

  texidocja = "
このテンプレートは基本的に単純な \"合唱\" テンプレートと同じですが、歌詞が 
@code{alignAboveContext} と @code{alignBelowContext} を用いて配置されています。
"

  texidoc = "
This template is basically the same as the simple \"Vocal ensemble\"
template, with the exception that here all the lyrics lines are placed
using @code{alignAboveContext} and @code{alignBelowContext}.

"
  doctitle = "Vocal ensemble template with lyrics aligned below and above the staves"
} % begin verbatim

global = {
  \key c \major
  \time 4/4
}

sopMusic = \relative c'' {
  c4 c c8[( b)] c4
}
sopWords = \lyricmode {
  hi hi hi hi
}

altoMusic = \relative c' {
  e4 f d e
}
altoWords = \lyricmode {
  ha ha ha ha
}

tenorMusic = \relative c' {
  g4 a f g
}
tenorWords = \lyricmode {
  hu hu hu hu
}

bassMusic = \relative c {
  c4 c g c
}
bassWords = \lyricmode {
  ho ho ho ho
}

\score {
  \new ChoirStaff <<
    \new Staff = women <<
      \new Voice = "sopranos" { \voiceOne << \global \sopMusic >> }
      \new Voice = "altos" { \voiceTwo << \global \altoMusic >> }
    >>
    \new Lyrics \with { alignAboveContext = women } \lyricsto sopranos \sopWords
    \new Lyrics \with { alignBelowContext = women } \lyricsto altos \altoWords
    % we could remove the line about this with the line below, since we want
    % the alto lyrics to be below the alto Voice anyway.
    % \new Lyrics \lyricsto altos \altoWords
    
    \new Staff = men <<
      \clef bass
      \new Voice = "tenors" { \voiceOne << \global \tenorMusic >> }
      \new Voice = "basses" { \voiceTwo << \global \bassMusic >> }
    >>
    \new Lyrics \with { alignAboveContext = men } \lyricsto tenors \tenorWords
    \new Lyrics \with { alignBelowContext = men } \lyricsto basses \bassWords
    % again, we could replace the line above this with the line below.
    % \new Lyrics \lyricsto basses \bassWords
  >>
  \layout {
    \context {
      % a little smaller so lyrics
      % can be closer to the staff
      \Staff
      \override VerticalAxisGroup #'minimum-Y-extent = #'(-3 . 3)
    }
  }
}
