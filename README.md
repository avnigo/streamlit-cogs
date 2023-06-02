# Streamlit: COG Visualization

Web app for visualizing and labeling COGs.

# Setup

1. If `GDAL` libraries are not on the system, `conda` is the simplest way to install them:

```console
$ conda env create -f streamlit-cogs.yml
```

- If `GDAL` libraries are available, skip to step (3), but it's a good idea to create a virtual environment:

```console
$ python -m venv venv && source vevn/bin/activate # on Unix
```

2. Activate the newly created environment:

```console
$ conda activate streamlit_cogs
```

3. From inside the directory that includes the `pyproject.toml` file:

```console
$ python -m pip install .
```

# Server Usage

```console
$ streamlit run streamlit-cogs/main.py
```

## Running and Deployment

- If run locally, this may open the browser at the `URL:port` given, otherwise a network URL is given if it is reachable.
- For actual deployment options, Streamlit apps are easily dockerizable, or for more public apps, they can be deployed straight to Streamlit Community Cloud through GitHub.

# Web App Usage

- Choose from the preloaded imagery, grouped together by date (`All`), or select an individual layer only.
  - Layers can also be toggled on and off from the map view by clicking on the top right button.
- _Adding URLs_: Other COG URLs may also be added manually in the appropriate text input box; separate by a `|` if adding multiple. Make sure to click `Submit changes` to load the new URLs.
- _Band ordering:_ Depending on the COG, the bands may be out of order, so they can be reordered using the multi-select box, and clicking `Submit changes`. It's also possible to inspect one or two bands individually by only including the ones needed.
- _Rescaling:_ To change the contrast levels of the displayed bands, they can be rescaled in the `Band rescaling` section. The default values are preloaded with the COG metadata min/max values. After the appropriate band min/max values are edited, click `Rescale bands` to add the bands as layers to the map view.
- _Labeling:_ The map view provides multiple labeling tools on the left-hand side. Clicking a drawn object on the map will open a popup of its GeoJSON object representation, while clicking on the `Export` button in the top right downloads a GeoJSON file with all the drawn objects.
