/*
  pango-select.cc --  implement lily font selection for Pango_fonts.

  source file of the GNU LilyPond music typesetter

  (c) 2004 Han-Wen Nienhuys <hanwen@xs4all.nl>

*/
#include <math.h>

#include "all-font-metrics.hh"
#include "output-def.hh"
#include "pango-font.hh"

Font_metric *
select_pango_font (Output_def *layout, SCM chain)
{
  SCM name = ly_chain_assoc (ly_symbol2scm ("font-name"), chain);

  PangoFontDescription *description = 0;
  if (scm_is_pair (name) && scm_is_string (scm_cdr (name)))
    {
      String name_str = ly_scm2string (scm_cdr (name));
      description = pango_font_description_from_string (name_str.to_str0 ());
      
      
      Real step = robust_scm2double (ly_symbol2scm ("font-size"), 0.0);
      Real size = layout->get_dimension (ly_symbol2scm ("text-font-size"))
	* pow (2.0, step / 6.0);
      pango_font_description_set_size (description,
				       gint (size * PANGO_SCALE));
    }
  else
    {
      SCM family = ly_chain_assoc_get (ly_symbol2scm ("font-family"), chain,
				       SCM_BOOL_F);
      SCM variant = ly_chain_assoc_get (ly_symbol2scm ("font-shape"), chain,
					SCM_BOOL_F);
	
      SCM style = ly_chain_assoc_get (ly_symbol2scm ("font-shape"), chain,
				      SCM_BOOL_F);
      SCM weight = ly_chain_assoc_get (ly_symbol2scm ("font-series"), chain,
				       SCM_BOOL_F);
      
      Real step = robust_scm2double (ly_symbol2scm ("font-size"), 0.0);
      Real size = layout->get_dimension (ly_symbol2scm ("text-font-size"))
	* pow (2.0, step / 6.0);

      description
	= symbols_to_pango_font_description (family, style, variant, weight,
					     SCM_BOOL_F,
					     size);
    }

  Font_metric * fm = all_fonts_global->find_pango_font (description);

  return find_scaled_font (layout, fm, 1.0,
			   ly_symbol2scm ("latin1"),
			   ly_symbol2scm ("latin1")); 
}


PangoStyle
symbol_to_pango_style (SCM style)
{
  PangoStyle pstyle = PANGO_STYLE_NORMAL;
  if (style == ly_symbol2scm ("italic"))
    {
      pstyle = PANGO_STYLE_NORMAL;
    }
  else if (style == ly_symbol2scm ("oblique")
	   || style == ly_symbol2scm ("slanted")
	   )
    {
      pstyle = PANGO_STYLE_OBLIQUE;
    }

  return pstyle;
}

PangoVariant
symbol_to_pango_variant (SCM variant)
{
  PangoVariant pvariant;
  if (variant == ly_symbol2scm ("caps"))
    {
      pvariant = PANGO_VARIANT_SMALL_CAPS;
    }
  return pvariant;
}


PangoWeight
symbol_to_pango_weight (SCM weight)
{
  PangoWeight pw = PANGO_WEIGHT_NORMAL;
  if (weight == ly_symbol2scm ("bold"))
    {
      pw = PANGO_WEIGHT_BOLD;
    }
  if (weight == ly_symbol2scm ("heavy"))
    {
      pw = PANGO_WEIGHT_HEAVY;
    }
  if (weight == ly_symbol2scm ("ultrabold"))
    {
      pw = PANGO_WEIGHT_ULTRABOLD;
    }
  if (weight == ly_symbol2scm ("light"))
    {
      pw = PANGO_WEIGHT_LIGHT;
    }
  if (weight == ly_symbol2scm ("ultralight"))
    {
      pw = PANGO_WEIGHT_ULTRALIGHT;
    }

  return pw;
}

PangoStretch
symbol_to_pango_stretch (SCM) //  stretch)
{
  PangoStretch ps = PANGO_STRETCH_NORMAL;

  /*
    // TODO
    
  PANGO_STRETCH_ULTRA_CONDENSED,
  PANGO_STRETCH_EXTRA_CONDENSED,
  PANGO_STRETCH_CONDENSED,
  PANGO_STRETCH_SEMI_CONDENSED,
  
  PANGO_STRETCH_SEMI_EXPANDED,
  PANGO_STRETCH_EXPANDED,
  PANGO_STRETCH_EXTRA_EXPANDED,
  PANGO_STRETCH_ULTRA_EXPANDED
  */ 
  return ps;
}



PangoFontDescription* 
symbols_to_pango_font_description(SCM family,
				  SCM style,
				  SCM variant,
				  SCM weight,
				  SCM stretch,
				  Real size)
{
  PangoFontDescription * description = pango_font_description_new ();

  String family_str = scm_is_symbol (family)
    ? ly_symbol2string (family)
    : String("roman");
  pango_font_description_set_family (description,
				     family_str.to_str0 ());
  pango_font_description_set_style (description,
				    symbol_to_pango_style (style));
  pango_font_description_set_variant (description,
				      symbol_to_pango_variant (variant));
  pango_font_description_set_weight (description,
				     symbol_to_pango_weight (weight));
  pango_font_description_set_stretch (description,
				      symbol_to_pango_stretch (stretch));
  pango_font_description_set_size (description,
				   gint (size * PANGO_SCALE));

  return description;
}
