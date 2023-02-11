# ==========================IMPORTS=========================
import snscrape.modules.twitter as tw
import general_methods as gm

dict_methods= {
    'by_user': lambda v: 'from:@'+v,#'from:@'+username
    'by_hashtag': lambda v: v+'#'#hashtag+'#'
    }

def get_by_type(method_type,query, limit= 200):

    try:
        query = dict_methods[method_type](query)
    except:
        return None

    return getTweets(query, limit)


def getTweets(query,numtweets):
  tweets_list = []
  for i, tweet in enumerate(tw.TwitterSearchScraper(query).get_items()):
      if i >= numtweets-1:
          break
      
      if gm.data_prep(tweet.rawContent):    #if not null to list 
        tweets_list.append([tweet.id, gm.data_prep(tweet.rawContent)])
      else:
        numtweets=numtweets+1
  return tweets_list 


print(' * twitter_methods is loaded')