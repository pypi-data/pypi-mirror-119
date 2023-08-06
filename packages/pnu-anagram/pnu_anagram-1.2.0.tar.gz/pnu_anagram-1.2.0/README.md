# Installation
pip install [pnu-anagram](https://pypi.org/project/pnu-anagram/)

# ANAGRAM(6)

## NAME
anagram - rearrange letters to form new words

## SYNOPSIS
**anagram**
\[-d|--dictionary pathname\]
\[-f|--files\]
\[-l|--length numbers\]
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]
\[letters\]

## DESCRIPTION
The **anagram** utility rearranges the given *letters* to form as many words (anagrams) as possible.

Standard input is read if no letters are provided on the command line.

The *-l|--length* option can be used to form words of selected size with the letters provided.

The *-f|--files* option can help you select a dictionary.

### OPTIONS
Options | Use
------- | ---
-d\--dictionary pathname|Use this dictionary pathname if you don't want the default dictionary
-f\|--files|Print possible dictionary files in the DICTPATH
-l\|--length numbers|Specify anagrams lengths if you want intermediate sizes. *numbers* is a number or a comma separated list of numbers or dash separated number intervals
--debug|Enable debug mode
--help\|-?|Print usage and a short help message and exit
--version|Print version and exit
--|Options processing terminator

## ENVIRONMENT
The ANAGRAM_DEBUG environment variable can also be set to any value to enable debug mode.

The DICTPATH environment variable is the search path for the dictionary files.
It is a colon-separated list of directories in which **anagram** looks for a *words* dictionary file.
If not set it will default to /usr/share/dict:/usr/local/share/dict.
Under a Posix system, $HOME/.local/share/dict will also be added to the default,
while %HOMEPATH%/appdata/roaming/python/share/dict:%HOMEPATH%/appdata/local/programs/python/pythonXX/share/dict will be added under a Windows system.

The ANAGRAM_DICT environment variable provides a way to avoid specifying an alternate directory on each command line.

## FILES
*/usr/share/dict/words* is the default (English) dictionary on a BSD operating system.

Some French dictionaries are also installed as a dependency.

## EXIT STATUS
The **anagram** utility exits 0 on success, and >0 if an error occurs.

## EXAMPLES
To solve a Wordscapes (French) level where the available letters are ABCDEFG, I use a command like:
```Shell
$ export ANAGRAM_DICT=/usr/local/share/dict/dict-fr-Wordscapes
$ anagram -l 3-7 abcdefg
```

Other dictionaries are also available. For example:
```Shell
$ export ANAGRAM_DICT=/usr/local/share/dict/dict-fr-ABU-mots_communs.ascii
$ export ANAGRAM_DICT=/usr/local/share/dict/dict-fr-AU-DELA-common-words.ascii
```

## SEE ALSO
[grep(1)](https://www.freebsd.org/cgi/man.cgi?query=grep)

## STANDARDS
The **anagram** utility is not a standard UNIX command.

This utility tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
Tested OK under Windows.

## HISTORY
This utility was made for the [PNU project](https://github.com/HubTou/PNU)
in order to help my wife play
[Wordscapes](https://play.google.com/store/apps/details?id=com.peoplefun.wordcross)
when she was stuck on a level.

## LICENSE
It is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

## CAVEATS
An English dictionary should be packaged for operating systems that are not providing one.

Searching only for a *words* link to one of the directories in the DICTPATH is too limitated.

