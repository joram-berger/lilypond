/*
  property-iterator.hh -- declare Property_iterator

  source file of the GNU LilyPond music typesetter

  (c)  1997--2000 Han-Wen Nienhuys <hanwen@cs.uu.nl>
*/


#ifndef PROPERTY_ITERATOR_HH
#define PROPERTY_ITERATOR_HH

#include "simple-music-iterator.hh"




/**
  Iterate a property.  
 */
class Property_iterator : public Simple_music_iterator
{
public:
  VIRTUAL_COPY_CONS (Music_iterator);
  static SCM constructor_cxx_function;
  /* construction */
protected:
  virtual void process (Moment);
};

class Push_property_iterator : public Simple_music_iterator
{
public:
  VIRTUAL_COPY_CONS (Music_iterator);
  static SCM constructor_cxx_function;  
protected:
  /* construction */
  virtual void process (Moment);
};

class Pop_property_iterator : public Simple_music_iterator
{
public:
  static SCM constructor_cxx_function;
  VIRTUAL_COPY_CONS (Music_iterator);
protected:
  /* construction */
  virtual void process (Moment);
};


#endif // PROPERTY_ITERATOR_HH
