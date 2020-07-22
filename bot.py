import tweepy
import requests
import time
from random import randrange

def getPostInfo(type):
    # returns url of random top subreddit post
    # type can be hour, day, week, month, year, all (bot will only use month, year, or all)

    headers = {'user-agent': 'my-app/0.0.1'}

    requestURL = 'https://old.reddit.com/r/random/top.json?t=' + type + '&limit=1'

    r = requests.get(requestURL, headers=headers)

    subreddit = r.json()['data']['children'][0]['data']['subreddit']
    name = r.json()['data']['children'][0]['data']['name']
    title = r.json()['data']['children'][0]['data']['title']


    url = 'https://old.reddit.com/r/' + subreddit + '/comments/' + name[3:]

    return url, subreddit, title, type

def generatePostType():
    num = randrange(3)

    if num == 0:
        postType = 'month'
    if num == 1:
        postType = 'year'
    if num == 2:
        postType = 'all'

    return postType

def main():
    while(True):
        # twitter api authentication
        consumer_key = '4suGwwWVXKC3qz139Cshn1psU'
        consumer_secret = 'bcosF1KtLOHvH0pSqLmIYMxyfMVS86mLXxjGwwN6birZ5PB6z1'

        key = '1284242327863570432-orrXVE1tvLzOrSEwVK8kWnM4mv2X3W'
        secret = 'UXonjwA0ZBgbkZjQ2TsDbc3CRL1tR1s6IgwkdnKDLA791'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)

        # creates the api object
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # generates post type
        postType = generatePostType()

        # calls getURL method to generate top post link
        postInfo = getPostInfo(postType)
        

        # create the content for the tweet. Wording is different depending on the type of post
        if postInfo[3] == 'all':
            tweetContent = 'Top post of all time in /r/' + postInfo[1] + ':\n\n'
        else:
            tweetContent = 'Top post of the ' + postInfo[3] + ' in /r/' + postInfo[1] + ':\n\n'

        # append the rest of the tweetcontent 
        redditContent = postInfo[2]
        tweetContent = tweetContent + redditContent[:100] + '...\n\n' + postInfo[0]
        
        # tweet content
        api.update_status(tweetContent)
        print('Tweeted Content')
        time.sleep(21600)

if __name__ == '__main__':
    main()