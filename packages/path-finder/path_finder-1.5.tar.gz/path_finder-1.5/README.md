### Context
* Created: September 2020
* Author: Renier Kramer, renier.kramer@hdsr.nl
* Python version: >3.5

### Description
A python project that serves as an interface for finding directories and files by 
combining best of both worlds: glob/rglob (speed) and regex (flexibility).

### Usage path_finder.FileFinder
```
# pip install path-finder
# pip install pathlib
from pathlib import Path
from path_finder import FileFinder

start_dir1          = Path('start_search_from_this_dir')
start_dir2          = Path('and_start_search_from_this_dir')
limit_depth         = True
depth               = 2  # 2, so search in start_dir1, subdir and subsubdirs (same for start_dir2) 
filename_regex      = '^[0-9]{8}_blabla'
extension           = '.csv'  # choose from ('.jpg', '.png', '.txt', '.xml', '.csv', '.xlsx', '.pdf', '.h5', '.nc', '.zip')   

file_finder = FileFinder(
    multi_start_dir=[start_dir1, start_dir2],
    extension=extension,
    limit_depth=True,                   
    depth=depth,
    filename_regex=filename_regex
)
                    
paths = file_finder.paths  # returns a List[Path]
paths_empty_files = file_finder.paths_empty_file  # returns a List[Path]
```

### Usage path_finder.DirFinder
```
# pip install path-finder
# pip install pathlib
from pathlib import Path
from path_finder import DirFinder

dir_finder = DirFinder(
    single_start_dir=Path('start_search_from_this_dir')
    exclude_empty_dirs=True,
    limit_depth=True,
    depth=0,  # so only search in single_start_dir
)

paths = dir_finder.paths  # returns a List[Path]
paths_empty_files = dir_finder.paths_empty_file  # returns a List[Path]
```

### License 
[MIT][mit]

### Releases
[PyPi][pypi]

### Contributions
All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
Issues are posted on: https://github.com/hdsr-mid/path_finder/issues

[pypi]: https://pypi.org/project/path-finder/
[mit]: https://github.com/hdsr-mid/path_finder/blob/main/LICENSE.txt

### Test coverage (release v1.4)
```
---------- coverage: platform win32, python 3.7.10-final-0 -----------
Name                         Stmts   Miss  Cover
------------------------------------------------
path_finder\__init__.py          2      0   100%
path_finder\base.py             47     13    72%
path_finder\dir_finder.py       65     11    83%
path_finder\file_finder.py      61      1    98%
setup.py                        10     10     0%
------------------------------------------------
TOTAL                          185     35    81%
```

### Conda general tips
#### Build conda environment (on Windows) from any directory using environment.yml:
```
> conda env create --name <conda_env_name> --file <path_to_project>/environment.yml python=<python_version>
> conda info --envs  # verify that <conda_env_name> is in this list 
```
#### Start the application from any directory:
```
> conda activate <conda_env_name>
At any location:
> (<conda_env_name>) python <path_to_project>/main.py
```
#### Test the application:
```
> conda activate <conda_env_name>
> cd <path_to_project>
> pytest  # make sure pytest is installed (conda install pytest)
```
#### List all conda environments on your machine:
```
At any location:
> conda info --envs
```
#### Delete a conda environment:
```
Get directory where environment is located 
> conda info --envs
Remove the enviroment
> conda env remove --name <conda_env_name>
Finally, remove the left-over directory by hand
```
#### Write dependencies to environment.yml:
The goal is to keep the .yml as short as possible (not include sub-dependencies), yet make the environment 
reproducible. Why? If you do 'conda install matplotlib' you also install sub-dependencies like pyqt, qt 
icu, and sip. You should not include these sub-dependencies in your .yml as:
- including sub-dependencies result in an unnecessary strict environment (difficult to solve when conflicting)
- sub-dependencies will be installed when dependencies are being installed
```
> conda activate <conda_env_name>

Recommended:
> conda env export --from-history --no-builds | findstr -v "prefix" > --file <path_to_project>/environment_new.yml   

Alternative:
> conda env export --no-builds | findstr -v "prefix" > --file <path_to_project>/environment_new.yml 

--from-history: 
    Only include packages that you have explicitly asked for, as opposed to including every package in the 
    environment. This flag works regardless how you created the environment (through CMD or Anaconda Navigator).
--no-builds:
    By default, the YAML includes platform-specific build constraints. If you transfer across platforms (e.g. 
    win32 to 64) omit the build info with '--no-builds'.
```
#### Pip and Conda:
If a package is not available on all conda channels, but available as pip package, one can install pip as a dependency.
Note that mixing packages from conda and pip is always a potential problem: conda calls pip, but pip does not know 
how to satisfy missing dependencies with packages from Anaconda repositories. 
```
> conda activate <conda_env_name>
> conda install pip
> pip install <pip_package>
```
The environment.yml might look like:
```
channels:
  - defaults
dependencies:
  - <a conda package>=<version>
  - pip
  - pip:
    - <a pip package>==<version>
```
You can also write a requirements.txt file:
```
> pip list --format=freeze > <path_to_project>/requirements.txt
```
