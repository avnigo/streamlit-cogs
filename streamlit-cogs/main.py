import streamlit as st
import leafmap.foliumap as leafmap

import tomllib

from pathlib import Path


def add_to_map(
    m: leafmap.Map,
    urls: list[str],
    bands=None,
    labels=None,
    rescale=None,
    autoscale=True,
):
    if not labels:
        labels = [Path(url).name for url in urls]

    for url, label in zip(urls, labels):
        # Get bands and reverse order (BGR)
        if not bands:
            bands = leafmap.cog_bands(url)[::-1]

        # For clean state or autoscale override
        if "rescale" not in st.session_state or autoscale:
            meta = leafmap.cog_stats(url)
            print(meta)
            print(meta.keys())
            st.session_state["meta"] = meta
            st.session_state["rescale"] = [
                f"{meta['b3']['min']},{meta['b3']['max']}",
                f"{meta['b2']['min']},{meta['b2']['max']}",
                f"{meta['b1']['min']},{meta['b1']['max']}",
            ]

        # Get rescale option from state if none is given
        if not rescale:
            rescale = st.session_state.rescale

        st.session_state["rescale"] = rescale
        m.add_cog_layer(
            url,
            name=f"{label}",
            bands=bands if len(bands) > 1 else [int(bands[-1][-1])],
            rescale=rescale,
        )
        st.session_state["bands"] = bands


def update_map_from_url(bands=None, rescale=None):
    if not bands:
        bands = st.session_state.bands

    # Prepare rescale options with on_change band value (min/max)
    if rescale:
        rescale = [
            f"{st.session_state[f'{band}_min']},{st.session_state[f'{band}_max']}"
            for band in bands
        ]

    add_to_map(
        m,
        st.session_state.url_input.split("|"),
        bands=bands,
        rescale=rescale,
        autoscale=False if rescale else True,
    )


def main():
    with header:
        st.title("COG Tiling Visualization")

    with options:
        (
            col_1,
            col_2,
            col_3,
        ) = st.columns([1, 1, 2])
        selection = col_1.selectbox("Swath:", list(sources.keys()))
        layer = col_2.selectbox("Layer:", ["All", *list(sources[selection].keys())])  # type: ignore

        url = st.text_input(
            "Enter COG URL(s):",
            (
                url_text := sources[selection][layer]  # type: ignore
                if layer != "All"
                else "|".join(sources[selection].values())  # type: ignore
            ),
            on_change=update_map_from_url,
            key="url_input",
            help="Separate URLs with a pipe symbol '|'.",
        )

        if url == url_text:
            if layer == "All":
                add_to_map(
                    m,
                    urls=list(sources[selection].values()),  # type: ignore
                    labels=list(sources[selection].keys()),  # type: ignore
                )
            else:
                add_to_map(m, urls=[sources[selection][layer]], labels=[layer])  # type: ignore

        bands = col_3.multiselect(
            "Order of bands:",
            st.session_state["bands"],
            default=st.session_state["bands"],
        )

        submit = st.button("Submit changes")

        if submit:
            update_map_from_url(bands=bands)

    with band_options:
        st.subheader("Band rescaling")
        cols = st.columns(6)

        # Create band input boxes dynamically
        for band, index in zip(bands, range(0, len(cols), 2)):
            cols[index].text_input(
                f"Band-{band} min",
                st.session_state.meta[band]["min"],
                key=f"{band}_min",
            )
            cols[index + 1].text_input(
                f"Band-{band} max",
                st.session_state.meta[band]["max"],
                key=f"{band}_max",
            )

        rescale = st.button("Rescale bands")

        if rescale:
            update_map_from_url(bands=bands, rescale=True)

    with mapview:
        m.to_streamlit()


if __name__ == "__main__":
    st.set_page_config(page_title="COGs Visualization", layout="wide")

    header = st.container()
    options = st.container()
    band_options = st.container()
    mapview = st.container()

    sources = tomllib.loads((Path(__file__).parent / "cog-sources.toml").read_text())

    m = leafmap.Map(
        draw_export=True,
    )

    main()
