## __Neural Wrappers :: NWData__

### __Description__:

A generic high level API for Dataset management. Highly used side by side with NWModule projects.

### __How to install__:

1. Pip

```
pip install nwdata
```

2. Manual (for code tweaking and development)

Clone & Add the path to the root directory of this project in PYTHONPATH environment variable.

```
git clone https://gitlab.com/neuralwrappers/nwdata /path/to/nwdata
vim ~/.bashrc
(append at end of file)
export PYTHONPATH="$PYTHONPATH:/path/to/nwdata/
```

### __Structure of this project__:
- README.md - This file
- examples/ - Some examples on how to use the library. TODO: Add examples.
- nwdata/ - Core implementation
- test/ - Unit tests. To run use `python -m pytest .` inside the directory.
