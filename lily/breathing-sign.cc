/*
  breathing_sign.cc -- implement Breathing_sign

  Copyright (C) 1999 Michael Krause

  written for the GNU LilyPond music typesetter

  TODO: --> see breathing-sign-engraver.cc

*/

#include "staff-symbol-referencer.hh"
#include "directional-element-interface.hh"
#include "breathing-sign.hh"
#include "string.hh"
#include "molecule.hh"
#include "paper-def.hh"
#include "lookup.hh"

#include "dimensions.hh"
#include "direction.hh"

MAKE_SCHEME_CALLBACK (Breathing_sign,brew_molecule,1);
SCM 
Breathing_sign::brew_molecule (SCM smob)
{
  Grob * me = unsmob_grob (smob);
  Real space = Staff_symbol_referencer::staff_space (me);

  // todo: cfg'able.
  Interval i1 (0, space / 6), i2 (-space / 2, space / 2);
  Box b (i1, i2);

  return Lookup::filledbox (b).smobbed_copy ();
}

/*
  Simplistic caesura.
 */
MAKE_SCHEME_CALLBACK (Breathing_sign,railtracks,1);
SCM 
Breathing_sign::railtracks (SCM smob)
{
  Grob * me = unsmob_grob (smob);
  Real space = Staff_symbol_referencer::staff_space (me);
  Real th = me->get_paper ()->get_var ("linethickness");
  SCM lt =  me->get_grob_property ("thickness");
  if (gh_number_p (lt))
    th *= gh_scm2double (lt);
  
  Offset x1 (0, -space);
  Offset x2 (space / 3, space);
  Molecule l1 (Lookup::line (th, x1, x2));
  Molecule l2 (l1);
  l2.translate_axis (space *0.6 , X_AXIS);
  l1.add_molecule (l2);
  return l1.smobbed_copy();
}


MAKE_SCHEME_CALLBACK (Breathing_sign,offset_callback,2);
SCM
Breathing_sign::offset_callback (SCM element_smob, SCM)
{
  Grob *me = unsmob_grob (element_smob);
  
  Direction d = Directional_element_interface::get (me);
  if (!d)
    {
      d = UP;
      Directional_element_interface::set (me, d);
    }

  Real inter_f = Staff_symbol_referencer::staff_space (me)/2;
  int sz = Staff_symbol_referencer::line_count (me)-1;
  return gh_double2scm (inter_f * sz * d);
}


ADD_INTERFACE(Breathing_sign, "breathing-sign-interface",
	      "A breathing sign.",
	      "direction");
