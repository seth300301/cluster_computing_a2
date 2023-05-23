import streamlit as st
import pandas as pd
import numpy as np
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
graph_type = st.radio('Show as:',("Bar Chart", "Word Cloud"))

entities = pd.read_json("dashboard/data/all_entities.json")
hashtags = pd.read_json("dashboard/data/hashtags.json")

entities['Entity'] = entities['Entity'] + " " + entities['Entity Type']

if (graph_type == 'Bar Chart'):
    figs = []

    ent_fig = px.bar(pd.DataFrame(entities.head(101)[1:]), x="Entity", y="Number of Tweets", title="#2 - 100 Entities Tweeted")
    figs.append(ent_fig)
    hash_fig = px.bar(pd.DataFrame(hashtags.head(101)[1:]), x="Hashtag", y="Number of Tweets", title="#2 - 100 Hashtags Tweeted")
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

else:
    wordcloud_entitiies = WordCloud(colormap='gist_rainbow', width=600, height=400)
    wordcloud_entitiies.generate_from_frequencies(entities)

    wordcloud_hashtags = WordCloud(colormap='gist_rainbow', width=600, height=400)
    wordcloud_hashtags.generate_from_frequencies(hashtags)

    st.write("## Shortage Words from Tweets")
    plt.imshow(wordcloud_entitiies, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.write("## Shortage Words from Toots")
    plt.imshow(wordcloud_hashtags, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)