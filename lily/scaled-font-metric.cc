/*   
     scaled-font-metric.cc -- declare Scaled_font_metric
  
  source file of the GNU LilyPond music typesetter
  
  (c) 1999--2001 Han-Wen Nienhuys <hanwen@cs.uu.nl>
  
 */

#include "scaled-font-metric.hh"
#include "string.hh"
#include "molecule.hh"


Scaled_font_metric::Scaled_font_metric (Font_metric* m, Real magn)
{
  magnification_f_ = magn;
  SCM desc = m->description_;

  Real total_mag = magn * gh_scm2double (gh_cdr (desc));
  description_ = gh_cons (gh_car (desc), gh_double2scm (total_mag));
  orig_l_ = m;
}

SCM
Scaled_font_metric::make_scaled_font_metric (Font_metric*m, Real s)
{
  Scaled_font_metric *sfm = new Scaled_font_metric (m,s);
  return sfm->self_scm ();
}

Molecule
Scaled_font_metric::find_by_name (String s) const
{
  Molecule m = orig_l_->find_by_name (s);
  Box b = m.extent_box ();
  b.scale (magnification_f_);
  Molecule q(b,fontify_atom ((Font_metric*) this, m.get_expr ()));

  return q ;
}

Box 
Scaled_font_metric::get_char (int i) const
{
  Box b = orig_l_->get_char (i);
  b.scale (magnification_f_);
  return b;  
}

Box
Scaled_font_metric::text_dimension (String t) const
{
  Box b (orig_l_->text_dimension (t));

  b.scale (magnification_f_);
  return b;
}
