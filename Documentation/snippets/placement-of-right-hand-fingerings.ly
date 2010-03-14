%% Do not edit this file; it is automatically
%% generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.13.10"

\header {
  lsrtags = "fretted-strings"

%% Translation of GIT committish: 45fc8488655f9ea122d1ec6e3328892618bd6971
  texidoces = "
Es posible ejercer un mayor control sobre la colocación de las
digitaciones de la mano derecha estableciendo el valor de una
propiedad específica, como se muestra en el ejemplo siguiente.  Nota:
se debe usar una construcción de acorde.

"
  doctitlees = "Posicionamiento de digitaciones de mano derecha"

%% Translation of GIT committish: d96023d8792c8af202c7cb8508010c0d3648899d
  texidocde = "
Man kann die Positionierung von Fingersatz der rechten Hand besser
kontrollieren, wenn eine bestimmte Eigenschaft gesetzt wird, wie
das folgende Beispiel zeigt:

"
  doctitlede = "Positionierung von Fingersatz der rechten Hand"
%% Translation of GIT committish: 3f880f886831b8c72c9e944b3872458c30c6c839

  texidocfr = "
Vous disposez d'une propriété spécifique qui permet de contrôler plus
finement le positionnement des doigtés main droite, comme l'indique
l'exemple suivant.

"
  doctitlefr = "Positionnement des doigtés main droite"


  texidoc = "
It is possible to exercise greater control over the placement of
right-hand fingerings by setting a specific property, as demonstrated
in the following example. Note: you must use a chord construct

"
  doctitle = "Placement of right-hand fingerings"
} % begin verbatim

#(define RH rightHandFinger)

\relative c {
  \clef "treble_8"

  \set strokeFingerOrientations = #'(up down)
  <c-\RH #1 e-\RH #2 g-\RH #3 c-\RH #4 >4

  \set strokeFingerOrientations = #'(up right down)
  <c-\RH #1 e-\RH #2 g-\RH #3 c-\RH #4 >4

  \set strokeFingerOrientations = #'(left)
  <c-\RH #1 e-\RH #2 g-\RH #3 c-\RH #4 >2
}

