# MeetUp 168 - Beginners Python and Machine Learning - Wed 28 Dec 2022 - Build wheel with pyproject and setuptools

Links:
- Youtube: https://youtu.be/f85VxNVxnrg
- Github:  https://github.com/timcu/session-summaries/raw/master/online/meetup168_tim_build_wheel_with_pyproject_and_setuptools.md
- Github:  https://github.com/timcu/bpaml-prime-minister
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/290400069/

Learning objectives:
- Learn the new and recommended pyproject.toml way of configuring build systems and other project metadata
- Package a Python project into a wheel
- Install wheel into virtual environment using pip

@author D Tim Cummings

### Set up using IDE

- Install Python 3.11 from https://www.python.org/downloads/
  - (3.9 or later should be fine, anaconda also fine) 
- Install Git 2.37.1 from https://git-scm.com/download/
- Install IDE e.g. PyCharm Community Edition 2022.3 from https://www.jetbrains.com/pycharm/download/
- Run PyCharm
- Clone repository and setup virtual environment
- Check out `pyprojecttoml`
- Follow instructions in `BUILDING.md` which are repeated below


## Packaging using pyproject.toml with setuptools
As described in https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html

References
 - https://toml.io/en/  - Tom's obvious minimal language
 - https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/
 - https://peps.python.org/pep-0517/  - format for source tree independent of build systems
 - https://peps.python.org/pep-0518/  - specifying build system
 - https://peps.python.org/pep-0621/  - project metadata
 - https://peps.python.org/pep-0660/  - editable installs

0. Start this exercise from the `pyprojecttoml` branch in a new branch called `bpaml168`. The solution of all the exercises is in a branch called `pyprojecttomlsoln`
```shell
git checkout pyprojecttoml
git checkout -b bpaml168
```
This branch has renamed `setup.py` to `setup.txt` so that it doesn't interfere with `pyproject.toml`.
1. Add build module to requirements.txt
2. Create a pyproject.toml file in project root directory.
3. Add dependencies to `[project]` table of pyproject.toml from requirements.txt. If you are building a library then don't overly specify dependency versions because that can lead to conflicts. 
```toml
[project]
dependencies = [
    "flask",
    "flask_bootstrap",
    "python-dotenv",
]
```
4. Specify a `[build-system]` table. If missing, defaults to
```toml
[build-system]
requires = ["setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta:__legacy__"
```
Python building from pyproject.toml provides an isolated build system which can have different requirements to runtime requirements. 
Our build system should use `setuptool.build_meta` but without the `__legacy__` attribute. 
It requires `setuptools`, `wheel` but good idea to specify later versions 65.6.3 and 0.38.4. Specifying versions here is 
OK because they are only used on the building system and are isolated.

5. Specify which data is dynamic in the `[project]` table. We will just specify `dynamic = ["version"]` but could also include `classifiers`, `description`, `entry-points`, `scripts`, `gui-scripts` and `readme`
6. Tell setuptools where to find package (and exclude any tests from packaged product).
```toml
[tool.setuptools.packages.find]
exclude = ["tests*"]
include = ["prime_minister*"]
```
7. Build package
```shell
python -m build
```
8. Note that version incorrectly used. Add a `table` section called `[tool.setuptools.dynamic]` saying where to get the version number and rebuild.
```toml
[tool.setuptools.dynamic]
version = {attr = "prime_minister.version.VERSION"}
```
```shell
rm -R dist prime_minister.egg-info
python -m build
```
9. Use an additional tool in build system to add version number from git tag. 
```toml
[build-system]
requires = ["setuptools>=65.6.3", "wheel>=0.38.4", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[tool.setuptools_scm]
write_to = "prime_minister/version.py"
```
You can also remove the `tool.setuptools.dynamic` table. Build another wheel and notice version number. It shows a dirty version number because it includes uncommitted code. 
10. Create a new branch and commit all your code and create a new tag then rebuild.
```shell
git checkout -b bpaml168
git commit -a -m "Implement pythons new recommended build system pyproject.toml and setuptools"
git tag "1.168.10"
rm -R dist prime_minister.egg-info
python -m build
```
11. Notice the naming convention of the wheel `{distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl`. 
```text
    distribution = package name = prime_minister
    version = package version = 1.168.10
    build tag = extra information about build = N/A
    python tag = which implementation of python it runs on = py3 = any python 3 implementation (not python 2)
    abi tag = application binary interface = none which means ABI is not a factor (usually only a factor if compiled C code included)
    platform tag = operating system = any (Mac, Windows, Linux, ...)
```
12. Install the created wheel in your own virtual environment
Windows
```commandline
py -m venv bpaml168venv
bpaml168venv\Scripts\Activate.bat
pip install prime_minister-1.168.10-py3-none-any.whl
```
Mac or Linux
```shell
python3 -m venv bpaml168venv
source bpaml168venv/bin/activate
pip install prime_minister-1.168.10-py3-none-any.whl
```
Anaconda
```commandline
conda create --name bpaml168venv python
conda activate bpaml168venv
pip install prime_minister-1.168.10-py3-none-any.whl
```
13. Notice how if you reinstall, it will uninstall the previous install and install the new wheel. If any dependencies have been updated the new dependencies will get installed. 
14. In your virtual environment, run the application
```shell
flask --app prime_minister init-db
flask --app prime_minister run
```
15. Add other information from `setup.txt` to `pyproject.toml`
```toml
[project]
name = "bpaml_prime_minister"
authors = [
    {name = "D Tim Cummings", email = "tim@triptera.com.au"},
]
description = "Demo flask web app listing prime ministers of Australia"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.9"
keywords = ["flask", "bpaml", "pm"]

classifiers =[
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython", 
    "License :: OSI Approved :: MIT License",
    "Framework :: Flask",
    "Intended Audience :: Education",
    "Intended Audience :: Developer",
    "Natural Language :: English",
    "Topic :: Education",
]

[project.urls]
repository = "https://github.com/timcu/bpaml-prime-minister"
```
