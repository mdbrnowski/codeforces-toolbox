# Codeforces tool

This tool is created for the purpose of participation in contests on Codeforces and for writing solutions for Codeforces problems more efficiently in general.

## Usage

`cft -h`

```
usage: cft [-h] {race,submit,test,config} ...

Codeforces tool

positional arguments:
  {race,submit,test,config}
    race                create folder and solution files based on the template
    submit              submit solution
    test                test the solution file
    config              change configuration of the cft

optional arguments:
  -h, --help            show this help message and exit

Wish you high ratings!
```

### Template, login, password

`cft config`

```
Choose one of the following (type an integer):
  1. change the template file
  2. change username and password
  3. change password
```
then you can just type an integer (1-3) and change your template file, username or password.

### Creating structure for a contest

`cft race 1234` creates the following directory structure:

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

### Testing solution

`cft test 1234A` downloads (if not yet downloaded) example test and check if it passes. Your solution should be already compiled.

If your current working directory is `some\path\1234` you can type just `cft test A`. 


_**Other functionalities are in progress and will be released in a few days (hopefully).**_

## Contribution & bugs

If you want to contribute to the project, fork this repository and open a new PR. If you have any questions or suggestions, email me (you can find my email address at my profile page) or create an issue.
