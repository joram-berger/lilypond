#!@PYTHON@

# once upon a rainy monday afternoon.
#
#   ...
#
# (not finished.)
# ABC standard v1.6:  http://www.gre.ac.uk/~c.walshaw/abc2mtex/abc.txt
#
# Enhancements  (Roy R. Rankin)
#
# Header section moved to top of lilypond file
# handle treble, treble-8, alto, and bass clef
# Handle voices (V: headers) with clef and part names, multiple voices
# Handle w: lyrics with multiple verses
# Handle key mode names for minor, major, phrygian, ionian, locrian, aeolian,
#     mixolydian, lydian, dorian
# Handle part names from V: header
# Tuplets handling fixed up
# Lines starting with |: not discarded as header lines
# Multiple T: and C: header entries handled
# Accidental maintained until next bar check
# Silent rests supported
# articulations fermata, upbow, downbow, ltoe, accent, tenuto supported
# Chord strings([-^]"string") can contain a '#'
# Header fields enclosed by [] in notes string processed
# W: words output after tune as abc2ps does it (they failed before)

# Enhancements (Laura Conrad)
#
# Barring now preserved between ABC and lilypond
# the default placement for text in abc is above the staff.
# %%LY now supported.						
			
# Limitations
#
# Multiple tunes in single file not supported
# Blank T: header lines should write score and open a new score
# Not all header fields supported
# ABC line breaks are ignored
# Block comments generate error and are ignored
# Postscript commands are ignored
# lyrics not resynchronized by line breaks (lyrics must fully match notes)
# ???



#TODO:
# UNDEF -> None
 
  
  
program_name = 'abc2ly'
version = '@TOPLEVEL_VERSION@'
if version == '@' + 'TOPLEVEL_VERSION' + '@':
	version = '(unknown version)'		# uGUHGUHGHGUGH
  
import __main__
import getopt
import sys
import re
import string
import os


UNDEF = 255
state = UNDEF
voice_idx_dict = {}
header = {}
lyrics = []
slyrics = []
voices = []
state_list = []
current_voice_idx = -1
current_lyric_idx = -1
lyric_idx = -1
part_names = 0
default_len = 8
length_specified = 0
nobarlines = 0
global_key = [0] * 7			# UGH
names = ["One", "Two", "Three"]
DIGITS='0123456789'
HSPACE=' \t'

	
def check_clef(s):
      if not s:
              return ''
      if re.match('^treble', s):
              s = s[6:]
              if re.match ('^-8', s):
                      s = s[2:]
                      state.base_octave = -2
                      voices_append("\\clef \"G_8\";\n")
              else:
                      state.base_octave = 0
                      voices_append("\\clef treble;\n")
      elif re.match('^-8va', s):
	      s = s[4:]
	      state.base_octave = -1
	      voices_append("\\clef \"G_8\";\n")
      elif re.match('^alto', s):
              s = s[4:]
              state.base_octave = -1
              voices_append ("\\clef alto;\n" )
      elif re.match('^bass',s ):
              s = s[4:]
              state.base_octave = -2
              voices_append ("\\clef bass;\n" )
      return s

def select_voice (name, rol):
	if not voice_idx_dict.has_key (name):
	      state_list.append(Parser_state())
	      voices.append ('')
	      slyrics.append ([])
	      voice_idx_dict[name] = len (voices) -1
	__main__.current_voice_idx =  voice_idx_dict[name]
	__main__.state = state_list[current_voice_idx]
	while rol != '':
	      m = re.match ('^([^ \t=]*)=(.*)$', rol) # find keywork
	      if m:
		      keyword = m.group(1)
		      rol = m.group (2)
		      a = re.match ('^("[^"]*"|[^ \t]*) *(.*)$', rol)
		      if a:
			      value = a.group (1)
			      rol = a.group ( 2)
			      if keyword == 'clef':
				      check_clef(value)
			      elif keyword == "name":
				      value = re.sub ('\\\\','\\\\\\\\', value)
				      voices_append ("\\property Staff.instrument = %s\n" % value )
				      __main__.part_names = 1
			      elif keyword == "sname" or keyword == "snm":
				      voices_append ("\\property Staff.instr = %s\n" % value )

	      else:
		      break

	return


