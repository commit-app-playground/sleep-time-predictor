import tweepy
import datetime
from django.shortcuts import render


def home(request):
    return render(request, "twitterapp/index.html", {})


def handle_form(request):
    handle = request.GET.get("twitterHandle", None)
    key = "OxKRWUXdFSujMuu9XE1vJNYoN"
    secret = "zqkjpU9HsxQPPJrLLrqueRSc5bJWERqyDGTmNAuM9M8XTCgRTO"
    access_token = "234259506-UbpK52FxGh5ZfbeqCHdMocw7D9M9HhHjO1Wdo1fl"
    access_token_secret = "Cuf303qBlDjT9UgynDjfcjFS3jQCV5fS2c42cYLmTaF3a"
    auth = tweepy.OAuth1UserHandler(key, secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=handle, count=200)
    user = api.get_user(screen_name=handle)
    timestamps = [tweet.created_at for tweet in tweets]
    timestamps = sorted(timestamps)
    min_max = {}
    maxes = []
    mins = []
    for time in timestamps:
        if time.date() in min_max.keys():
            min_max[time.date()].append(time)
        else:
            min_max[time.date()] =[time]

    for k, v in min_max.items():
        v = sorted(v)
        mins.append(v[0])
        maxes.append(v[-1])

    print(f"Minimum times : {mins}")
    print(f"Maximum times : {maxes}")

    avg_max = datetime.datetime.fromtimestamp(sum(d.timestamp() for d in maxes)/len(maxes))
    avg_min = datetime.datetime.fromtimestamp(sum(d.timestamp() for d in mins)/len(mins))
    wake = (avg_min + datetime.timedelta(hours=-3)).time()
    sleep = (avg_max + datetime.timedelta(hours=1.5)).time()

    return render(request, "twitterapp/results.html", {
        "user":user,
        "tweet_count": len(tweets),
        "avg_max": avg_max.time(),
        "avg_min": avg_min.time(),
        "wake": wake,
        "sleep": sleep
    })