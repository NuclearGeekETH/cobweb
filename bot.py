from cobweb_twit import startBot
import tweepy
import requests
import json
import time
import threading
from dotenv import load_dotenv
import os

load_dotenv()

twitter_api_key = os.environ["twitter_api_key"]
twitter_api_secret = os.environ["twitter_api_secret"]
twitter_bearer_token = os.environ["twitter_bearer_token"]
twitter_access_token = os.environ["twitter_access_token"]
twitter_access_secret = os.environ["twitter_access_secret"]
twitter_client_id = os.environ["twitter_client_id"]
twitter_client_secret = os.environ["twitter_client_secret"]

# AiFrensBot
API_KEY = twitter_api_key
API_KEY_SECRET = twitter_api_secret
Bearer_Token = twitter_bearer_token
Access_Token = twitter_access_token
Access_Token_Secret = twitter_access_secret
Client_ID = twitter_client_id
Client_Secret = twitter_client_secret
CONSUMER_KEY = API_KEY
CONSUMER_SECRET = API_KEY_SECRET
ACCESS_KEY = Access_Token
ACCESS_SECRET = Access_Token_Secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

csv_file_name = "cobweb.csv"

def getClient():
    client = tweepy.Client(bearer_token=Bearer_Token, 
                        consumer_key=API_KEY, 
                        consumer_secret=API_KEY_SECRET, 
                        access_token=Access_Token, 
                        access_token_secret=Access_Token_Secret)
    return client

def start_thread(func, name=None, args = []):
    threading.Thread(target=func, name=name, args=args).start()

def tweet(url, tweet_id):
    link = startBot(url)
    # time.sleep(10)
    status_text = f"This tweet has been forever pinned to IPFS using Cobweb: {link}"
    print(status_text)
    client = getClient()
    client.create_tweet(text=status_text, in_reply_to_tweet_id=tweet_id)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {Bearer_Token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()

def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))

def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "@AiFrensBot", "tag": "fren"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

def get_stream(set):
    try:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream?expansions=author_id,referenced_tweets.id&user.fields=username", auth=bearer_oauth, stream=True,
        )
        print(response.status_code)
    except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as err:
        print(err + ' Put to sleep before retrying.')
        time.sleep(100)
        get_stream(set)

    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():

        try:
            if response_line:
                json_response = json.loads(response_line)
                # tweet_type = json_response['data']['referenced_tweets'][0]['type']
                # print(json.dumps(json_response, indent=4, sort_keys=True))
                tweet_id = json_response['data']['id']
                tweet_text = json_response['data']['text']
                print(tweet_text)
                # print(tweet_text)
                screen_name = json_response['includes']['users'][0]['username']
                pin_tweet_id = json_response['includes']['tweets'][0]['id']
                # referenced_tweet = json_response['data']['referenced_tweets'][0]['id']
                # print(referenced_tweet)
                print(screen_name)
                url = 'https://twitter.com/anyuser/status/' + pin_tweet_id
                print(url)
                tweet_text_case = tweet_text.lower()
                if tweet_text[:2] == 'RT':
                    # print(tweet_text[:2])
                    pass
                if tweet_text_case.endswith('@aifrensbot'):
                    start_thread(tweet, args=[url, tweet_id])
                    # link = startBot(url)
                else:
                  pass          
        except:
            pass
        
def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)
    main()

if __name__ == "__main__":
  main()