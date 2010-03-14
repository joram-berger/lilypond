%% Do not edit this file; it is automatically
%% generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.13.10"

\header {
  lsrtags = "fretted-strings"

%% Translation of GIT committish: 45fc8488655f9ea122d1ec6e3328892618bd6971
  texidoces = "

Se pueden añadir diagramas de posiciones predefinidas para
instrumentos nuevos además de los estándar que se usan para la
guitarra.  Este archivo muestra cómo se hace, definiendo una afinación
nueva y unas cuantas posiciones para el cuatro venezolano.

Este archivo también muestra cómo se pueden incluir las digitaciones
en los acordes que se usan como puntos de referencia para la búsqueda
de acordes en la tabla, y mostrarse en el diagrama de posiciones y la
tablatura @code{TabStaff}, pero no en la música.

Estas posiciones no se pueden transportar porque contienen información
de las cuerdas.  Hay planes para corregir esto en un futuro.

"
  doctitlees = "Definición de posiciones predefinidas para otros instrumentos"

%% Translation of GIT committish: 33f623301a41fcc53efadf96bca1c72834763415
  texidocde = "
Vordefinierte Bunddiagramme können für neue Instrumente hinzugefügt werden
neben denen, die schon für die Gitarre definiert sind.  Dieses Schnipsel
zeigt, wie man eine neue Saitenstimmung definiert und dann eigene vordefinierte
Bunddiagramme bestimmt.  Das Beispiel ist für das venezualische Cuatro.

Dieses Schnipsel zeigt auch, wie Fingersatz in die Akkorde eingebunden
werden kann, um als Referenzpunkt für die Akkordauswahl benutzt werden
kann.  Dieser Fingersatz wird im Bunddiagramm und in der Tabulatur,
aber nicht in den Noten angezeigt.

Diese Bunddiagramme sind nicht transponierbar, weil sie Saiteninformationen
enthalten.  Das soll in der Zukunft verbessert werden.

"
  doctitlede = "Eigene vordefinierte Bunddiagramme für andere Instrumente erstellen"
%% Translation of GIT committish: d96023d8792c8af202c7cb8508010c0d3648899d

  texidocfr = "
La liste des diagrammes standards prédéfinis pour la guitare peut être
 augmentée d'autres définitions spécifiques à d'autres instruments.
Voici comment définir un nouvel accordage ainsi que quelques diagrammes
prédéfinis pour le @qq{cuatro vénézuélien}.

Cet exemple illustre aussi la manière d'ajouter des doigtés aux
accords ; ils serviront de référence pour la boucle d'accord et seront
indiqués dans les diagrammes et le @code{TabStaff}, mais pas dans la musique.

Ces diagrammes ne peuvent pas être transposés, dans la mesure où ils
contiennent des informations sur les cordes.  Ceci est amené à évoluer.

"
  doctitlefr = "Création de diagrammes de fret prédéfinis pour d'autres instruments"


  texidoc = "
Predefined fret diagrams can be added for new instruments in addition
to the standards used for guitar.  This file shows how this is done by
defining a new string-tuning and a few predefined fretboards for the
Venezuelan cuatro.

This file also shows how fingerings can be included in the chords used
as reference points for the chord lookup, and displayed in  the fret
diagram and the @code{TabStaff}, but not the music.


These fretboards are not transposable because they contain string
information.  This is planned to be corrected in the future.

"
  doctitle = "Defining predefined fretboards for other instruments"
} % begin verbatim

% add FretBoards for the Cuatro
%   Note: This section could be put into a separate file
%      predefined-cuatro-fretboards.ly
%      and \included into each of your compositions

cuatroTuning = #'(11 18 14 9)

dSix = { <a\4 b\1 d\3 fis\2> }
dMajor = { <a\4 d\1 d\3 fis \2> }
aMajSeven = { <a\4 cis\1 e\3 g\2> }
dMajSeven = { <a\4 c\1 d\3 fis\2> }
gMajor = { <b\4 b\1 d\3 g\2> }

\storePredefinedDiagram \dSix
                        #cuatroTuning
                        #"o;o;o;o;"
\storePredefinedDiagram \dMajor
                        #cuatroTuning
                        #"o;o;o;3-3;"
\storePredefinedDiagram \aMajSeven
                        #cuatroTuning
                        #"o;2-2;1-1;2-3;"
\storePredefinedDiagram \dMajSeven
                        #cuatroTuning
                        #"o;o;o;1-1;"
\storePredefinedDiagram \gMajor
                        #cuatroTuning
                        #"2-2;o;1-1;o;"

% end of potential include file /predefined-cuatro-fretboards.ly


#(set-global-staff-size 16)

primerosNames = \chordmode {
  d:6 d a:maj7 d:maj7
  g
}
primeros = {
  \dSix \dMajor \aMajSeven \dMajSeven
  \gMajor
}

\score {
  <<
    \new ChordNames {
      \set chordChanges = ##t
      \primerosNames
    }

    \new Staff {
      \new Voice \with {
        \remove "New_fingering_engraver"
      }
      \relative c'' {
        \primeros
      }
    }

    \new FretBoards {
      \set stringTunings = #cuatroTuning
      \override FretBoard
        #'(fret-diagram-details string-count) = #'4
      \override FretBoard
        #'(fret-diagram-details finger-code) = #'in-dot
      \primeros
    }

    \new TabStaff \relative c'' {
      \set TabStaff.stringTunings = #cuatroTuning
      \primeros
    }

  >>

  \layout {
    \context {
      \Score
      \override SpacingSpanner
        #'base-shortest-duration = #(ly:make-moment 1 16)
    }
  }
  \midi { }
}
