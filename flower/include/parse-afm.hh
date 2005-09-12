/* Modified 1999 Morten Welinder:
 * 1. ANSI prototype.
 * 2. parseFileFree function.
 */
// 2000 HWN: AFM_ prefixes.
/*
 * (C) 1988, 1989 by Adobe Systems Incorporated. All rights reserved.
 *
 * This file may be freely copied and redistributed as long as:
 *   1) This entire notice continues to be included in the file,
 *   2) If the file has been modified in any way, a notice of such
 *      modification is conspicuously indicated.
 *
 * PostScript, Display PostScript, and Adobe are registered trademarks of
 * Adobe Systems Incorporated.
 *
 * ************************************************************************
 * THE INFORMATION BELOW IS FURNISHED AS IS, IS SUBJECT TO CHANGE WITHOUT
 * NOTICE, AND SHOULD NOT BE CONSTRUED AS A COMMITMENT BY ADOBE SYSTEMS
 * INCORPORATED. ADOBE SYSTEMS INCORPORATED ASSUMES NO RESPONSIBILITY OR
 * LIABILITY FOR ANY ERRORS OR INACCURACIES, MAKES NO WARRANTY OF ANY
 * KIND (EXPRESS, IMPLIED OR STATUTORY) WITH RESPECT TO THIS INFORMATION,
 * AND EXPRESSLY DISCLAIMS ANY AND ALL WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR PARTICULAR PURPOSES AND NONINFRINGEMENT OF THIRD PARTY RIGHTS.
 * ************************************************************************
 */

/* ParseAFM.h
 *
 * This header file is used in conjuction with the parseAFM.c file.
 * Together these files provide the functionality to parse Adobe Font
 * Metrics files and store the information in predefined data structures.
 * It is intended to work with an application program that needs font metric
 * information. The program can be used as is by making a procedure call to
 * parse an AFM file and have the data stored, or an application developer
 * may wish to customize the code.
 *
 * This header file defines the data structures used as well as the key
 * strings that are currently recognized by this version of the AFM parser.
 * This program is based on the document "Adobe Font Metrics Files,
 * Specification Version 2.0".
 *
 * AFM files are separated into distinct sections of different data. Because
 * of this, the parseAFM program can parse a specified file to only save
 * certain sections of information based on the application's needs. A record
 * containing the requested information will be returned to the application.
 *
 * AFM files are divided into five sections of data:
 *	1) The Global Font Information
 *	2) The Character Metrics Information
 *	3) The Track Kerning Data
 *	4) The Pair-Wise Kerning Data
 *	5) The Composite Character Data
 *
 * Basically, the application can request any of these sections independent
 * of what other sections are requested. In addition, in recognizing that
 * many applications will want ONLY the x-width of characters and not all
 * of the other character metrics information, there is a way to receive
 * only the width information so as not to pay the storage cost for the
 * unwanted data. An application should never request both the
 * "quick and dirty" char metrics (widths only) and the Character Metrics
 * Information since the Character Metrics Information will contain all
 * of the character widths as well.
 *
 * There is a procedure in parseAFM.c, called parseFile, that can be
 * called from any application wishing to get information from the AFM File.
 * This procedure expects 3 parameters: a vaild file descriptor, a pointer
 * to a (FontInfo *) variable (for which space will be allocated and then
 * will be filled in with the data requested), and a mask specifying
 * which data from the AFM File should be saved in the FontInfo structure.
 *
 * The flags that can be used to set the appropriate mask are defined below.
 * In addition, several commonly used masks have already been defined.
 *
 * History:
 *	original: DSM  Thu Oct 20 17:39:59 PDT 1988
 *  modified: DSM  Mon Jul  3 14:17:50 PDT 1989
 *    - added 'storageProblem' return code
 *	  - fixed typos
 */

#include <cstdio>
using namespace std;

#define BOOL int
#define FLAGS int

/* Possible return codes from the parseFile procedure.
 *
 * ok means there were no problems parsing the file.
 *
 * parseError means that there was some kind of parsing error, but the
 * parser went on. This could include problems like the count for any given
 * section does not add up to how many entries there actually were, or
 * there was a key that was not recognized. The return record may contain
 * vaild data or it may not.
 *
 * earlyEOF means that an End of File was encountered before expected. This
 * may mean that the AFM file had been truncated, or improperly formed.
 *
 * storageProblem means that there were problems allocating storage for
 * the data structures that would have contained the AFM data.
 */
#define AFM_ok 0
#define AFM_parseError -1
#define AFM_earlyEOF -2
#define AFM_storageProblem -3

/************************* TYPES *********************************/
/* Below are all of the data structure definitions. These structures
 * try to map as closely as possible to grouping and naming of data
 * in the AFM Files.
 */

/* Bounding box definition. Used for the Font AFM_BBox as well as the
 * Character AFM_BBox.
 */
typedef struct
{
  int llx;	/* lower left x-position  */
  int lly;	/* lower left y-position  */
  int urx;	/* upper right x-position */
  int ury;	/* upper right y-position */
}
  AFM_BBox;

/* Global Font information.
 * The key that each field is associated with is in comments. For an
 * explanation about each key and its value please refer to the AFM
 * documentation (full title & version given above).
 */
