/*
  notename-table.hh -- declare 

  source file of the GNU LilyPond music typesetter

  (c) 1997 Han-Wen Nienhuys <hanwen@stack.nl>
*/


#ifndef NOTENAME_TABLE_HH
#define NOTENAME_TABLE_HH

#include "pointer.hh"
#include "string.hh"
#include "lily-proto.hh"
#include "assoc.hh"

class Notename_table :   Assoc<String, P<Melodic_req> >{
public:
    void add(String, Melodic_req*);
    Melodic_req*get_l(String);
};
  
#endif // NOTENAME_TABLE_HH
