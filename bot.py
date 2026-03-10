import requests
from PIL import Image, ImageDraw, ImageFont
import tweepy
import config

def get_last_match(team):

    url = f"{config.SPORTSDB_API}searchteams.php?t={team}"
    r = requests.get(url).json()

    if not r["teams"]:
        print("Team not found:", team)
        return None

    team_id = r["teams"][0]["idTeam"]

    url2 = f"{config.SPORTSDB_API}eventslast.php?id={team_id}"
    data = requests.get(url2).json()

    if not data["results"]:
        print("No match found for", team)
        return None

    return data["results"][0]


def create_result_image(match):

    img = Image.new("RGB", (900, 500), (20,20,20))
    draw = ImageDraw.Draw(img)

    text = f"{match['strHomeTeam']} {match['intHomeScore']} - {match['intAwayScore']} {match['strAwayTeam']}"

    draw.text((100,200), text, fill="white")

    file = "result.png"
    img.save(file)

    return file


def tweet_result(match):

    client = tweepy.Client(
        consumer_key=config.API_KEY,
        consumer_secret=config.API_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_SECRET
    )

    text = f"FT: {match['strHomeTeam']} {match['intHomeScore']} - {match['intAwayScore']} {match['strAwayTeam']}"
    print("Tweeting:", text)
    image = create_result_image(match)

    api = tweepy.API(
        tweepy.OAuth1UserHandler(
            config.API_KEY,
            config.API_SECRET,
            config.ACCESS_TOKEN,
            config.ACCESS_SECRET
        )
    )

    media = api.media_upload(image)

    client.create_tweet(text=text, media_ids=[media.media_id])

def main():
    print("BOT START")

    for team in config.TEAMS:

        try:
            print("Checking team:", team)

            match = get_last_match(team)            
            if not match:
                continue

            print("Match data:", match)

            tweet_result(match)

            print("Tweet sent")

        except Exception as e:
            print("ERROR:", e)


if __name__ == "__main__":
    main()