def dump_header (outf,hdr):
	outf.write ('\\header {\n')
	ks = hdr.keys ()
	ks.sort ()
	for k in ks:
		outf.write ('\t%s = "%s";\n'% (k,hdr[k]))
 	outf.write ('}')

def dump_lyrics (outf):
	if (len(lyrics)):
		outf.write("\n\\score\n{\n    \\context Lyrics\n    <\n")
		for i in range (len (lyrics)):
			outf.write ( lyrics [i])
			outf.write ("\n")
		outf.write("    >\n    \\paper{}\n}\n")

def dump_default_bar (outf):
	outf.write ("\n\\property Score.defaultBarType=\"empty\"\n")


def dump_slyrics (outf):
	ks = voice_idx_dict.keys()
	ks.sort ()
	for k in ks:
		for i in range (len(slyrics[voice_idx_dict[k]])):
			outf.write ("\nwords%sV%d = \\lyrics  {" % (k, i))
			outf.write ("\n" + slyrics [voice_idx_dict[k]][i])
			outf.write ("\n}")

def dump_voices (outf):
	ks = voice_idx_dict.keys()
	ks.sort ()
	for k in ks:
		outf.write ("\nvoice%s = \\notes {" % k)
		dump_default_bar(outf)
		outf.write ("\n" + voices [voice_idx_dict[k]])
		outf.write ("\n}")
	
def dump_score (outf):
	outf.write (r"""\score{
        \notes <
""")

	ks  = voice_idx_dict.keys ();
	ks.sort ()
	for k in  ks:
		if k == 'default' and len (voice_idx_dict) > 1:
			break
		if len ( slyrics [voice_idx_dict[k]] ):
			outf.write ("\n        \\addlyrics")
		outf.write ("\n\t\\context Staff=\"%s\"\n\t{\n" %k ) 
		if k != 'default':
			outf.write ("\t    \\$voicedefault\n")
		outf.write ("\t    \\$voice%s " % k)
		outf.write ("\n\t}\n")
		if len ( slyrics [voice_idx_dict[k]] ):
			outf.write ("\n\t\\context Lyrics=\"%s\" \n\t<\t" % k)
			for i in range (len(slyrics[voice_idx_dict[k]])):
				outf.write("\n\t  { \\$words%sV%d }" % ( k, i) )
			outf.write ( "\n\t>\n" )
	outf.write ("\n    >")
	outf.write ("\n\t\\paper {\n")
	if part_names:
		outf.write ("\t    \\translator \n\t    {\n")
		outf.write ("\t\t\\StaffContext\n")
		outf.write ("\t\t\\consists Staff_margin_engraver;\n")
		outf.write ("\t    }\n")
	outf.write ("\t}\n\t\\midi {}\n}\n")



def set_default_length (s):
	global length_specified
	m =  re.search ('1/([0-9]+)', s)
	if m:
		__main__.default_len = string.atoi ( m.group (1))
		length_specified = 1

def set_default_len_from_time_sig (s):
	m =  re.search ('([0-9]+)/([0-9]+)', s)
	if m:
		n = string.atoi (m.group (1))
		d = string.atoi (m.group (2))
		if (n * 1.0 )/(d * 1.0) <  0.75:
			__main__.default_len =  16
		else:
			__main__.default_len = 8

def gulp_file(f):
	try:
		i = open(f)
		i.seek (0, 2)
		n = i.tell ()
		i.seek (0,0)
	except:
		sys.stderr.write ("can't open file: %s\n" % f)
		return ''
	s = i.read (n)
	if len (s) <= 0:
		sys.stderr.write ("gulped empty file: %s\n" % f)
	i.close ()
	return s


# pitch manipulation. Tuples are (name, alteration).
# 0 is (central) C. Alteration -1 is a flat, Alteration +1 is a sharp
# pitch in semitones. 
def semitone_pitch  (tup):
	p =0

	t = tup[0]
	p = p + 12 * (t / 7)
	t = t % 7
	
	if t > 2:
		p = p- 1
		
	p = p + t* 2 + tup[1]
	return p

