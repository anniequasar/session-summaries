# MeetUp 219 - Beginners Python and Machine Learning - Wed 06 Aug 2025 - Windows install of venv, git, vscode, pycharm

Links:

- Youtube: <https://youtu.be/JA4Sbgqb8aA>
- Github:  <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup219_tim_venv_vscode_pycharm.md>
- Meetup:  <https://www.meetup.com/beginners-python-machine-learning/events/310203410/>

References:

- <https://python.org>  Python
- <https://code.visualstudio.com>  Visual Studio Code
- <https://git-scm.com>  Git source code manager
- <https://jetbrains.com/>  PyCharm IDE
- <https://docs.python.org/3/tutorial/venv.html>  Python Virtual Environments

Learning objectives:

- How and why to create virtual environments (Python or Anaconda)
- How to run Python scripts on the command line, VS Code, and PyCharm
- How to clone a git repository
- How to run Jupyter notebooks in VS Code

Related sessions:

- <https://github.com/timcu/bpaml-sessions/raw/master/online/meetup192_tim_vscode_git_pyenv_pdm_for_windows.md>  More advanced virtual environment with ability to specify python versions.

@author D Tim Cummings

## Install Python

Install Python for local user from <https://python.org>

Create and activate a Python virtual environment in Windows.

Windows Command Prompt

```commandprompt
mkdir %HOMEPATH%\bpaml219
cd %HOMEPATH%\bpaml219
py -m venv venv219
venv219\Scripts\Activate.bat
```

Windows Power Shell

```powershell
mkdir $env:USERPROFILE\bpaml219
cd $env:USERPROFILE\bpaml219
py -m venv venv219
Get-ExecutionPolicy -List
# If you can't activate venv then you might need to set execution policy. Remember to set back when finished today so you don't have unintended consequences
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#Set-ExecutionPolicy -ExecutionPolicy undefined -Scope CurrentUser
venv219\Scripts\Activate.bat
```

Linux or Mac, bash or zsh

```bash
mkdir ~/bpaml219
cd ~/bpaml219
python3 -m venv venv219
venv219/bin/activate
```

If you are using an Anaconda installation rather than Python then use `conda create` in an Anaconda shell. The 'python' at the end of the command specifies a minimal virtual environment.

```commandprompt
conda create --name venv219 python
conda activate venv219
conda install python-dotenv
```

## Microsoft Visual Studio Code

Install Visual Studio Code from Microsoft Store or <https://code.visualstudio.com>

## Git source code manager

Install Git from <https://git-scm.com>

Install the portable version if you don't have administrator rights. I installed it in %HOMEPATH%\Apps folder and then "edit environment variables for your account" in control panel to add the "cmd" folder to `Path`

## Installing a third party library from pypi.org

Use `pip` which is short for "Pip installs packages"

```bash
pip list                         # see what third party libraries are installed
pip install --upgrade pip        # upgrade pip to latest version
pip install python-dotenv        # install a third party library from https://pypi.org
pip list                         # see list
deactivate                       # stop using the virtual environment
```

## Clone repository from Git Bash into bpaml219 directory

```bash
git clone https://github.com/timcu/bpaml-sessions.git
```

## Running VS Code

- Run VS Code. VS Code has concept of folders for a project.
- Open folder "bpaml219".
- Trust the author in this case.
- New install of VS Code will have no extensions.
- Create a new file called "hello.py" in bpaml219
- VS Code will recommend installing "Python" extension from Microsoft for the Python language - Click "Install".
- Enter the following code into "hello.py"

```python
'Find which Python executable is running this script'
import sys
print(sys.version)
print(sys.executable)
```

Run the script using the triangle play button.

## Virtual environments in VS Code

The Python extension will try to activate a virtual environment if it finds the one we created earlier "venv219". Notice the name of the virtual environment down in the bottom right, next to the Python version. You can click on the venv name to select or create a different virtual environment.

Let's create a new virtual environment called .venv. VS Code Python doesn't give you a choice when create venv but does let you select a differently named one created by other means. It will also let you create an Anaconda virtual environment.

Starting new Terminal in VS Code used to give warning that the virtual environment name may not show. I think this has been fixed now.

Now try opening the file `online/meetup211_tim_colab_introduction.ipynb` file in the git repository. In the top right corner it asks for kernel to run the jupyter notebook. First it will suggest installing the Jupyter extension. Then install the kernel into the active virtual environment. Now try running the cells in the jupyter notebook including the ones to install libraries in virtual environment. Use `pip list` to see which libraries are installed at different stages of the process. You won't be able to run commands that require ubuntu, such as bash commands `cat`, `free`, `df`, `echo`, `whoami`, `apt`, `source`, `ls`, `head`. You can't install detectron2 which requires Mac or Linux. You can't mount google drive which requires colab. 

Another way start VS Code is to navigate to the folder in the command line and then type `code .`. If you activate the virtual environment first, VS Code will use that environment

Windows Powershell

```powershell
cd $env:USERPROFILE\bpaml219
venv219\Scripts\Activate.ps1
code .
```

Windows Command Prompt

```commandprompt
cd %USERPROFILE%\bpaml219
venv219\Scripts\Activate.bat
code .
```

Mac or Linux, `bash` or `zsh`

```bash
cd ~/bpaml219
source venv219/Scripts/activate
code .
```

## Install PyCharm Unified Edition

<https://www.jetbrains.com/pycharm/download/> 

When installing you can say No to elevating privileges and it will install for just that user.

## Virtual environments in PyCharm

PyCharm comes with virtual environment support out of the box.

- Open bpaml219 as a project.
- Check virtual environment in File > Settings > Python > Interpreter.
- Also check "Python Packages" view which tells you which packages can be upgraded.
- Create a file called "requirements.txt" which lists which packages are required.
- Version numbers can be specified in "requirements.txt"

```bash
pip freeze >> requirements.txt
```

Now edit "python-dotenv==1.0.0" and downgrade python-dotenv. "Python Packages" will show that it can be upgraded.

Now try opening Jupyter Notebook. PyCharm without the pro upgrade gives a read-only view of the notebook. You need PyCharm Pro to do more with the notebook.

## Building applications to install in virtual environments

See <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup168_tim_build_wheel_with_pyproject_and_setuptools.md>
