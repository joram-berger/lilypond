#!@PYTHON@

# mf-to-table.py -- convert spacing info in  MF logs .afm and .tex
# 
# source file of the GNU LilyPond music typesetter
# 
# (c) 1997 Han-Wen Nienhuys <hanwen@cs.uu.nl>

import os
import sys
import getopt
import string
import re
import time


postfixes = ['log', 'dvi', '2602gf', 'tfm']

def read_log_file (fn):
	str = open (fn).read ()
	str = re.sub ('\n', '', str) 	
	str = re.sub ('[\t ]+', ' ', str) 

	deps = []
	autolines = []
	def include_func (match, d = deps):
		d.append (match.group (1))
		return ''

	def auto_func (match, a = autolines):
		a.append (match.group (1))
		return ''

	str = re.sub ('\(([a-zA-Z_0-9-]+\.mf)', include_func, str)
	str = re.sub ('@{(.*?)@}', auto_func, str)

	return (autolines, deps)



class Char_metric:
	def __init__ (self):
		pass


def tfm_checksum (fn):
	sys.stderr.write ("Reading checksum from `%s'\n" % fn) 
	s = open (fn).read ()
	s = s[ 12 * 2 : ]
	cs_bytes = s[:4]

	shift = 24
	cs = 0
	for b in cs_bytes:
		cs = cs  + (ord (b) << shift)
		shift = shift - 8

	return cs

## ugh.  What's font_family supposed to be?  It's not an afm thing.
font_family = 'feta'
def parse_logfile (fn):
	(autolines, deps) = read_log_file (fn)
	charmetrics = []
	global_info = {}
	group = ''

	for l in autolines:
		tags = string.split(l, '@:')
		if tags[0] == 'group':
			group = tags[1]
		elif tags[0] == 'char':
			m = {
				'description':  tags[1],
				'name': group + '-' + tags[7],
				'tex': tags[8],
				'code': string.atoi (tags[2]),
				'breapth':string.atof (tags[3]),
				'width': string.atof (tags[4]),
				'depth':string.atof (tags[5]),
				'height':string.atof (tags[6])
				}
			charmetrics.append (m)
		elif tags[0] == 'font':
			global font_family
			font_family = (tags[3])
			# To omit 'GNU' (foundry) from font name proper:
			# name = tags[2:]
			#urg
			if 0: #testing
				tags.append ('Regular')
			name = tags[1:]
			global_info['FontName'] = string.join (name,'-')
			global_info['FullName'] = string.join (name,' ')
			global_info['FamilyName'] = string.join (name[1:-1],
								 '-')
			if 1:
				global_info['Weight'] = tags[4]
			else: #testing
				global_info['Weight'] = tags[-1]
			global_info['FontBBox'] = '0 0 1000 1000'
			global_info['Ascender'] = '0'
			global_info['Descender'] = '0'
			global_info['EncodingScheme'] = 'FontSpecific'
	
	return (global_info, charmetrics, deps)


def write_afm_char_metric(file, charmetric):

	f = 1000;
	tup = (charmetric['code'],
	       (charmetric['width'] + charmetric['breapth'])*f,
		charmetric['name'],
		-charmetric['breapth'] *f,
		-charmetric['depth']*f,
		charmetric['width']*f,
		charmetric['height']*f)
	
	
	file.write ('C %d ; WX %d ; N  %s ;  B %d %d %d %d ;\n'% tup)

def write_afm_header (file):
	file.write ("StartFontMetrics 2.0\n")
	file.write ("Comment Automatically generated by mf-to-table.py\n")

def write_afm_metric (file, global_info, charmetrics):
	for (k,v) in global_info.items():
		file.write ("%s %s\n" % (k,v))
	file.write ('StartCharMetrics %d\n' % len(charmetrics ))
	for m in charmetrics:
		write_afm_char_metric (file,m)
	file.write ('EndCharMetrics\n')
	file.write ('EndFontMetrics\n')


def write_tex_defs (file, global_info, charmetrics):
	##nm = global_info['FontFamily']
	nm = font_family
	for m in charmetrics:
		file.write (r'''\gdef\%s%s{\char%d}%%%s''' % (nm, m['tex'], m['code'],'\n'))
	file.write ('\\endinput\n')

