from fastapi import FastAPI
import uvicorn

from process_mastodon_data import process_mastodon
from views import rent_view
from get_twitter_shortage import tweet_shortages

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/mastodon_wordcloud")
async def mastodon_wordcloud():
    final_words = process_mastodon()

    return final_words

@app.get("/rent")
async def rent():
    result = rent_view()
    return result

@app.get("/twitter_wordcloud")
async def twitter_wordcloud():
    final_words = tweet_shortages()
    
    return final_words

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