def fifth_above_pitch (tup):
	(n, a)  = (tup[0] + 4, tup[1])

	difference = 7 - (semitone_pitch ((n,a)) - semitone_pitch (tup))
	a = a + difference
	
	return (n,a)

def sharp_keys ():
	p = (0,0)
	l = []
	k = 0
	while 1:
		l.append (p)
		(t,a) = fifth_above_pitch (p)
		if semitone_pitch((t,a)) % 12 == 0:
			break

		p = (t % 7, a)
	return l

def flat_keys ():
	p = (0,0)
	l = []
	k = 0
	while 1:
		l.append (p)
		(t,a) = quart_above_pitch (p)
		if semitone_pitch((t,a)) % 12 == 0:
			break

		p = (t % 7, a)
	return l

def quart_above_pitch (tup):
	(n, a)  = (tup[0] + 3, tup[1])

	difference = 5 - (semitone_pitch ((n,a)) - semitone_pitch (tup))
	a = a + difference
	
	return (n,a)

key_lookup = { 	# abc to lilypond key mode names
	'm'   : 'minor',
	'min' : 'minor',
	'maj' : 'major',
	'phr' : 'phrygian',
	'ion' : 'ionian',
	'loc' : 'locrian',
	'aeo' : 'aeolian',
	'mix' : 'mixolydian',
	'lyd' : 'lydian',
	'dor' : 'dorian'
}

def lily_key (k):
	k = string.lower (k)
	key = k[0]
	k = k[1:]
	if k and k[0] == '#':
		key = key + 'is'
		k = k[1:]
	elif k and k[0] == 'b':
		key = key + 'es'
		k = k[1:]
	if not k:
		return '%s \\major' % key

	type = k[0:3]
	if key_lookup.has_key(type):
		return("%s \\%s" % ( key, key_lookup[type]))
	sys.stderr.write("Unknown key type %s ignored\n" % type)
	return key

def shift_key (note, acc , shift):
        s = semitone_pitch((note, acc))
        s = (s + shift + 12) % 12
        if s <= 4:
                n = s / 2
                a = s % 2
        else:
                n = (s + 1) / 2
                a = (s + 1) % 2
        if a:
                n = n + 1
                a = -1
        return (n,a)

key_shift = { # semitone shifts for key mode names
	'm'   : 3,
	'min' : 3,
	'maj' : 0,
	'phr' : -4,
	'ion' : 0,
	'loc' : 1,
	'aeo' : 3,
	'mix' : 5,
	'lyd' : -5,
	'dor' :	-2
}
def compute_key (k):
	k = string.lower (k)
	intkey = (ord (k[0]) - ord('a') + 5) % 7
	intkeyacc =0
	k = k[1:]
	
	if k and k[0] == 'b':
		intkeyacc = -1
		k = k[1:]
	elif  k and k[0] == '#':
		intkeyacc = 1
		k = k[1:]
	k = k[0:3]
	if k and key_shift.has_key(k):
		(intkey, intkeyacc) = shift_key(intkey, intkeyacc, key_shift[k])
	keytup = (intkey, intkeyacc)
	
	sharp_key_seq = sharp_keys ()
	flat_key_seq = flat_keys ()

	accseq = None
	accsign = 0
	if keytup in sharp_key_seq:
		accsign = 1
		key_count = sharp_key_seq.index (keytup)
		accseq = map (lambda x: (4*x -1 ) % 7, range (1, key_count + 1))

	elif keytup in flat_key_seq:
		accsign = -1
		key_count = flat_key_seq.index (keytup)
		accseq = map (lambda x: (3*x + 3 ) % 7, range (1, key_count + 1))
	else:
		raise "Huh"
	
	key_table = [0] * 7
	for a in accseq:
		 key_table[a] = key_table[a] + accsign

	return key_table

tup_lookup = {
	'2' : '3/2',
	'3' : '2/3',
	'4' : '4/3',
	'5' : '4/5',
	'6' : '4/6',
	'7' : '6/7',
	'9' : '8/9',
	}


def try_parse_tuplet_begin (str, state):
	if re.match ('\([2-9]', str):
		dig = str[1]
		str = str[2:]
		state.parsing_tuplet = string.atoi (dig[0])
		
		voices_append ("\\times %s {" % tup_lookup[dig])
	return str

