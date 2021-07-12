# Codeforces tool

This tool is created for the purpose of participation in contests on Codeforces and for writing solutions for Codeforces problems more efficiently in general.

## Usage

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
  A/
    1234A.cpp
  B/
    1234B.cpp
  C/
    1234C.cpp
  D/
    1234D.cpp
  E/
    1234E.cpp
  F/
    1234F.cpp
  G/
    1234G.cpp
```

files 1234*X*.cpp are created by copying the previously specified template file.


_**Other functionalities are in progress and will be released in a few days (hopefully).**_

## Contribution & bugs

If you want to contribute to the project, fork this repository and open a new PR. If you have any questions or suggestions, email me (you can find my email address at my profile page) or create an issue.
