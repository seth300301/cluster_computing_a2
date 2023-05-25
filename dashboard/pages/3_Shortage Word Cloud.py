import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Shortage Word Cloud",
    layout="wide",
)

@st.cache
def initialise_data():
    shortage_tweets = requests.get('http://backend:8000/twitter_wordcloud').json()
    shortage_toots = requests.get('http://backend:8000/mastodon_wordcloud').json()

    return shortage_tweets, shortage_toots

def main():
    shortage_tweets, shortage_toots = initialise_data()

    st.write("# Words Relating Shortages in Australia")
    graph_type = st.radio('Show as:',("Bar Chart", "Word Cloud"))

    if (graph_type == 'Word Cloud'):
        wordcloud_tweets = WordCloud(colormap='gist_rainbow', width=600, height=400)
        wordcloud_tweets.generate_from_frequencies(shortage_tweets)

        wordcloud_toots = WordCloud(colormap='gist_rainbow', width=600, height=400)
        wordcloud_toots.generate_from_frequencies(shortage_toots)

        st.write("## Shortage Words from Tweets")
        plt.imshow(wordcloud_tweets, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        st.write("## Shortage Words from Toots")
        plt.imshow(wordcloud_toots, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
    
    else:
        shortage_tweets = pd.DataFrame.from_dict(shortage_tweets, orient='index', columns=['Number of Tweets'])
        shortage_toots = pd.DataFrame.from_dict(shortage_toots, orient='index', columns=['Number of Tweets'])

        figs = []

        tweet_fig = px.bar(pd.DataFrame(shortage_tweets), x=shortage_tweets.index, y="Number of Tweets")
        figs.append(tweet_fig)
        toot_fig = px.bar(pd.DataFrame(shortage_toots), x=shortage_toots.index, y="Number of Tweets")
        figs.append(toot_fig)

        for fig in figs:
            fig.update_layout(
                xaxis=dict(showticklabels=False),
            )

        st.write("### Shortage Words from Tweets:")
        st.plotly_chart(figs[0], use_container_width=True)
        st.write("### Shortage Words from Toots")
        st.plotly_chart(figs[1], use_container_width=True)

if __name__ == '__main__':
    main()