def  try_parse_group_end (str, state):
	if str and str[0] in HSPACE:
		str = str[1:]
	return str
	
def header_append (key, a):
	s = ''
	if header.has_key (key):
		s = header[key] + "\n"
	header [key] = s + a

def wordwrap(a, v):
	linelen = len (v) - string.rfind(v, '\n')
	if linelen + len (a) > 80:
		v = v + '\n'
	return v + a + ' '

def stuff_append (stuff, idx, a):
	if not stuff:
		stuff.append (a)
	else:
		stuff [idx] = wordwrap(a, stuff[idx])



def voices_append(a):
	if current_voice_idx < 0:
		select_voice ('default', '')

	stuff_append (voices, current_voice_idx, a)

def lyrics_append(a):
	a = re.sub ( '#', '\\#', a)	# latex does not like naked #'s
	a = re.sub ( '"', '\\"', a)	# latex does not like naked "'s
	a = '\t{ \\lyrics "' + a + '" }\n'
	stuff_append (lyrics, current_lyric_idx, a)

# break lyrics to words and put "'s around words containing numbers and '"'s
def fix_lyric(str):
	ret = ''

	while str != '':
		m = re.match('[ \t]*([^ \t]*)[ \t]*(.*$)', str)
		if m:
			word = m.group(1)
			str = m.group(2)
			word = re.sub('"', '\\"', word) # escape "
			if re.match('.*[0-9"]', word):
				word = re.sub('_', ' ', word) # _ causes probs inside ""
				ret = ret + '\"' + word + '\" '
			else:
				ret = ret + word + ' '
		else:
			return (ret)
	return (ret)

def slyrics_append(a):
	a = re.sub ( '_', ' _ ', a)	# _ to ' _ '
	a = re.sub ( '-', '- ', a)	# split words with -
	a = re.sub ( '\\\\- ', '-', a) 	# unless \-
	a = re.sub ( '~', '_', a)	# ~ to space('_')
	a = re.sub ( '\*', '_ ', a)	# * to to space
	a = re.sub ( '#', '\\#', a)	# latex does not like naked #'s
	if re.match('.*[0-9"]', a):	# put numbers and " into quoted string
		a = fix_lyric(a)
	a = re.sub ( '$', ' ', a)	# insure space between lines
	__main__.lyric_idx = lyric_idx + 1
	if len(slyrics[current_voice_idx]) <= lyric_idx:
		slyrics[current_voice_idx].append(a)
	else:
		v = slyrics[current_voice_idx][lyric_idx]
		slyrics[current_voice_idx][lyric_idx] = wordwrap(a, slyrics[current_voice_idx][lyric_idx])


def try_parse_header_line (ln, state):
	global length_specified
	m = re.match ('^([A-Za-z]): *(.*)$', ln)

	if m:
		g =m.group (1)
		a = m.group (2)
		if g == 'T':	#title
			a = re.sub('[ \t]*$','', a)	#strip trailing blanks
			if header.has_key('title'):
				if a:
					header['title'] = header['title'] + '\\\\\\\\' + a
			else:
				header['title'] =  a
		if g == 'M':	# Meter
			if a == 'C':
				if not state.common_time:
					state.common_time = 1
					voices_append ("\\property Staff.TimeSignature \push #\'style = #\"C\"\n")
				a = '4/4'
			if a == 'C|':
				if not state.common_time:
					state.common_time = 1
					voices_append ("\\property Staff.TimeSignature \push #\'style = #\"C\"\n")
				a = '2/2'
			if not length_specified:
				set_default_len_from_time_sig (a)
			else:
				length_specified = 0
			voices_append ('\\time %s;' % a)
			state.next_bar = ''
		if g == 'K': # KEY
			a = check_clef(a)
			if a:
				m = re.match ('^([^ \t]*) *(.*)$', a) # seperate clef info
				if m:
					# there may or may not be a space
					# between the key letter and the mode
					if key_lookup.has_key(m.group(2)[0:3]):
						key_info = m.group(1) + m.group(2)[0:3]
						clef_info = m.group(2)[4:]
					else:
						key_info = m.group(1)
						clef_info = m.group(2)
					__main__.global_key  = compute_key (key_info)# ugh.
					voices_append ('\\key %s;' % lily_key(key_info))
					check_clef(clef_info)
				else:
					__main__.global_key  = compute_key (a)# ugh.
					voices_append ('\\key %s \\major;' % lily_key(a))
		if g == 'O': # Origin
			header ['origin'] = a
		if g == 'X': # Reference Number
			header ['crossRefNumber'] = a
		if g == 'A': #	Area
			header ['area'] = a
		if g == 'H':	# History
			header_append ('history', a)
		if g == 'B':	# Book
			header ['book'] = a
		if g == 'C':	# Composer
			if header.has_key('composer'):
				if a:
					header['composer'] = header['composer'] + '\\\\\\\\' + a
			else:
				header['composer'] =  a
		if g == 'S':
			header ['subtitle'] = a
		if g == 'L':	# Default note length
			set_default_length (ln)
		if g == 'V':	# Voice 
			voice = re.sub (' .*$', '', a)
			rest = re.sub ('^[^ \t]*  *', '', a)
			if state.next_bar:
				voices_append(state.next_bar)
				state.next_bar = ''
			select_voice (voice, rest)
		if g == 'W':	# Words
			lyrics_append(a);
		if g == 'w':	# vocals
			slyrics_append (a);

		return ''
	return ln

