/*
  instrument-name-engraver.cc -- implement Instrument_name_engraver

  source file of the GNU LilyPond music typesetter

  (c) 2000--2005 Han-Wen Nienhuys <hanwen@cs.uu.nl>
*/

#include "engraver.hh"
#include "bar-line.hh"
#include "system-start-delimiter.hh"
#include "side-position-interface.hh"
#include "align-interface.hh"
#include "axis-group-interface.hh"
#include "context.hh"
#include "text-item.hh"

class Instrument_name_engraver : public Engraver
{

public:
  TRANSLATOR_DECLARATIONS (Instrument_name_engraver);

protected:
  Grob *text_;

  virtual void create_text ();
  virtual void initialize ();
  virtual void acknowledge_grob (Grob_info);
  virtual void stop_translation_timestep ();
  virtual void process_music ();
};

Instrument_name_engraver::Instrument_name_engraver ()
{
  text_ = 0;
}

void
Instrument_name_engraver::initialize ()
{
  context ()->set_property ("instrumentSupport", SCM_EOL);
}

void
Instrument_name_engraver::stop_translation_timestep ()
{
  if (text_)
    {
      text_->set_property ("side-support-elements",
			   get_property ("instrumentSupport"));
      text_ = 0;
    }
}

void
Instrument_name_engraver::create_text ()
{
  if (text_)
    return;

  SCM txt = get_property ("instrument");

  if (now_mom () > Moment (0))
    txt = get_property ("instr");
  /*
    UGH.
  */
  if (txt == SCM_EOL)
    return;

  text_ = make_item ("InstrumentName", SCM_EOL);

  if (text_->get_property ("text") != txt)
    text_->set_property ("text", txt);
}

void
Instrument_name_engraver::acknowledge_grob (Grob_info i)
{
  if (Bar_line::has_interface (i.grob ()))
    {
      create_text ();
    }

  /*
    Ugh - typechecking for pedal and dynamic sucks.
  */
  if (dynamic_cast<Spanner *> (i.grob ())
      && (i.grob ()->internal_has_interface (ly_symbol2scm ("dynamic-interface"))
	  || i.grob ()->internal_has_interface (ly_symbol2scm ("piano-pedal-interface"))))
    return;

  /*
    Hang the instrument names on the staves, but not on the alignment
    groups enclosing that staff. The alignment has no real location,
    but is only a vehicle for the placement routine it contains, and
    therefore the location of its refpoint won't be very useful.

    We could also just use stavesFound, but lets keep this working
    without staffs as well.
  */
  if (dynamic_cast<Spanner *> (i.grob ())
      && ((Axis_group_interface::has_interface (i.grob ())
	   && Axis_group_interface::has_axis (i.grob (), Y_AXIS)))
      && !Align_interface::has_interface (i.grob ()))
    {
      SCM nl = scm_cons (i.grob ()->self_scm (),
			 get_property ("instrumentSupport"));

      context ()->set_property ("instrumentSupport", nl);
    }
}

void
Instrument_name_engraver::process_music ()
{
  /*
    Also create text if barlines in other groups. This allows
    a name to be attached to lyrics or chords.
  */
  if (scm_is_string (get_property ("whichBar")))
    create_text ();
}

ADD_TRANSLATOR (Instrument_name_engraver,
		/* descr */ " Prints the name of the instrument (specified by "
		" @code{Staff.instrument} and @code{Staff.instr}) "
		"at the left of the staff. ",
		/* creats*/ "InstrumentName",
		/* accepts */ "",
		/* acks  */ "bar-line-interface axis-group-interface",
		/* reads */ "instrument instr",
		/* write */ "");

/****************************************************************/

class Vocal_name_engraver : public Instrument_name_engraver
{
public:
  TRANSLATOR_DECLARATIONS (Vocal_name_engraver);
  virtual void create_text ();
};

Vocal_name_engraver::Vocal_name_engraver ()
{
}

void
Vocal_name_engraver::create_text ()
{
  if (text_)
    return;

  SCM txt = get_property ("vocalName");

  if (now_mom () > Moment (0))
    txt = get_property ("vocNam");

  /*
    UGH.
  */
  if (txt == SCM_EOL)
    return;

  text_ = make_item ("VocalName", SCM_EOL);

  if (text_->get_property ("text") != txt)
    text_->set_property ("text", txt);
}

ADD_TRANSLATOR (Vocal_name_engraver,
		/* descr */ " Prints the name of the a lyric voice (specified by "
		" @code{Staff.vocalName} and @code{Staff.vocNam}) "
		"at the left of the staff. ",
		/* creats*/ "VocalName",
		/* accepts */ "",
		/* acks  */ "bar-line-interface axis-group-interface",
		/* reads */ "vocNam vocalName",
		/* write */ "");
