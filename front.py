import streamlit as st
from halo import Halo

import time, utils
from threads import multithread

# Cache the dataframe so it's only loaded once
@st.experimental_memo(ttl=7200)
def load_data(spots_data):
    start_time = time.time()
    spinner = Halo(
        text="Scrapping data from MagicSeaWeed\n",
        text_color="blue",
        color="magenta",
        spinner="dots",
    )
    spinner.start()

    df = multithread.scrape_multiple_sites(spots_data)
    df = utils.format_dataframe(df)
    utils.df_to_csv("magicseaweed.csv", df)

    spinner.stop_and_persist(
        text="You can check the url (👨‍💻) or if you prefer, the csv file (👀📈), happy surfing (🏄) and respect the sea(🌊)"
    )
    print("--- %s seconds ---" % (time.time() - start_time))

    return df


def plot_data(spots_data):

    # Boolean to resize the dataframe, stored as a session state variable
    st.checkbox("Use container width", value=False, key="use_container_width")
    st.session_state.df = load_data(spots_data)

    #
    button = st.button("Rescrape data")
    if button:
        st.experimental_memo.clear()
        st.session_state.df = multithread.scrape_multiple_sites(spots_data)
        st.session_state.df = utils.format_dataframe(st.session_state.df)
        button = False
    #

    # Display the dataframe and allow the user to stretch the dataframe
    # across the full width of the container, based on the checkbox value

    # GET UNIQUES
    date_name = st.session_state.df["date_name"].unique().tolist()
    wind_state = st.session_state.df["wind_state"].unique().tolist()
    beach = st.session_state.df["beach"].unique().tolist()
    approval = st.session_state.df["approval"].unique().tolist()
    tides_state = st.session_state.df["tides_state"].unique().tolist()
    island = st.session_state.df["island"].unique().tolist()

    # CREATE MULTISELECT
    date_name_selection = st.multiselect("Date:", date_name, default=date_name)
    wind_state_selection = st.multiselect(
        "Wind State:", wind_state, default=["Offshore"]
    )
    beach_selection = st.multiselect("Beach:", beach, default=beach)
    approval_selection = st.multiselect("Approval:", approval, default=["Favorable"])

    tides_state_selection = st.multiselect(
        "Tides State:", tides_state, default=tides_state
    )

    island_selection = st.multiselect("Island:", island, default=["Lanzarote"])
    # --- FILTER DATAFRAME BASED ON SELECTION
    mask = (
        (st.session_state.df["date_name"].isin(date_name_selection))
        & (st.session_state.df["wind_state"].isin(wind_state_selection))
        & (st.session_state.df["beach"].isin(beach_selection))
        & (st.session_state.df["approval"].isin(approval_selection))
        & (st.session_state.df["tides_state"].isin(tides_state_selection))
        & (st.session_state.df["island"].isin(island_selection))
    )

    # --- GROUP DATAFRAME AFTER SELECTION
    st.session_state.df = st.session_state.df[mask]

    st.dataframe(
        st.session_state.df, use_container_width=st.session_state.use_container_width
    )
