import datetime
import os
import pathlib
import requests
import zipfile
import couchdb
import pandas as pd
import pydeck as pdk
import geopandas as gpd
import streamlit as st
import leafmap.colormaps as cm
from leafmap.common import hex_to_rgb

st.set_page_config(layout="wide")

# @st.cache_data
def initialise_data():
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

    gdf = gpd.read_file("dashboard/data/states.geojson")
    english = pd.DataFrame(requests.get('http://localhost:8000/english_view').json())
    foreign = pd.DataFrame(requests.get('http://localhost:8000/foreigner_view').json())
    income = pd.DataFrame(requests.get('http://localhost:8000/income_view').json())
    mental = pd.DataFrame(requests.get('http://localhost:8000/mentalhealth_view').json())
    sentiment = pd.DataFrame(requests.get('http://localhost:8000/sentiment_view').json())
    rent = pd.DataFrame(requests.get('http://localhost:8000/weekly_rent').json())
    rent_tweets = pd.DataFrame(requests.get('http://localhost:8000/rent_tweets').json())

    dfs = [english, foreign, income, mental, sentiment, rent, rent_tweets]
    new_gdf = gdf.copy()

    for df in dfs:
        curr_df = df.reset_index().rename(columns={'index': 'STATE_NAME'})
        new_gdf = new_gdf.merge(curr_df, on='STATE_NAME', how='outer')

    new_gdf['rent_tweets_percentage'] = new_gdf['rent_tweets'] / new_gdf['total_tweets']

    return new_gdf


def select_non_null(gdf, col_name):
    new_gdf = gdf[~gdf[col_name].isna()]
    return new_gdf


def select_null(gdf, col_name):
    new_gdf = gdf[gdf[col_name].isna()]
    return new_gdf


