/*
  key-reg.cc -- implement Key_engraver

  source file of the GNU LilyPond music typesetter

  (c)  1997--1998 Han-Wen Nienhuys <hanwen@cs.uu.nl>

  */
#include "key-engraver.hh"
#include "key-item.hh"
#include "command-request.hh"
#include "local-key-engraver.hh"
#include "musical-request.hh"
#include "local-key-item.hh"
#include "bar.hh"
#include "time-description.hh"

Key_engraver::Key_engraver ()
{
  kit_p_ = 0;
  do_post_move_processing ();
}

void
Key_engraver::create_key ()
{
  if (!kit_p_) 
    {
      kit_p_ = new Key_item;
      kit_p_->break_priority_i_ = -1; // ugh
      announce_element (Score_element_info (kit_p_,keyreq_l_));


      for (int i = 0; i < accidental_idx_arr_.size(); i++) 
	{
	  Musical_pitch m_l =accidental_idx_arr_[i];
	  int a =m_l.accidental_i_;      
	  if (key_.multi_octave_b_)
	    kit_p_->add (m_l.steps (), a);
	  else
	    kit_p_->add (m_l.notename_i_, a);
	}

      for (int i = 0 ; i< old_accidental_idx_arr_.size(); i++) 
	{
	  Musical_pitch m_l =old_accidental_idx_arr_[i];
	  int a =m_l.accidental_i_;
	  if (key_.multi_octave_b_)
	    kit_p_->add_old (m_l.steps  (), a);
	  else
	    kit_p_->add_old (m_l.notename_i_, a);
	}
    }
}      


bool
Key_engraver::do_try_request (Request * req_l)
{
  if (Key_change_req *kc = dynamic_cast <Key_change_req *> (req_l))
    {
      if (keyreq_l_)
	warning ("Fixme: key change merge.");
      keyreq_l_ = kc;
      read_req (keyreq_l_);
      return true;
    }   
  return  false;
}

void
Key_engraver::acknowledge_element (Score_element_info info)
{
  if (dynamic_cast <Clef_change_req *> (info.req_l_)) 
    {
      int i= get_property ("createKeyOnClefChange").length_i ();
      if (i)
	create_key ();
    }
  else if (dynamic_cast<Bar *> (info.elem_l_)
	   && accidental_idx_arr_.size ()) 
    {
      if (!keyreq_l_)
	default_key_b_ = true;
      create_key ();
    }

}

void
Key_engraver::do_process_requests ()
{
  if (keyreq_l_) 
    {
      create_key ();
    }
}

void
Key_engraver::do_pre_move_processing ()
{ 
  if (kit_p_) 
    {
      kit_p_->default_b_ = default_key_b_;
      typeset_element (kit_p_);
      kit_p_ = 0;
    }
}


/*
  TODO Slightly hairy.  
 */
void
Key_engraver::read_req (Key_change_req const * r)
{
  old_accidental_idx_arr_ = accidental_idx_arr_;
  key_.clear ();
  Scalar prop = get_property ("keyoctaviation");
  if (prop.length_i () > 0)
    {
      key_.multi_octave_b_ = ! prop.to_bool ();
    }
  
  accidental_idx_arr_.clear ();

  if (r->ordinary_key_b_) 
    {
      int p;
      if (r->pitch_arr_.size () < 1) 
        {
	  r->warning (_ ("No key name: assuming `C'"));
	  p = 0;
	}
      else
	{
	  p = r->pitch_arr_[0].semitone_pitch ();
	  p += r->modality_i_;
	}
      /* Solve the equation 7*no_of_acc mod 12 = p, -6 <= no_of_acc <= 5 */
      int no_of_acc = (7*p) % 12;
      no_of_acc = (no_of_acc + 18) % 12 -6;

      /* Correct from flats to sharps or vice versa */
      if (no_of_acc * r->pitch_arr_[0].accidental_i_ < 0)
	no_of_acc += 12 * sign (r->pitch_arr_[0].accidental_i_);

      if (no_of_acc < 0) 
	{
	  int accidental = 6 ; // First accidental: bes
	  for ( ; no_of_acc < 0 ; no_of_acc++ ) 
	    {
	      Musical_pitch m;
	      m.accidental_i_ = -1;
	      m.notename_i_ = accidental;
	      if (key_.multi_octave_b_)
		key_.set (m);
	      else
		key_.set (m.notename_i_, m.accidental_i_);
	      accidental_idx_arr_.push (m);
	      
	      accidental = (accidental + 3) % 7 ;
	    }
	}
      else 
	{ 
	  int accidental = 3 ; // First accidental: fis
	  for ( ; no_of_acc > 0 ; no_of_acc-- ) 
	    {
	      Musical_pitch m;
	      m.accidental_i_ = 1;
	      m.notename_i_ = accidental;
	      if (key_.multi_octave_b_)
		key_.set (m);
	      else
		key_.set (m.notename_i_, m.accidental_i_);
	      accidental_idx_arr_.push (m);
	      
	      accidental = (accidental + 4) % 7 ;
	    }
	}
    }
  else // Special key
    {
      for (int i = 0; i < r->pitch_arr_.size (); i ++) 
	{
	  Musical_pitch m_l =r->pitch_arr_[i];
	  if (key_.multi_octave_b_)
	    key_.set (m_l);
	  else
	    key_.set (m_l.notename_i_, m_l.accidental_i_);
	  
	  accidental_idx_arr_.push (m_l);
	}
    }
}

void
Key_engraver::do_post_move_processing ()
{
  keyreq_l_ = 0;
  default_key_b_ = false;
  old_accidental_idx_arr_.clear ();
}


IMPLEMENT_IS_TYPE_B1 (Key_engraver,Engraver);
ADD_THIS_TRANSLATOR (Key_engraver);

