import requests, json, time
import datetime as dt
from steem import Steem
from jinja2 import Template
from textblob import TextBlob
from auth import keys

# Settings
author = 'bobthebot'
# End Settings

# Init
prev_post_time = dt.datetime.now()
s = Steem(keys=keys)
# Get related results
def get_related_results(post):
    print('='*20)
    print(post.title)
    response = json.loads(requests.get(
        'https://api.asksteem.com/related?author={}&permlink={}&min_score=100'.format(
            post.author,post.permlink
        )
    ).content.decode('utf-8'))
    # return top 3 results
    return response['results'][:3]

# Check if bot already relied to a post
def already_replied_to(post):
    replies = post.get_replies()
    if author in [reply.author for reply in replies]:
        return True
    else:
        return False

def post_scheduler(body):
    global prev_post_time
    if (dt.datetime.now() - prev_post_time).total_seconds() > 20:
        post.reply(
            author=author,
            body=body
        )
        prev_post_time = dt.datetime.now()
        print('New Reply at {}'.format(prev_post_time))
        return True
    else:
        return False


# jinja2 template
with open('post.temp','r') as f:
    template = Template(f.read())

while True:
    try:
        for post in s.stream_comments():
            if post.is_main_post():
                # for now limit it the english posts
                if TextBlob(post.title).detect_language() == 'en':
                    if not already_replied_to(post):
                        related = get_related_results(post)
                        if len(related) > 0:
                            post_scheduler(template.render(related=related))
    except:
        time.sleep(10)
