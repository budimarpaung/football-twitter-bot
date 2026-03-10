import requests
import tweepy
from PIL import Image, ImageDraw
import config

print("BOT STARTED")

def get_matches():

    r = requests.get(config.SCOREBAT_API).json()

    return r["response"]


def find_team_match(team, matches):

    for match in matches:

        title = match["title"]

        if team.lower() in title.lower():

            return match

    return None


def create_result_image(match):

    title = match["title"]

    img = Image.new("RGB", (900,500),(20,20,20))
    draw = ImageDraw.Draw(img)

    draw.text((120,220), title, fill="white")

    file="result.png"

    img.save(file)

    return file


def tweet(match):

    client = tweepy.Client(
        consumer_key=config.API_KEY,
        consumer_secret=config.API_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_SECRET
    )

    api = tweepy.API(
        tweepy.OAuth1UserHandler(
            config.API_KEY,
            config.API_SECRET,
            config.ACCESS_TOKEN,
            config.ACCESS_SECRET
        )
    )

    text=f"FT: {match['title']}"

    image=create_result_image(match)

    media=api.media_upload(image)

    client.create_tweet(
        text=text,
        media_ids=[media.media_id]
    )

    print("Tweet sent:", text)


def main():

    matches=get_matches()

    for team in config.TEAMS:

        print("Checking:", team)

        match=find_team_match(team,matches)

        if not match:
            continue

        tweet(match)


if __name__=="__main__":
    main()
