import requests
from PIL import Image, ImageDraw
import tweepy
import config
import os

print("BOT START")


def get_last_match(team):

    url = f"{config.SPORTSDB_API}searchteams.php?t={team}"
    r = requests.get(url).json()

    if not r["teams"]:
        return None

    team_id = r["teams"][0]["idTeam"]

    url2 = f"{config.SPORTSDB_API}eventslast.php?id={team_id}"
    match = requests.get(url2).json()["results"][0]

    return match


def create_result_image(match):

    img = Image.new("RGB", (900, 500), (15,15,15))
    draw = ImageDraw.Draw(img)

    text = f"{match['strHomeTeam']} {match['intHomeScore']} - {match['intAwayScore']} {match['strAwayTeam']}"

    draw.text((150,220), text, fill="white")

    file = "result.png"
    img.save(file)

    return file


def already_tweeted(match_id):

    if not os.path.exists("last_match.txt"):
        return False

    with open("last_match.txt","r") as f:
        last = f.read()

    return last == match_id


def save_match(match_id):

    with open("last_match.txt","w") as f:
        f.write(match_id)


def tweet_result(match):

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

    text = f"FT: {match['strHomeTeam']} {match['intHomeScore']} - {match['intAwayScore']} {match['strAwayTeam']}"

    image = create_result_image(match)

    media = api.media_upload(image)

    client.create_tweet(
        text=text,
        media_ids=[media.media_id]
    )


def main():

    for team in config.TEAMS:

        try:

            print("Checking:", team)

            match = get_last_match(team)

            if not match:
                continue

            match_id = match["idEvent"]

            if already_tweeted(match_id):
                print("Already tweeted")
                continue

            tweet_result(match)

            save_match(match_id)

            print("Tweet sent")

        except Exception as e:

            print("ERROR:", e)


if __name__ == "__main__":
    main()
