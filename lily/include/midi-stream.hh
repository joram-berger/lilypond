/*
  midi-stream.hh -- declare Midi_stream

  (c)  1997--2001 Jan Nieuwenhuizen <janneke@gnu.org>
 */

#ifndef MIDI_STREAM_HH
#define MIDI_STREAM_HH

#include "string.hh"

/// Midi outputfile
struct Midi_stream {
  Midi_stream (String filename_str);
  ~Midi_stream();

  Midi_stream& operator <<( String str);
  Midi_stream& operator <<( Midi_item const& midi_c_r);
  Midi_stream& operator <<( int i);

  void open();

  ostream* os_p_;
  String filename_str_;
};

#endif // MIDI_STREAM_HH
