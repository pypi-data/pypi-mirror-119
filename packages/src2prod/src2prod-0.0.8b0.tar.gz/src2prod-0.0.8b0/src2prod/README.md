The `Python` module `src2prod`
==============================

> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.


About `src2prod`
----------------

This module allows to develop a project within a source folder and to publish the final product in another folder, this last directory being a "thin" version of the source one. If you use `git`, this module can talk with it to do a better job.


The example used for a short tutorial
-------------------------------------

Let's consider [`TeXitEasy`](https://github.com/projetmbc/tools-for-latex/tree/master/TeXitEasy) which had merly the following tree structure on August 9, 2021 (this was the very begining of this project that used a single small `README.md` file).

~~~
+ TeXitEasy
    + changes
        + 2021
            * 08.txt
        * LICENSE.txt
        * x-todo-x.txt

    + src
        * __init__.py
        * escape.py
        * LICENSE.txt
        + tool_config
            * escape.peuf
        * tool_debug.py
        * tool_escape.py

    + tests
        + escape
            * escape.peuf
            * fstringit.peuf
            * test_fstringit.py
            * test_escape.py
        * about.peuf
        * pyproject.toml
        * README.md
~~~


Building a thin copy of the source folder
-----------------------------------------

### What we want...

In our project above, there are some files only useful for the development of the code.

  1. Names using the pattern `x-...-x` indicate files or folders to be ignored by `git` (there are no such file or folder in the `src` folder but we could imagine using some of them).

  1. Names using the pattern `tool_...` are for files and folders to not copy into the final product, but at the same time to be kept by `git`.

  1. The `README.md` file used for `git` servers must also be used for the final product.


The final product built from the `src` folder must have the following name and structure.

~~~
+ texiteasy
    * __init__.py
    * escape.py
    * LICENSE.txt
    * README.md
~~~


### How to do that?

Here is how to acheive a selective copy of the `src` folder to the `texiteasy` one. We will suppose the use of the `cd` command to go inside the parent folder of `TeXitEasy` before launching the following script where we use instances of `Path` from `pathlib`.

~~~python
from src2prod import *

project = Project(
    project = Path('TeXitEasy'),
    source  = Path('src'),
    target  = Path('texiteasy'),
    ignore  = '''
        tool_*/
        tool_*.*
    ''',
    usegit = True,
    readme = Path('README.md')
)

project.update()
~~~

Here are some important points about the code above.

  1. `project`, `source`, `target` and `readme` follows the rules below.

      * The values of this arguments can also be strings (that will be converted to instances of `Path`).

      * The argument `readme` is optional contrary to `project`, `source` and `target`.

      * `project` is a complete path regarding the working directory when launching the file, but `source`, `target` and `readme` are relative to `project`.

  1. The argument `ignore` can be used even if the project doesn't use `git`. It can be either a string containing rules, or an absolute `Path` to a file containg rules (an absolute path allows to use the same rules for several projects). Let's see now how to define rules.

      * Empty lines are ignored (this allows a basic formatting of rules).

      * Each none empty line is internally stripped. This will indicate one rule for either a file or a folder.

      * A rule finishing by `/` is for a folder: internally the last `/` is removed such as to store the rule only for folders.

      * Each rule will be used with the method `match` of `pathlib.Path` (this is very basic).

  1. `usegit = True` asks also to ignore files and folders as `git` does (this action completes the rules defined in `ignore`). This setting implies that there isn't any uncommited file in the `src` folder (even if that files must be ignored).

  1. Errors and warnings are printed in the terminal and written verbosely in the file `TeXitEasy.src2prod.log` where `TeXitEasy` is the name extracted from the path `project`.


Only the source files to copy
-----------------------------

Sometimes the final product is not just a "selective clone" of the `src` folder: for example, it can be a melting of several source files in a single final one (the author of `src2prod` uses this technic to develop his `LaTeX` projects). In such a case, you can use the following method and attribut.

  1. The method `build` just looks for the files to keep for the `texiteasy` folder.

  1. The attribut `lof` is the list of all files to keep in the `src` folder (`lof` is for `list of files`).

Here is an example of code printing the list of only the source files to keep.

~~~python
from src2prod import *

project = Project(
    name   = 'TeXitEasy',
    source = Path('src'),
    target = Path('texiteasy'),
    ignore = '''
        tool_*/
        tool_*.*
    ''',
    usegit = True,
    readme = Path('README.md')
)

