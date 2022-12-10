import pandas as pd
import streamlit as st
from halo import Halo

import time
import utils

# Cache the dataframe so it's only loaded once
@st.experimental_memo
def load_data(urls):
    
    start_time = time.time()
    spinner = Halo(text='Scrapping data from MagicSeaWeed\n',text_color='blue', color= 'magenta', spinner='dots')
    spinner.start()

    df = utils.scrape_multiple_sites(urls)
    df = utils.format_dataframe(df)
    utils.df_to_csv("magicseaweed.csv", df)
    
    spinner.stop_and_persist(text='You can check the url (👨‍💻) or if you prefer, the csv file (👀📈), happy surfing (🏄) and respect the sea(🌊)')
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
    return df



def plot_data(urls):

    
    # Boolean to resize the dataframe, stored as a session state variable
    st.checkbox("Use container width", value=False, key="use_container_width")
    df = load_data(urls)

    # Display the dataframe and allow the user to stretch the dataframe
    # across the full width of the container, based on the checkbox value

    #GET UNIQUES
    date_name = df['date_name'].unique().tolist()
    wind_state = df['wind_state'].unique().tolist()
    beach = df['beach'].unique().tolist()
    approval = df['approval'].unique().tolist()
    tides_state = df['tides_state'].unique().tolist()

    #CREATE MULTISELECT
    date_name_selection = st.multiselect('Date:', date_name, default=date_name)
    wind_state_selection = st.multiselect('Wind State:',
                                          wind_state,
                                          default=['Offshore'])
    beach_selection = st.multiselect('Beach:', beach, default=beach)
    approval_selection = st.multiselect('Approval:',
                                        approval,
                                        default=['Favorable'])

    tides_state_selection = st.multiselect('Tides State:',
                                           tides_state,
                                           default=tides_state)

    # --- FILTER DATAFRAME BASED ON SELECTION
    mask = (df['date_name'].isin(date_name_selection)) & (df['wind_state'].isin(
        wind_state_selection)) & (df['beach'].isin(beach_selection)) & (
            df['approval'].isin(approval_selection)) & (df['tides_state'].isin(tides_state_selection))

    number_of_result = df[mask].shape[0]

    # --- GROUP DATAFRAME AFTER SELECTION
    df = df[mask]

    st.dataframe(df, use_container_width=st.session_state.use_container_width)
    