# we use in this order specified accidental, active accidental for bar,
# active accidental for key
def pitch_to_mudela_name (name, acc, bar_acc, key):
	s = ''
	if acc == UNDEF:
		if not nobarlines:
			acc = bar_acc
	if acc == UNDEF:
		acc = key
	if acc == -1:
		s = 'es'
	elif acc == 1:
		s =  'is'
	
	if name > 4:
		name = name -7
	return(chr (name  + ord('c')) + s)


def octave_to_mudela_quotes (o):
	o = o + 2
	s =''
	if o < 0:
		o = -o
		s=','
	else:
		s ='\''

	return s * o

def parse_num (str):
	durstr = ''
	while str and str[0] in DIGITS:
		durstr = durstr + str[0]
		str = str[1:]

	n = None
	if durstr:
		n  =string.atoi (durstr) 
	return (str,n)


def duration_to_mudela_duration  (multiply_tup, defaultlen, dots):
	base = 1
	# (num /  den)  / defaultlen < 1/base
	while base * multiply_tup[0] < multiply_tup[1]:
		base = base * 2
	return '%d%s' % ( base, '.'* dots)

class Parser_state:
	def __init__ (self):
		self.in_acc = {}
		self.next_articulation = ''
		self.next_bar = ''
		self.next_dots = 0
		self.next_den = 1
		self.parsing_tuplet = 0
		self.plus_chord = 0
		self.base_octave = 0
		self.common_time = 0



# return (str, num,den,dots) 
def parse_duration (str, parser_state):
	num = 0
	den = parser_state.next_den
	parser_state.next_den = 1

	(str, num) = parse_num (str)
	if not num:
		num = 1
	
	if str[0] == '/':
		while str[:1] == '/':
			str= str[1:]
			d = 2
			if str[0] in DIGITS:
				(str, d) =parse_num (str)

			den = den * d

	den = den * default_len
	
	current_dots = parser_state.next_dots
	parser_state.next_dots = 0
	if re.match ('[ \t]*[<>]', str):
		while str[0] in HSPACE:
			str = str[1:]
		while str[0] == '>':
			str = str [1:]
			current_dots = current_dots + 1;
			parser_state.next_den = parser_state.next_den * 2
		
		while str[0] == '<':
			str = str [1:]
			den = den * 2
			parser_state.next_dots = parser_state.next_dots + 1



	try_dots = [3, 2, 1]
	for d in try_dots:
		f = 1 << d
		multiplier = (2*f-1)
		if num % multiplier == 0 and den % f == 0:
			num = num / multiplier
			den = den / f
			current_dots = current_dots + d
		
	return (str, num,den,current_dots)