def app():

    st.title("Analysis across Australian States")

    row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns(
        [1, 0.5, 0.5, 0.5, 1]
    )

    attributes = ['total_tweets', 'eng_tweets', 'local_people', 'foreign_people', \
                  'mean_income', 'median_income', 'total_emergencies', 'mental_emergencies', \
                  'avg_sentiment', 'very_happy', 'happy', 'neutral', 'sad', 'very_sad', 'rent', 'rent_tweets']
    percentage_atts = ['eng_tweets', 'foreign_tweets', 'mental_emergencies', 'very_happy', 'happy', 'neutral', 'sad', 'very_sad', 'rent_tweets']
    descriptions = {
        'total_tweets': 'Total number of tweets in the state.',
        'eng_tweets': 'Number of English tweets in the state.',
        'eng_tweets_percentage': 'Percentage of English tweets in the state.',
        'local_people': 'Number of locals in the state.',
        'foreign_people': 'Number of foreigners in the state.',
        'foreign_people_percentage': 'Percentage of foreigners in the state.',
        'mean_income': 'Annual mean income (AUD).',
        'median_income': 'Annual median income (AUD).',
        'total_emergencies': 'Number of emergencies in the state.',
        'mental_emergencies': 'Number of emergencies in the state relating to mental health.',
        'mental_emergencies_percentage': 'Percentage of emergencies in the state relating to mental health.',
        'avg_sentiment': 'Average sentiment value (-1,1) from tweets made in the state.',
        'very_happy': 'Number of tweets with a very happy sentiment (> 0.7).',
        'very_happy_percentage': 'Percentage of tweets with a very happy sentiment (> 0.7).',
        'happy': 'Number of tweets with a happy sentiment (<= 0.7 and > 0.3).',
        'happy_percentage': 'Percentage of tweets with a happy sentiment (<= 0.7 and > 0.3).',
        'neutral': 'Number of tweets with a neutral sentiment (< 0.3 and > -0.3).',
        'neutral_percentage': 'Percentage of tweets with a neutral sentiment (< 0.3 and > -0.3).',
        'sad': 'Number of tweets with a sad sentiment (<= -0.3 and > -0.7).',
        'sad_percentage': 'Percentage of tweets with a sad sentiment (<= -0.3 and > -0.7).',
        'very_sad': 'Number of tweets with a very sad sentiment (<= -0.7).',
        'very_sad_percentage': 'Percentage of tweets with a very sad sentiment (<= -0.7).',
        'rent_2019': 'Median weekly rental prices (AUD) in the state in 2019.',
        'rent_2021': 'Median weekly rental prices (AUD) in the state in 2021.',
        'rent_tweets': 'Number of tweets related to rent in the state.',
        'rent_tweets_percentage': 'Percentage of tweets related to rent in the state.'
    }

    with row1_col1:
        selected_col = st.selectbox("Attribute", attributes)
    with row1_col2:
        if (selected_col == 'rent'):
            year = st.radio('Year',("2019", "2021"))
        elif selected_col in percentage_atts:
            percentage = st.checkbox("Show as percentage", value=False)
        else:
            st.empty()
    palettes = cm.list_colormaps()
    with row1_col3:
        palette = st.selectbox("Color palette", palettes, index=palettes.index("Blues"))
    with row1_col4:
        show_nodata = st.checkbox("Show nodata areas", value=True)

    gdf = initialise_data()

    if (selected_col == 'rent'):
        selected_col = 'rent_' + str(year)
    elif ((selected_col in percentage_atts) and (percentage)):
        selected_col = selected_col + '_percentage'

    with row1_col5:
        show_desc = st.checkbox("Show attribute description", value=True)
        if show_desc:
            markdown = f"""
                {descriptions[selected_col]}
                """
            st.markdown(markdown)
    
    gdf_null = select_null(gdf, selected_col)
    gdf = select_non_null(gdf, selected_col)
    gdf = gdf.sort_values(by=selected_col, ascending=True)

    colors = cm.get_palette(palette)
    colors = [hex_to_rgb(c) for c in colors]

    for i, ind in enumerate(gdf.index):
        index = int(i / (len(gdf) / len(colors)))
        if index >= len(colors):
            index = len(colors) - 1
        gdf.loc[ind, "R"] = colors[index][0]
        gdf.loc[ind, "G"] = colors[index][1]
        gdf.loc[ind, "B"] = colors[index][2]

    initial_view_state = pdk.ViewState(
        latitude=-28,
        longitude=133,
        zoom=3.25,
        max_zoom=5,
        pitch=0,
        bearing=0,
        height=600,
        width=None,
    )

    min_value = gdf[selected_col].min()
    max_value = gdf[selected_col].max()
    color = "color"
    color_exp = f"[R, G, B]"

    geojson = pdk.Layer(
        "GeoJsonLayer",
        gdf,
        pickable=True,
        opacity=0.5,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color=color_exp,
        get_line_color=[0, 0, 0],
        get_line_width=2,
        line_width_min_pixels=1,
    )

    geojson_null = pdk.Layer(
        "GeoJsonLayer",
        gdf_null,
        pickable=True,
        opacity=0.2,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color=[200, 200, 200],
        get_line_color=[0, 0, 0],
        get_line_width=2,
        line_width_min_pixels=1,
    )

    tooltip = {
        "html": "<b>Name:</b> {STATE_NAME}<br><b>Value:</b> {"
        + selected_col
        + "}",
        "style": {"backgroundColor": "steelblue", "color": "white"},
    }

    layers = [geojson]
    if show_nodata:
        layers.append(geojson_null)

    r = pdk.Deck(
        layers=layers,
        initial_view_state=initial_view_state,
        map_style="light",
        tooltip=tooltip,
    )

    row3_col1, row3_col2 = st.columns([6, 1])

    with row3_col1:
        st.pydeck_chart(r)
    with row3_col2:
        st.write(
            cm.create_colormap(
                palette,
                label=selected_col.replace("_", " ").title(),
                width=0.2,
                height=3,
                orientation="vertical",
                vmin=min_value,
                vmax=max_value,
                font_size=10,
            )
        )

app()