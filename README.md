# Codeforces Toolbox

[![Status PyPI](https://img.shields.io/pypi/status/codeforces-toolbox)](https://pypi.org/project/codeforces-toolbox/)
[![Version PyPI](https://img.shields.io/pypi/v/codeforces-toolbox)](https://pypi.org/project/codeforces-toolbox/)
[![Last commit](https://img.shields.io/github/last-commit/mdbrnowski/codeforces-toolbox)](https://pypi.org/project/codeforces-toolbox/)
[![License PyPI](https://img.shields.io/pypi/l/codeforces-toolbox)](https://pypi.org/project/codeforces-toolbox/)

This tool is a CLI (Command Line Interface) that makes writing [Codeforces](https://codeforces.com/) contests more efficient.

## Features

* Create files based on the specified template. These files will be named appropriately for the contest, for example 1000A, 1000B1, 1000B2, 1000C.
* Download sample test from Codeforces.
* Compile solution and test it.
* Submit solution
* Wait for the verdict

Supported languages: C++, C, Python, Java, Kotlin, Rust, C#, Go.


### Settings configuration

`cft config`

```
Choose one of the following (type an integer):
  1. change the template file
  2. change username and password
  3. change programming language
  4. set compile command
  5. set run command
```
then you can just type an integer (1-5) and change your template file, username and password, language, run or compilation command.

See the FAQ at the bottom of this page.

### Creating structure for a contest

`cft race 1234` creates the following directory structure (provided that your programming language is C++):

```
1234/
  1234A.cpp
  1234B.cpp
  1234C.cpp
  1234D.cpp
  1234E.cpp
  1234F.cpp
  1234G.cpp
```

files 1234*X*.cpp are created by copying the previously specified template file.

It is recommended that you then change the current working directory (`cd 1234`) to operate more smoothly later.

You can also enter a task name (e.g. `cft race 1234X`) instead of a contest name, in which case a single file will be created.

### Testing solution

`cft test 1234A` compiles your solution, downloads (if not yet downloaded) example test and checks if it passes.

If your current working directory is `some/path/1234` you can type just `cft test A`.

If your answer uses floating point numbers you can determine what error will be acceptable by using `-p` or `--precision` flag.
```commandline
cft test 1495A -p 1e-9
cft test 1495A --precision 1e-9
```

### Submitting solution

`cft submit 1234A` submits solution and returns judgement verdict.

If your current working directory is `some/path/1234` you can type just `cft submit A`. 

## Installation

Please first install Python 3.7 or higher from [python.org](https://www.python.org/downloads/). During installation, you should check the option *'Add Python to PATH'*.

Then just copy and paste in your terminal this:
```commandline
pip install codeforces-toolbox
```

If you want to upgrade the package, you can do this by:
```commandline
pip install --upgrade codeforces-toolbox
```
The program will automatically check if there is a new version and try to install it if you run `cft` without any arguments or `cft config`.

If `pip` command is not found you can use `pip3 install codeforces-toolbox` or `python3 -m pip install codeforces-toolbox`. 

## Contribution & bugs

If you want to contribute to the project, fork this repository and open a new PR. If you have any questions or suggestions, email me (you can find my email address at my profile page) or create an issue.

## FAQ

> My favorite language is not supported!

Well, that is not a question, nevertheless I encourage you to create an issue in the repository.

> _Compile command_, _run command_ – what is this?

_Compile command_ is the command you would use to compile your solution. For example: in C++ it can be `g++ -Wall`, in Java `javac`, in Kotlin `kotlinc-native`, in Rust `rustc`, in C# `csc`, in Go `go build`. Note that Python does not have a corresponding compiler because it is an interpreted language.

_Run command_ is the command you would use to run your solution. If you are using a language that compiles to machine code that your operating system can run, you don't need this command. Otherwise, if you are using Python this can be `python`, `python3`, `py`, `pypy`. In the case of Java, it is probably `java`.

I assume that your compiler/interpreter is added to the PATH environment variable. If it is not, add it, or provide an absolute path, e.g. `C:\Users\user\AppData\Local\Programs\Python\Python39\python.exe` instead of just `python`.