from fastapi import FastAPI
import uvicorn

from process_mastodon_data import process_mastodon
from views import english_view, foreigner_view, income_view, mentalhealth_view, sentiment_view, weekly_rent, rent_tweets, tweet_shortages

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/mastodon_wordcloud")
async def mastodon_wordcloud():
    final_words = process_mastodon()
    return final_words

@app.get("/mastodon_wordcloud")
async def mastodon_wordcloud():
    final_words = process_mastodon()
    return final_words

@app.get("/mastodon_wordcloud")
async def mastodon_wordcloud():
    final_words = process_mastodon()
    return final_words

@app.get("/twitter_wordcloud")
async def twitter_wordcloud():
    final_words = tweet_shortages()
    return final_words

@app.get("/english_view")
async def english():
    return english_view()

@app.get("/foreigner_view")
async def foreigner():
    return foreigner_view()

@app.get("/income_view")
async def income():
    return income_view()

@app.get("/mentalhealth_view")
async def mentalhealth():
    return mentalhealth_view()

@app.get("/sentiment_view")
async def sentiment():
    return sentiment_view()

@app.get("/weekly_rent")
async def rent():
    return weekly_rent()

@app.get("/rent_tweets")
async def rent_tweet():
    return rent_tweets()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
