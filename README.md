# Codeforces Toolbox

![Last commit](https://img.shields.io/github/last-commit/mdbrnowski/codeforces-toolbox)
![Issues](https://img.shields.io/github/issues/mdbrnowski/codeforces-toolbox)
![License](https://img.shields.io/github/license/mdbrnowski/codeforces-toolbox)

This tool is a CLI (Command Line Interface) that makes writing [Codeforces](https://codeforces.com/) contests more efficient.

***Note***: At the moment only C++ is supported.

## Features

* Create files based on the specified template. These files will be named appropriately for the contest, for example 1000A, 1000B1, 1000B2, 1000C.
* Download sample test from Codeforces.
* Compile solution and test it.
* Submit solution and get the verdict.


### Template, login, password, compilation command

`cft config`

```
Choose one of the following (type an integer):
  1. change the template file
  2. change username and password
  3. change password
  4. set compile command
```
then you can just type an integer (1-4) and change your template file, username, password or compile command.

### Creating structure for a contest

`cft race 1234` creates the following directory structure:

```
1234
├─ 1234A.cpp
├─ 1234B.cpp
├─ 1234C.cpp
├─ 1234D.cpp
├─ 1234E.cpp
├─ 1234F.cpp
├─ 1234G.cpp
```

files 1234*X*.cpp are created by copying the previously specified template file.

It is recommended that you then change the current working directory (`cd 1234`) to operate more smoothly later.

### Testing solution

`cft test 1234A` compiles your solution, downloads (if not yet downloaded) example test and checks if it passes.

If your current working directory is `some\path\1234` you can type just `cft test A`.

Test will be downloaded only if directories `\in` and `\ans` are empty or do not exist. You can force download test from Codeforces by using `cft test A -d` or `cft test A --download`.

### Submitting solution

`cft submit 1234A` submits solution and returns judgement verdict.

If your current working directory is `some\path\1234` you can type just `cft submit A`. 

## Installation

Please first install Python 3.7 or higher from [python.org](https://www.python.org/downloads/).

Then just copy and paste in your terminal
```commandline
pip install codeforces-toolbox
```

## Contribution & bugs

If you want to contribute to the project, fork this repository and open a new PR. If you have any questions or suggestions, email me (you can find my email address at my profile page) or create an issue.
