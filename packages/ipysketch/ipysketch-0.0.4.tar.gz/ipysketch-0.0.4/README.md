# ipysketch

A Python package for handwriting and sketching in Jupyter notebooks.

## Installation

First, install the *ipysketch* package using *pip*:

```
pip install --upgrade ipysketch
```

Then install and enable the widgets extension in Jupyter:

```
jupyter nbextension install --user --py widgetsnbextension
jupyter nbextension enable --py widgetsnbextension
```

## Usage

In a Jupyter notebook:

```
from ipysketch import Sketch
```