typedef struct
{
  char *afmVersion;		/* key: StartFontMetrics */
  char *fontName;		/* key: FontName */
  char *fullName;		/* key: FullName */
  char *familyName;		/* key: FamilyName */
  char *weight;		/* key: Weight */
  float italicAngle;		/* key: ItalicAngle */
  BOOL isFixedPitch;		/* key: IsFixedPitch */
  AFM_BBox fontBBox;		/* key: FontBBox */
  int underlinePosition;  	/* key: UnderlinePosition */
  int underlineThickness; 	/* key: UnderlineThickness */
  char *version;		/* key: Version */
  char *notice;		/* key: Notice */
  char *encodingScheme;	/* key: EncodingScheme */
  int capHeight;		/* key: CapHeight */
  int xHeight;			/* key: XHeight */
  int ascender;		/* key: Ascender */
  int descender;		/* key: Descender */
}
  AFM_GlobalFontInfo;

/* Ligature definition is a linked list since any character can have
 * any number of ligatures.
 */
typedef struct _t_ligature
{
  char *succ, *lig;
  struct _t_ligature *next;
} AFM_Ligature;

/* Character Metric Information. This structure is used only if ALL
 * character metric information is requested. If only the character
 * widths is requested, then only an array of the character x-widths
 * is returned.
 *
 * The key that each field is associated with is in comments. For an
 * explanation about each key and its value please refer to the
 * Character Metrics section of the AFM documentation (full title
 * & version given above).
 */
typedef struct
{
  int code,                                 		/* key: C */
    wx,                                		/* key: WX */
    wy;		/* together wx and wy are associated with key: W */
  char *name; 	/* key: N */
  AFM_BBox charBBox;	/* key: B */
  AFM_Ligature *ligs;	/* key: L (linked list; not a fixed number of Ls */
}
  AFM_CharMetricInfo;

/* Track kerning data structure.
 * The fields of this record are the five values associated with every
 * TrackKern entry.
 *
 * For an explanation about each value please refer to the
 * Track Kerning section of the AFM documentation (full title
 * & version given above).
 */
typedef struct
{
  int degree;
  float minPtSize,
    minKernAmt,
    maxPtSize,
    maxKernAmt;
}
  AFM_TrackKernData;

/* Pair Kerning data structure.
 * The fields of this record are the four values associated with every
 * KP entry. For KPX entries, the yamt will be zero.
 *
 * For an explanation about each value please refer to the
 * Pair Kerning section of the AFM documentation (full title
 * & version given above).
 */
typedef struct
{
  char *name1;
  char *name2;
  int xamt,
    yamt;
}
  AFM_PairKernData;

/* AFM_Pcc is a piece of a composite character. This is a sub structure of a
 * AFM_CompCharData described below.
 * These fields will be filled in with the values from the key AFM_Pcc.
 *
 * For an explanation about each key and its value please refer to the
 * Composite Character section of the AFM documentation (full title
 * & version given above).
 */
typedef struct
{
  char *AFM_PccName;
  int deltax,
    deltay;
}
  AFM_Pcc;

/* Composite Character Information data structure.
 * The fields ccName and numOfPieces are filled with the values associated
 * with the key CC. The field pieces points to an array (size = numOfPieces)
 * of information about each of the parts of the composite character. That
 * array is filled in with the values from the key AFM_Pcc.
 *
 * For an explanation about each key and its value please refer to the
 * Composite Character section of the AFM documentation (full title
 * & version given above).
 */
typedef struct
{
  char *ccName;
  int numOfPieces;
  AFM_Pcc *pieces;
}
  AFM_CompCharData;

/*  FontInfo
 *  Record type containing pointers to all of the other data
 *  structures containing information about a font.
 *  A a record of this type is filled with data by the
 *  parseFile function.
 */
typedef struct
{
  AFM_GlobalFontInfo *gfi;	/* ptr to a AFM_GlobalFontInfo record */
  int *cwi;			/* ptr to 256 element array of just char widths */
  int numOfChars;		/* number of entries in char metrics array */
  AFM_CharMetricInfo *cmi;	/* ptr to char metrics array */
  int numOfTracks;		/* number to entries in track kerning array */
  AFM_TrackKernData *tkd;		/* ptr to track kerning array */
  int numOfPairs;		/* number to entries in pair kerning array */
  AFM_PairKernData *pkd;		/* ptr to pair kerning array */
  int numOfComps;		/* number to entries in comp char array */
  AFM_CompCharData *ccd;		/* ptr to comp char array */
}
  AFM_Font_info;

/************************* PROCEDURES ****************************/

/*  Call this procedure to do the grunt work of parsing an AFM file.
 *
 *  "fp" should be a valid file pointer to an AFM file.
 *
 *  "fi" is a pointer to a pointer to a FontInfo record sturcture
 * (defined above). Storage for the FontInfo structure will be
 *  allocated in parseFile and the structure will be filled in
 *  with the requested data from the AFM File.
 *
 *  "flags" is a mask with bits set representing what data should
 *  be saved. Defined above are valid flags that can be used to set
 *  the mask, as well as a few commonly used masks.
 *
 *  The possible return codes from parseFile are defined above.
 */

int AFM_parseFile (FILE *fp, AFM_Font_info **fi, FLAGS flags);
void AFM_free (AFM_Font_info *fi);
