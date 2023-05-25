import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import altair as alt
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Trends in Tweets and Toots",
    layout="wide",
)

st.write("# Trending Entities and Hashtags")
row1_col1, row1_col2 = st.columns([1, 1])
with row1_col1:
    graph_type = st.radio('Show as:',("Bar Chart", "Word Cloud"))
with row1_col2:
    data_type = st.radio('Show as:',("Tweets", "Toots"))

if (graph_type == 'Bar Chart'):
    if (data_type == 'Tweets'):
        entities = pd.read_json("dashboard/data/all_entities.json")
        hashtags = pd.read_json("dashboard/data/hashtags.json")

        entities['Entity'] = entities['Entity'] + " " + entities['Entity Type']
    else:
        entities = pd.DataFrame(requests.get('http://backend:8000/mastodon_entities').json())
        hashtags = pd.DataFrame(requests.get('http://backend:8000/mastodon_hashtags').json())

        entities['Entity'] = entities['Entity'] + " " + entities['Entity Type']
        entities = entities.sort_values('Number of Tweets', ascending=False)
        hashtags = hashtags.sort_values('Number of Tweets', ascending=False)

    figs = []

    if (data_type == 'Tweets'):
        ent_data = entities.head(101)[1:]
        hash_data = hashtags.head(101)[1:]
        ent_title = "#2 - 100 Entities " + str(data_type)[:-1] + "ed"
        hash_title = "#2 - 100 Hashtags " + str(data_type)[:-1] + "ed"
    else:
        ent_data = entities.head(101)
        hash_data = hashtags.head(101)
        ent_title = "Top 100 Entities " + str(data_type)[:-1] + "ed"
        hash_title = "Top 100 Hashtags " + str(data_type)[:-1] + "ed"


    ent_fig = px.bar(pd.DataFrame(ent_data), x="Entity", y="Number of Tweets", title=ent_title)
    figs.append(ent_fig)
    hash_fig = px.bar(pd.DataFrame(hash_data), x="Hashtag", y="Number of Tweets", title=hash_title)
    figs.append(hash_fig)

    for fig in figs:
        fig.update_layout(
            xaxis=dict(showticklabels=False),
        )

    st.write("### Entity Count in " + str(data_type))
    if (data_type == 'Tweets'):
        st.write("_#1 Entity " + str(data_type)[:-1] + "ed: " + str(entities['Entity'][0]) + " - " + str(entities['Number of Tweets'][0]) + "_")
    st.plotly_chart(figs[0], use_container_width=True)
    st.write("### Hashtag Count in " + str(data_type))
    if (data_type == 'Tweets'):
        st.write("_#1 Hashtag " + str(data_type)[:-1] + "ed: " + str(hashtags['Hashtag'][0]) + " - " + str(hashtags['Number of Tweets'][0]) + "_")
    st.plotly_chart(figs[1], use_container_width=True)

else:
    if (data_type == 'Tweets'):
        with open("dashboard/data/all_entities.json", 'r') as file:
        # Load the contents of the file as JSON data
            entities = {item['Entity']: item['Number of Tweets'] for item in json.load(file)}

        with open("dashboard/data/hashtags.json", 'r') as file:
        # Load the contents of the file as JSON data
            hashtags = {item['Hashtag']: item['Number of Tweets'] for item in json.load(file)}
    else:
        entities = requests.get('http://backend:8000/mastodon_entities').json()
        entities = {item['Entity']: item['Number of Tweets'] for item in entities}

        hashtags = requests.get('http://backend:8000/mastodon_hashtags').json()
        hashtags = {item['Hashtag']: item['Number of Tweets'] for item in hashtags}

    wordcloud_entitiies = WordCloud(colormap='gist_rainbow', width=600, height=400)
    wordcloud_entitiies.generate_from_frequencies(entities)

    wordcloud_hashtags = WordCloud(colormap='gist_rainbow', width=600, height=400)
    wordcloud_hashtags.generate_from_frequencies(hashtags)

    st.write("## Trending Entities from " + str(data_type))
    plt.imshow(wordcloud_entitiies, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.write("## Trending Hashtags from " + str(data_type))
    plt.imshow(wordcloud_hashtags, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)