# c-builder
Small python script to build c programs, stuctured as folder module

## What It Does?

Its a Python Script that goes through your source directory and collects all the .c files. Then it filters through the files, on the basis of

- Accept Files
- Ignore Certain Files
- Accept Folder
- Ignore Folder despite being a .c files conatainer
- Accept file name patern
- Ignore file name patern


Example:
This is the folder structure in one my other projects ![zint](github.com/zakarouf/zint)
``` bash
>>> exa -T
.
├── common
│  ├── common_color.h
│  ├── common_string.c
│  └── common_string.h
├── common.h
├── examples
│  ├── count.zintfile
│  └── helloworld.zintfile
├── LICENCE.md
├── README.md
├── start.py
├── Z.un_zFile
├── zcon
│  ├── zcon_main.c
│  └── zcon_sys.h
├── zint
│  ├── zint_config.h
│  ├── zint_defs.h
│  ├── zint_inBuilt_modules
│  │  ├── zmod_curses.c
│  │  └── zmod_math.c
│  ├── zint_main.c
│  ├── zint_sys.c
│  └── zint_sys.h
└── Ztest.zfile
```
It contains 3 main Folders

- common => It includues all the code i.e needed by all other programs
- zint => Source code for zint (includes main() function )
- zcon => Souce code for zint convertor (includes main() function)

Now you already there are 2 folders containing main() function and are independent from one another. But both of them need `common` for work
so instead of copying code or anything. I'll just put a string in cbuild.py, inside `folderIgnore`.
```python
folderIgnore={"zcon"}
```
That's it Now if I run cbuild.py it takes all the source code execpt for in zcon.
Better yet It also work in sub-directories

So, Example 2:
```bash
>>> exa -T zint
zint
├── zint_config.h
├── zint_defs.h
├── zint_inBuilt_modules
│  ├── zmod_curses.c
│  └── zmod_math.c
├── zint_main.c
├── zint_sys.c
└── zint_sys.h
```
Now I have `zint` directory where I have a sub-directory name `zint_inBuilt_modules`, it contains additional modules for my program. but what if i want to build my program to without the optional `zint_inBuilt_modules`, now there are only 2 files but in future there will be more, keeping track of them would be a chore but here we again only have to add one string in cbuild.py

```python
folderIgnore={"zint_inBuilt_modules"}
```
Voila! Its done no hassle, nothing.
Consedering you have #ifdefs in your other c files so they dont unknowingly include them.

## Cool, How Can I Use This?

Inside the cbuild.py there are some globals, which defines, what to include...

```python
folderIgnore={"zint_inBuilt_modules", "zcon"}  # Do not take anything from these directories
IgnoreNames={"a.c", "test.c"}                  # Do not take these files

ignorePatternFront = ["."]                     # Do not take files that start with *
ignorePatternEnd = []                          # Do not take files that ends with *
onlyTakePatternEnd = [".c"]                    # Only take files that ends with *


CC="clang"                                     # Compiler
CFLAGS=["-std=c99", "-Os", "-O2"]              # CFLAGS
LDFLAGS=""                                     # LDFLAGS
OUTEXE="cb-out"                                # Executable name

testCommands = []                              # Default Arguments run the executable once it compiled, can be change with -m argument
```

On Commandline executing it with some flags:
- -b ,--build [source_dir_path]   Change the source dir path default is './'
- -c ,--clean                     Cleans the build dir
- -w ,--testwith [args..]         Set Arguments for compiled binary test run (should be used at last)
- -t ,--testdisable               Disables test run

## Why not makefiles?
Python is a language I was more comfortable with, so I wrote it in it.
My style of placing/naming in C code files is very ordered and verbose and this script compliments that. At the end of the getting the code running asap is the more important. Heck even a bash script will do in many cases. But they don't scale very well as the file and folder structure gets bigger and bigger. 

I'm not telling anyone to not use makefiles. Makefiles are great. They are `install goes brrr..` at its finest. And you should learn it and use it, rather than my small script.

Cheers!!!