def write_ps_encoding (file, global_info, charmetrics):
	encs = ['.notdef'] * 256
	for m in charmetrics:
		encs[m['code']] = m['tex']
		
	file.write ('/FetaEncoding [\n')
	for m in range(0,256):
		file.write ('  /%s %% %d\n' % (encs[m], m))
	file.write ('] def\n')
	
def write_fontlist (file, global_info, charmetrics):
	##nm = global_info['FontFamily']
	nm = font_family
	file.write (r"""
% Lilypond file to list all font symbols and the corresponding names
% Automatically generated by mf-to-table.py
\score{\notes{\fatText
""")
	for m in charmetrics:
		escapedname=re.sub('_','\\\\\\\\_', m['name'])
		file.write ('  s^\\markup { \\char #%d "%s" }\n' % (m['code'], escapedname))
	file.write (r"""
}
  \paper{
    interscoreline=1
    \translator{
      \ScoreContext
      \remove "Bar_number_engraver"
      TextScript \override #'extra-X-extent = #'(-1 . 1)
    }
    \translator{
      \StaffContext
      \remove "Clef_engraver"
      \remove "Key_engraver"
      \remove "Time_signature_engraver"
      \remove "Staff_symbol_engraver"
      minimumVerticalExtent = ##f
    }
  }
}
""")

def write_deps (file, deps, targets):
	
	
	for t in targets:
		t = re.sub ( '^\\./', '', t)
		file.write ('%s '% t)
	file.write (": ")
	for d in deps:
		file.write ('%s ' % d)
	file.write ('\n')

def help():
    sys.stdout.write(r"""Usage: mf-to-table [options] LOGFILEs
Generate feta metrics table from preparated feta log\n
Options:
  -a, --afm=FILE         .afm file
  -d, --dep=FILE         print dependency info to FILE
  -h, --help             print this help
  -l, --ly=FILE          name output table
  -o, --outdir=DIR       prefix for dependency info
  -p, --package=DIR      specify package
  -t, --tex=FILE         name output tex chardefs"""
)
    sys.exit (0)



(options, files) = getopt.getopt(
    sys.argv[1:], 'a:d:hl:o:p:t:', 
    ['enc=', 'afm=', 'outdir=', 'dep=',  'tex=', 'ly=', 'debug', 'help', 'package='])


enc_nm = ''
texfile_nm = ''
depfile_nm = ''
afmfile_nm = ''
lyfile_nm = ''
outdir_prefix = '.'

for opt in options:
	o = opt[0]
	a = opt[1]
	if o == '--dep' or o == '-d':
		depfile_nm = a
	elif o == '--outdir' or o == '-o':
		outdir_prefix = a
	elif o == '--tex' or o == '-t':
		texfile_nm = a
	elif o == '--enc':
		enc_nm = a
	elif o == '--ly' or o == '-':
		lyfile_nm = a
	elif o== '--help' or o == '-h':
		help()
	elif o=='--afm' or o == '-a':
		afmfile_nm = a
	elif o == '--debug':
		debug_b = 1
	elif o == '-p' or o == '--package':
		topdir = a
	else:
		print o
		raise getopt.error

base = re.sub ('.tex$', '', texfile_nm)

for filenm in files:
	(g,m, deps) =  parse_logfile (filenm)
	cs = tfm_checksum (re.sub ('.log$', '.tfm', filenm))
	afm = open (afmfile_nm, 'w')

	write_afm_header (afm)
	afm.write ("Comment TfmCheckSum %u\n" % cs)
	write_afm_metric (afm, g, m)
	
	write_tex_defs (open (texfile_nm, 'w'), g, m)
	write_ps_encoding (open (enc_nm, 'w'), g, m)

	write_deps (open (depfile_nm, 'wb'), deps, [base + '.dvi', base + '.pfa', base + '.pfb',  texfile_nm, afmfile_nm])
	if lyfile_nm != '':
		write_fontlist(open (lyfile_nm, 'w'), g, m)