def try_parse_rest (str, parser_state):
	if not str or str[0] <> 'z' and str[0] <> 'x':
		return str

	__main__.lyric_idx = -1

	if parser_state.next_bar:
		voices_append(parser_state.next_bar)
		parser_state.next_bar = ''

	if str[0] == 'z':
		rest = 'r'
	else:
		rest = 's'
	str = str[1:]

	(str, num,den,d) = parse_duration (str, parser_state)
	voices_append ('%s%s' % (rest, duration_to_mudela_duration ((num,den), default_len, d)))
	if parser_state.next_articulation:
		voices_append (parser_state.next_articulation)
		parser_state.next_articulation = ''

	return str

artic_tbl = {
	'.'  : '-.',
	 'T' : '^\\trill',
	 'H' : '^\\fermata',
	 'u' : '^\\upbow',
	 'K' : '^\\ltoe',
	 'k' : '^\\accent',
	 'M' : '^\\tenuto',
	 '~' : '^"~" ',
	 'J' : '',		# ignore slide
	 'R' : '',		# ignore roll
	 'v' : '^\\downbow'
}
	
def try_parse_articulation (str, state):
	
	while str and  artic_tbl.has_key(str[:1]):
		state.next_articulation = state.next_articulation + artic_tbl[str[:1]]
		if not artic_tbl[str[:1]]:
			sys.stderr.write("Warning: ignoring %s\n" % str[:1] )

		str = str[1:]

	
		
	# s7m2 input doesnt care about spaces
	if re.match('[ \t]*\(', str):
		str = string.lstrip (str)

	slur_begin =0
	while str[:1] =='(' and str[1] not in DIGITS:
		slur_begin = slur_begin + 1
		state.next_articulation = state.next_articulation + '('
		str = str[1:]

	return str
		
#
# remember accidental for rest of bar
#
def set_bar_acc(note, octave, acc, state):
	if acc == UNDEF:
		return
	n_oct = note + octave * 7
	state.in_acc[n_oct] = acc

# get accidental set in this bar or UNDEF if not set
def get_bar_acc(note, octave, state):
	n_oct = note + octave * 7
	if state.in_acc.has_key(n_oct):
		return(state.in_acc[n_oct])
	else:
		return(UNDEF)

def clear_bar_acc(state):
	for k in state.in_acc.keys():
		del state.in_acc[k]
	

		
# WAT IS ABC EEN ONTZETTENDE PROGRAMMEERPOEP  !
def try_parse_note (str, parser_state):
	mud = ''

	slur_begin =0
	if not str:
		return str

	articulation =''
	acc = UNDEF
	if str[0] in '^=_':
		c = str[0]
		str = str[1:]
		if c == '^':
			acc = 1
		if c == '=':
			acc = 0
		if c == '_':
			acc = -1

        octave = parser_state.base_octave
	if str[0] in "ABCDEFG":
		str = string.lower (str[0]) + str[1:]
		octave = octave - 1


	notename = 0
	if str[0] in "abcdefg":
		notename = (ord(str[0]) - ord('a') + 5)%7
		str = str[1:]
	else:
		return str		# failed; not a note!

	
	__main__.lyric_idx = -1

	if parser_state.next_bar:
		voices_append(parser_state.next_bar)
		parser_state.next_bar = ''

	while str[0] == ',':
		 octave = octave - 1
		 str = str[1:]
	while str[0] == '\'':
		 octave = octave + 1
		 str = str[1:]

	(str, num,den,current_dots) = parse_duration (str, parser_state)


	if re.match('[ \t]*\)', str):
		str = string.lstrip (str)
	
	slur_end =0
	while str[:1] ==')':
		slur_end = slur_end + 1
		str = str[1:]

	
	if slur_end:
		voices_append ('%s' % ')' *slur_end )

	bar_acc = get_bar_acc(notename, octave, parser_state)
	pit = pitch_to_mudela_name(notename, acc, bar_acc, global_key[notename])
	oct = octave_to_mudela_quotes (octave)
	if acc != UNDEF and (acc == global_key[notename] or acc == bar_acc):
		mod='!'
	else:
		mod = ''
	voices_append ("%s%s%s%s" %
		(pit, oct, mod,
	 	 duration_to_mudela_duration ((num,den), default_len, current_dots)))
	
	set_bar_acc(notename, octave, acc, parser_state)
	if parser_state.next_articulation:
		articulation = articulation + parser_state.next_articulation
		parser_state.next_articulation = ''

	voices_append (articulation)

	if parser_state.parsing_tuplet:
		parser_state.parsing_tuplet = parser_state.parsing_tuplet - 1
		if not parser_state.parsing_tuplet:
			voices_append ("}")
	if slur_begin:
		voices_append ('%s' % '(' * slur_begin )


	return str

