import requests
from bs4 import BeautifulSoup
import tweepy
import random

# Suas credenciais do Twitter Developer
bearer_token = ''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

def get_philosophy_quote_from_quotable():
    response = requests.get("https://api.quotable.io/random")
    if response.status_code == 200:
        data = response.json()
        return {"author": data['author'], "quote": data['content']}
    else:
        print("Error fetching quote.")
        return None

def get_author_image_from_wikipedia(author_name):
    base_url = "https://en.wikipedia.org/wiki/"
    author_url = base_url + author_name.replace(" ", "_")
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_tag = soup.find('table', class_='infobox').find('img')
    if image_tag:
        image_url = "https:" + image_tag['src']
        image_response = requests.get(image_url, stream=True)
        filename = f"{author_name}.jpg"
        with open(filename, 'wb') as file:
            for chunk in image_response.iter_content(8192):
                file.write(chunk)
        return filename
    else:
        return None

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api_v1 = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

quote_data = get_philosophy_quote_from_quotable()
if quote_data:
    quote = quote_data["quote"]
    author = quote_data["author"]

    # Display the quote and ask for Sindarin translation
    print(f"Please provide the Sindarin translation for the following quote:\n{quote}")
    sindarin_translation = input("Sindarin Translation: ")

    author_image_path = get_author_image_from_wikipedia(author)

    elf_image_number = random.randint(1, 9)
    elf_image_path = f"elfas/{elf_image_number}.jpg"

    media_ids = []
    for image_path in [author_image_path, elf_image_path]:
        media_id = api_v1.media_upload(filename=image_path).media_id_string
        media_ids.append(media_id)

    # Format the tweet
    text = f'Sindarin: "{sindarin_translation}" - {author}\n'
    text += f'Translate: "{quote}" - {author}'

    client.create_tweet(text=text, media_ids=media_ids)
    print("Tweeted!")