import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
import requests
#import couchdb

# server = couchdb.Server('http://admin:300301@localhost:5984')
# ent_db = server['entities']
# hash_db = server['hashtags']

st.set_page_config(
    page_title="Home | Overview",
    layout="wide",
)

st.write("# Overview Dashboard")

entities = pd.read_json("dashboard/data/all_entities.json")
hashtags = pd.read_json("dashboard/data/hashtags.json")

entities['Entity'] = entities['Entity'] + " " + entities['Entity Type']

figs = []

ent_fig = px.bar(pd.DataFrame(entities.head(101)[1:]), x="Entity", y="Number of Tweets")
figs.append(ent_fig)
hash_fig = px.bar(pd.DataFrame(hashtags.head(101)[1:]), x="Hashtag", y="Number of Tweets")
figs.append(hash_fig)

for fig in figs:
    fig.update_layout(
        xaxis=dict(showticklabels=False),
    )

st.write("### Entity Count in Tweets:")
st.write("_#1 Entity Tweeted: " + str(entities['Entity'][0]) + " - " + str(entities['Number of Tweets'][0]) + "_")
st.plotly_chart(figs[0], use_container_width=True)
st.write("### Hashtag Count in Tweets")
st.write("_#1 Hashtag Tweeted: " + str(hashtags['Hashtag'][0]) + " - " + str(hashtags['Number of Tweets'][0]) + "_")
st.plotly_chart(figs[1], use_container_width=True)