def junk_space (str):
	while str and str[0] in '\t\n ':
		str = str[1:]

	return str


def try_parse_guitar_chord (str, state):
	if str[:1] =='"':
		str = str[1:]
		gc = ''
		while str and str[0] != '"':
			gc = gc + str[0]
			str = str[1:]
			
		if str:
			str = str[1:]
		gc = re.sub('#', '\\#', gc)	# escape '#'s
		state.next_articulation = ("^\"%s\"" % gc) + state.next_articulation
	return str

def try_parse_escape (str):
	if not str or str [0] != '\\':
		return str
	
	str = str[1:]
	if str[:1] =='K':
		key_table = compute_key ()
	return str

#
# |] thin-thick double bar line
# || thin-thin double bar line
# [| thick-thin double bar line
# :| left repeat
# |: right repeat
# :: left-right repeat
# |1 volta 1
# |2 volta 2
bar_dict = {
'|]' : '|.',
'||' : '||',
'[|' : '||',
':|' : ':|',
'|:' : '|:',
'::' : ':|:',
'|1' : '|',
'|2' : '|',
':|2' : ':|',
'|' :  '|'
}


warn_about = ['|:', '::', ':|', '|1', ':|2', '|2']

def try_parse_bar (str,state):
	bs = None

	# first try the longer one
	for trylen in [3,2,1]:
		if str[:trylen] and bar_dict.has_key (str[:trylen]):
			s = str[:trylen]
			bs = "\\bar \"%s\";" % bar_dict[s]
			if s in warn_about:
				sys.stderr.write('Warning kludging for barline `%s\'\n' % s)
			str = str[trylen:]
			break

	if str[:1] == '|':
		state.next_bar = '|\n'
		str = str[1:]
		clear_bar_acc(state)
	
	if bs <> None or state.next_bar != '':
		if state.parsing_tuplet:
			state.parsing_tuplet =0
			voices_append ('} ')
		
	if bs <> None:
		clear_bar_acc(state)
		voices_append (bs)

	return str

def try_parse_tie (str):
	if str[:1] =='-':
		str = str[1:]
		voices_append (' ~ ')
	return str

def bracket_escape (str, state):
	m = re.match ( '^([^\]]*)] *(.*)$', str)
	if m:
		cmd = m.group (1)
		str = m.group (2)
		try_parse_header_line (cmd, state)
	return str

def try_parse_chord_delims (str, state):
	if str[:1] =='[':
		str = str[1:]
		if re.match('[A-Z]:', str):	# bracket escape
			return bracket_escape(str, state)
		if state.next_bar:
			voices_append(state.next_bar)
			state.next_bar = ''
		voices_append ('<')

	if str[:1] == '+':
		str = str[1:]
		if state.plus_chord:
			voices_append ('>')
			state.plus_chord = 0
		else:
			if state.next_bar:
				voices_append(state.next_bar)
				state.next_bar = ''
			voices_append ('<')
			state.plus_chord = 1

	ch = ''
	if str[:1] ==']':
		str = str[1:]
		ch = '>'

	end = 0
	while str[:1] ==')':
		end = end + 1
		str = str[1:]

	
	voices_append ("\\spanrequest \\stop \"slur\"" * end);
	voices_append (ch)
	return str

def try_parse_grace_delims (str, state):
	if str[:1] =='{':
		if state.next_bar:
			voices_append(state.next_bar)
			state.next_bar = ''
		str = str[1:]
		voices_append ('\\grace { ')

	if str[:1] =='}':
		str = str[1:]
		voices_append ('}')

	return str

def try_parse_comment (str):
	global nobarlines
	if (str[0] == '%'):
		if str[0:5] == '%MIDI':
