# MeetUp 192 - Beginners Python and Machine Learning - Wed 18 Oct 2023 - Windows install of vscode, git, pyenv, pdm

Links:

- Youtube: <https://youtu.be/w94A6TU9Q6Y>
- Github:  <https://github.com/timcu/bpaml-sessions/raw/master/online/meetup192_tim_vscode_git_pyenv_pdm_for_windows.md>
- Github:  <https://github.com/Oracen/python-intro>
- Meetup:  <https://www.meetup.com/beginners-python-machine-learning/events/296628481/>

References:

References

- <https://github.com/Oracen/python-intro>  # Original script used during BPAML in-person session
- <https://git-scm.com>  # Git source code manager
- <https://pdm.fming.dev/latest/>  # Python Dependency Manager
- <https://github.com/pyenv/pyenv>  # pyenv not officially supported on windows
- <https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md>  # fork of pyenv to work on windows without wsl
- <https://github.com/pyenv-win/pyenv-win/wiki>

Learning objectives:

- Repeat of in-person session of 27 Sep 2023 but just for Windows and without requiring administrator access
- Install Microsoft Visual Studio Code as an Integrated Development Environment (IDE)
- Install Git (and Git Bash) for collaborating with others using a source code repository
- Install pyenv-win (Windows fork of pyenv) for installing multipled versions of Python at the same time
- Install pdm for managing dependencies and virtual environments (more advanced than `python -m venv` and `pip`, more standard than poetry and anaconda)

@author D Tim Cummings

Install in C:\Users\pytho\AppData\Local\Programs\Git

## Microsoft Visual Studio Code

Install Visual Studio Code from Microsoft Store

## Git source code manager

Install Git from <https://git-scm.com/download/win>

- 64-bit Git for Windows Setup
- Should install in $HOME\AppData\Local\Programs\Git if installing for this user with no admin access.
- Use Visual Studio Code as Git's default editor
- Accept all other defaults

Run Git Bash and paste following code (Shift-Insert)

```bash
mkdir --parents ~/projects
cd ~/projects
git clone https://github.com/Oracen/python-intro.git
cd python-intro
ls .
```

Run VSCode from python-intro directory (from Git Bash or PowerShell or Command Prompt)

```bash
code .
```

## pyenv-win - fork of pyenv for Windows

Need to check if Windows PowerShell will let you run scripts (default is Restricted which means you can't).

Go to PowerShell terminal in VSCode (Ctrl-`)

In shells, the path is the list of directories where the shell will look for programs to run. For example in PowerShell:

```powershell
echo $Env:Path
```

Check execution policies in PowerShell

```powershell
Get-ExecutionPolicy -List
```

Shows in order of precedence. First one not undefined wins.
https:/go.microsoft.com/fwlink/?LinkID=135170 shows list of policies
AllSigned Bypass Default RemoteSigned Restricted Undefined Unrestricted


Set the execution policy required to run a script on Process so it is temporary while this PowerShell is open.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Install pyenv-win using PowerShell

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

Check installation

```powershell
pyenv --version
```

Open Git Bash terminal in VSCode or start a new Git Bash in Windows and run the script to build `.bashrc` and `.bash_profile`. Note that, in Git Bash, these files will not have the execute permission set so need to run with the `source` command. To save typing you can use the bash abbreviation `.` instead of `source`. Note that because pyenv and pyenv-win are slightly different, we need different `.bash_profile` for pyenv-win.

```bash
. ~/projects/python-intro/bootstrap/bash-pyenv-win-profile.sh
```

From new Git Bash terminal in VSCode

```bash
pyenv install 3.10.11
pyenv local 3.10.11
python --version
```

The `pyenv global 3.a.b` command creates a file `~/.python-version`. You can override this with `pyenv local 3.c.d` which creates a file in the current directory for the current application, as we have done here. This can be further overridden by `pyenv shell 3.e.f` which creates a shell variable `PYENV_VERSION`. If a file called `.python-version` does not exist in the current directory, pyenv will start checking parent directories until it finds the file. If no file is found then the system python is used.

Don't run `pyenv install -l` unless you have plenty of spare time as it crawls the python website.

In shells, the path is the list of directories where the shell will look for programs to run. For example in bash:

```bash
echo $PATH
```

## pdm - Python Dependency Manager

Install pdm. This only works from Git Bash, not PowerShell

```bash
curl -sSL https://pdm.fming.dev/install-pdm.py | python -
pdm --version
```

On my computer it installed pdm in C:\Users\pytho\AppData\Roaming\Python\Scripts\pdm.exe

## running demo streamlit app

Build python-intro app. Remember pdm only works in Git Bash, not PowerShell.

```bash
pdm install  # from the python-intro directory

pdm start-demo  # http://localhost:8501
```

Stop later using ctrl-c or killing the terminal window.

## running complex demo streamlit app

Try different version of app in branch

```bash
git switch feature/complex-app
pdm start-demo
```

## Uninstalling

Uninstall pdm using Git Bash with `--remove` at the end.

```bash
curl -sSL https://pdm.fming.dev/install-pdm.py | python - --remove
```

Uninstall pyenv-win using Powershell with `-Uninstall` at the end.

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1 -Uninstall"
```

Uninstall git from Settings > Apps > Git > Uninstall

Uninstall VSCode from Settings > Apps > Microsoft Visual Studio Code > Uninstall

Delete ~/.bashrc and ~/.bash_profile if they were not there before. PYENV_ROOT is in first line added by this procedure so if it is in the first line you can delete the whole file.
