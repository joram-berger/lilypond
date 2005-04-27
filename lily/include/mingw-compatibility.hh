/*
  mingw-compatibility.hh -- MINGW workarounds

  source file of the GNU LilyPond music typesetter

  (c) 2005 Jan Nieuwenhuizen <janneke@gnu.org>
*/

#ifndef MINGW_COMPATIBILITY_HH
#define MINGW_COMPATIBILITY_HH

#if __MINGW32__

/* Mingw uses invalid names for typedefs and defines.  Not yet
   investigated whether this is a mingw bug or a windows bug (ie,
   mingw compatibility feature), also not reported yet.  */

#  ifdef CHAR
#    define LILY_CHAR CHAR
#    undef CHAR
#  endif
#  define CHAR MINGW_INFRINGES_ON_OUR_NAMESPACE_USING_CHAR

#  ifdef CONTEXT
#    define LILY_CONTEXT CONTEXT
#    undef CONTEXT
#  endif
#  define CONTEXT MINGW_INFRINGES_ON_OUR_NAMESPACE_USING_CONTEXT

#  ifdef RELATIVE
#    define LILY_RELATIVE RELATIVE
#    undef RELATIVE
#  endif
#  define RELATIVE MINGW_INFRINGES_ON_OUR_NAMESPACE_USING_RELATIVE

#  ifdef THIS
#    define LILY_THIS THIS
#    undef THIS
#  endif
#  define THIS MINGW_INFRINGES_ON_OUR_NAMESPACE_USING_THIS

//#  include <winsock2.h>

#if defined (__MINGW32__) && !defined (STATIC)
# define SCM_IMPORT 1
#endif

#  include <libguile.h>

#  undef CHAR
#  ifdef LILY_CHAR
#    define CHAR LILY_CHAR
#  endif

#  undef CONTEXT
#  ifdef LILY_CONTEXT
#    define CONTEXT LILY_CONTEXT
#  endif
#  undef CONTEXT

#  undef RELATIVE
#  ifdef LILY_RELATIVE
#    define RELATIVE LILY_RELATIVE
#  endif

#  undef THIS
#  ifdef LILY_THIS
#    define THIS LILY_THIS
#  endif


#endif /* __MINGW__ */

#endif /* MINGW_COMPATIBILITY_HH */