project.build()

for f in project.lof:
    print(f)
~~~

This script gives the following output in a terminal. Note that the list doesn't contain the path of the `README` file, this last one must be manage by hand (see the methods `check_readme` and `copy_readme` of the class `Project`).

~~~
/full/path/to/TeXitEasy/src/__init__.py
/full/path/to/TeXitEasy/src/escape.py
/full/path/to/TeXitEasy/src/LICENSE.txt
~~~


`README.md` part by part
------------------------

You can write you `README.md` typing small section like parts as it is the case for the `README.md` you are reading (that is both in the repository and the final project to be distributed). The `src2prod` project had merly the following partial tree structure on August 22, 2021.

~~~
+ src2prod
    + changes
        * ...

    + readme
        * about.peuf
        * build.md
        * cli.md
        * example-used.md
        * only-files.md
        * prologue.md
        * readme-splitted.md

    + src
        * ...

    * README.md
    * ...
~~~

This section has been written inside the file `readme-splitted.md`. The special file `about.peuf` allows to indicate the order to use to merge the different `MD` files. Its content was the following one.

~~~
toc::
    + prologue
    + example-used
    + build
    + only-files
    + readme-splitted
    + cli
~~~

The way used to build the source of `src2prod` is very simple: we just indicate the folder `readme` instead of a file for the argument `readme`. That's all! See the code below.

~~~python
from src2prod import *

project = Project(
    project = Path('TeXitEasy'),
    source  = Path('src'),
    target  = Path('texiteasy'),
    ignore  = '''
        tool_*/
        tool_*.*
    ''',
    usegit = True,
    readme = Path('readme')
)

project.update()
~~~


Using a `CLI`
-------------

The project proposes one `CLI`, aka one "Command Line Interface", to update a project. Let's consider the following script `mycli.py`.

~~~python
from src2prod import cmdline

cmdline.update()
~~~

The following `Unix` terminal session shows how to use this basic script to update a project.


### What we have before

~~~
> ls
spkpb         src2prod
ignore.txt    mycli.py

> cat ignore.txt
tool_*/
tool_*.*

> ls spkpb
README.md     src
changes       tools
~~~


### How to use the tiny script

~~~
> python mycli.py --usegit --notsafe --readme='README.md' --ignore='ignore.txt' spkpb
---------------
"spkpb": UPDATE
---------------

1) The log file used will be :
   "spkpb/spkpb.src2prod.log".
2) External "README" file to use:
   "spkpb/README.md".
3) Ignore rules in the file:
   "ignore.txt"
4) Checking "git".
5) Working in the branch "master".
6) Starting the analysis of the source folder:
   "spkpb/src".
7) 21 files found using the rules from "ignore".
8) Removing unwanted files using "git".
9) 10 files found using "git". 11 new files ignored thanks to "git".
10) Target folder has been created:
    "spkpb/spkpb".
11) Copying 10 files from source to target.
12) "README.md" added to the target.
13) Target folder updated.
~~~


### What we obtain after

~~~
> ls spkpb
README.md     spkpb.src2prod.log
src           changes
spkpb         tools

> ls spkpb/spkpb/*
spkpb/spkpb/LICENSE.txt        spkpb/spkpb/__init__.py
spkpb/spkpb/problems.py        spkpb/spkpb/README.md
spkpb/spkpb/base.py            spkpb/spkpb/timer.py

spkpb/spkpb/speaker:
__init__.py         log.py
term.py             allinone.py
spk_interface.py
~~~


### Help

You can have an help as usual in the `Unix` command line world.


~~~
> python mycli.py --help
Usage: cmdline.py [OPTIONS] PROJECT

  Update your "source-to-product" like projects using the Python module
  src2prod.

  PROJECT: the path of the project to update.

Options:
  --src TEXT     Relative path of the source folder of the project. The
                 default value is "src".

  --target TEXT  Relative path of the targer folder of the project. The
                 default value "", an empty string, indicates to use the name,
                 in lower case, of the project.

  --ignore TEXT  Path to a file with the rules for ignoring files in addition
                 to what git does. The default value "", an empty string,
                 indicates to not use any rule.

  --usegit       This flag is to use git.
  --readme TEXT  Relative path of an external "README" file or "readme"
                 folder. The default value "", an empty string, indicates to
                 not use any external "README" file.

  --notsafe      This flag allows to remove a none empty target folder.
  --help         Show this message and exit.
~~~