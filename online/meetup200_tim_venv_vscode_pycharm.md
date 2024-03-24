# MeetUp 200 - Beginners Python and Machine Learning - Wed 03 Apr 2024 - Windows install of venv, git, vscode, pycharm

Links:

- Youtube: <https://youtu.be/sYSwLQhHYXA>
- Github:  <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup200_tim_venv_vscode_pycharm.md>
- Meetup:  <https://www.meetup.com/beginners-python-machine-learning/events/299977463/>

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

Create and activate a Python virtual environment.

```commandprompt
mkdir %HOMEPATH%\bpaml200
cd %HOMEPATH%\bpaml200
py -m venv venv200
venv200\Scripts\Activate.bat
```

If you are using an Anaconda installation rather than Python then use `conda create` in an Anaconda shell. The 'python' at the end of the command specifies a minimal virtual environment.

```commandprompt
conda create --name venv200 python
conda activate venv200
conda install python-dotenv
```

## Microsoft Visual Studio Code

Install Visual Studio Code from Microsoft Store or <https://code.visualstudio.com>

## Git source code manager

Install Git from <https://git-scm.com>

Install the portable version if you don't have administrator rights. I installed it in %HOMEPATH%\Apps folder and then "edit environment variables for your account" in control panel to add the "cmd" folder to `Path`

## Creating a virtual environment in bash or zsh

Run bash (on Windows with Git Bash, or Mac/Linux with Terminal) and type the following code as required.

```bash
mkdir ~/bpaml200                 # create directory with its parents
cd ~/bpaml200                    # change into that directory
python3 -m venv venv200          # create a virtual environment (common name would be .venv)
source venv200/bin/activate      # activate the virtual environment  Mac/Linux
source venv200/Scripts/activate  # activate the virtual environment  Windows
pip list                         # see what third party libraries are installed
pip install --upgrade pip        # upgrade pip to latest version
pip install python-dotenv        # install a third party library from https://pypi.org
pip list                         # see list
deactivate                       # stop using the virtual environment
```

## Clone repository from Git Bash

```bash
git clone https://github.com/arunslb123/anthropic_claude3_masterclass.git
```

## Running VS Code

- Run VS Code. VS Code has concept of folders for a project.
- Open folder "bpaml200".
- Trust the author in this case.
- New install of VS Code will have no extensions.
- Create a new file called "hello.py" in bpaml200
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

The Python extension will try to activate a virtual environment if it finds the one we created earlier "venv200". Notice the name of the virtual environment down in the bottom right, next to the Python version. You can click on the venv name to select or create a different virtual environment.

Let's create a new virtual environment called .venv. VS Code Python doesn't give you a choice when create venv but does let you select one a differently named one created by other means. It will also let you create an Anaconda virtual environment.

Starting new Terminal in VS Code gives warning that the virtual environment name may not show.

Now try opening the first `ipynb` file in the git repository. In the top right corner it asks for kernel to run the jupyter notebook. First it will suggest installing the Jupyter extension. Then install the kernel into the active virtual environment. Now try running the cells in the jupyter notebook including the ones to install anthropic libraries in virtual environment.

Another way start VS Code is to navigate to the folder in the command line and then type `code .`. If you activate the virtual environment first, VS Code will use that environment

```bash
cd ~/bpaml200
source venv200/Scripts/activate
code .
```

## Install PyCharm Community Edition

<https://www.jetbrains.com/pycharm/download/> and scroll down to Community Edition

When installing you can say No to elevating privileges and it will install for just that user.

## Virtual environments in PyCharm

PyCharm comes with virtual environment support out of the box.

- Open bpaml200 as a project.
- Check virtual environment in File > Settings > Project > Python Interpreter.
- Also check "Python Packages" view which tells you which packages can be upgraded.
- Create a file called "requirements.txt" which lists which packages are required.
- Version numbers can be specified in "requirements.txt"

```bash
pip freeze >> requirements.txt
```

Now edit "python-dotenv==1.0.0" and downgrade python-dotenv. "Python Packages" will show that is can be upgraded.

Now try opening Jupyter Notebook. PyCharm Community Edition gives a read-only view of the notebook. You need PyCharm Professional to do more with the notebook.

## Building applications to install in virtual environments

See <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup168_tim_build_wheel_with_pyproject_and_setuptools.md>