#the nobarlines option is necessary for an abc to mudela translator for
#exactly the same reason abc2midi needs it: abc requires the user to enter
#the note that will be printed, and MIDI and lilypond expect entry of the
#pitch that will be played.
#
#In standard 19th century musical notation, the algorithm for translating
#between printed note and pitch involves using the barlines to determine
#the scope of the accidentals.
#
#Since ABC is frequently used for music in styles that do not use this
#convention, such as most music written before 1700, or ethnic music in
#non-western scales, it is necessary to be able to tell a translator that
#the barlines should not affect its interpretation of the pitch.  
			if (string.find(str,'nobarlines') > 0):
 		                #debugging
				nobarlines = 1
		elif str[0:3] == '%LY':
			p = string.find(str, 'voices')
			if (p > -1):
				voices_append(str[p+7:])
				voices_append("\n")
#write other kinds of appending  if we ever need them.			
	return str

happy_count = 100
def parse_file (fn):
	f = open (fn)
	ls = f.readlines ()

	select_voice('default', '')
	lineno = 0
	sys.stderr.write ("Line ... ")
	sys.stderr.flush ()
	__main__.state = state_list[current_voice_idx]
	
	for ln in ls:
		lineno = lineno + 1

		if not (lineno % happy_count):
			sys.stderr.write ('[%d]'% lineno)
			sys.stderr.flush ()
		m = re.match  ('^([^%]*)%(.*)$',ln)  # add comments to current voice
		if m:
			if m.group(2):
				try_parse_comment(m.group(2))
				voices_append ('%% %s\n' % m.group(2))
			ln = m.group (1)

		orig_ln = ln
		
		ln = try_parse_header_line (ln, state)

		# Try nibbling characters off until the line doesn't change.
		prev_ln = ''
		while ln != prev_ln:
			prev_ln = ln
			ln = try_parse_chord_delims (ln, state)
			ln = try_parse_rest (ln, state)
			ln = try_parse_articulation (ln,state)
			ln = try_parse_note  (ln, state)
			ln = try_parse_bar (ln, state)
			ln = try_parse_tie (ln)
			ln = try_parse_escape (ln)
			ln = try_parse_guitar_chord (ln, state)
			ln = try_parse_tuplet_begin (ln, state)
			ln = try_parse_group_end (ln, state)
			ln = try_parse_grace_delims (ln, state)
			ln = junk_space (ln)

		if ln:
			msg = "%s: %d: Huh?  Don't understand\n" % (fn, lineno)
			sys.stderr.write (msg)
			left = orig_ln[0:-len (ln)]
			sys.stderr.write (left + '\n')
			sys.stderr.write (' ' *  len (left) + ln + '\n')	


def identify():
	sys.stderr.write ("%s from LilyPond %s\n" % (program_name, version))

def help ():
	print r"""
Convert ABC to Mudela.

Usage: abc2ly [OPTIONS]... ABC-FILE

Options:
  -h, --help          this help
  -o, --output=FILE   set output filename to FILE
  -v, --version       version information

This program converts ABC music files (see
http://www.gre.ac.uk/~c.walshaw/abc2mtex/abc.txt) To LilyPond input.
"""

def print_version ():
	print r"""abc2ly (GNU lilypond) %s""" % version



(options, files) = getopt.getopt (sys.argv[1:], 'vo:h', ['help','version', 'output='])
out_filename = ''

for opt in options:
	o = opt[0]
	a = opt[1]
	if o== '--help' or o == '-h':
		help ()
		sys.exit (0)
	if o == '--version' or o == '-v':
		print_version ()
		sys.exit(0)
		
	if o == '--output' or o == '-o':
		out_filename = a
	else:
		print o
		raise getopt.error

identify()

header['tagline'] = 'Lily was here %s -- automatically converted from ABC' % version
for f in files:
	if f == '-':
		f = ''

	sys.stderr.write ('Parsing... [%s]\n' % f)
	parse_file (f)

	if not out_filename:
		out_filename = os.path.basename (os.path.splitext (f)[0]) + ".ly"
	sys.stderr.write ('Ly output to: %s...' % out_filename)
	outf = open (out_filename, 'w')

#	dump_global (outf)
	dump_header (outf ,header)
	dump_slyrics (outf)
	dump_voices (outf)
	dump_score (outf)
	dump_lyrics (outf)
	sys.stderr.write ('\n')
	
