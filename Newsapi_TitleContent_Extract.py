import requests
import pandas as pd
import time

# Newsapi.org API Data Feed
url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'GET_YOUR_OWN_API_KEY')

# Title & content extraction from nested JSON data feed
def ArticleList(url_call):
    """ This function will extract title and content """  

    title = []
    content = []
    _output = []
    
    response = requests.get(url_call).json()
    article = response['articles']
    
    for ar in article:
        title.append(ar['title'])
        content.append(ar['content'])
    
    _output = list(zip(title,content))
    output = pd.DataFrame(list(_output),
                          columns=['Title','Content'])
    return(output)

# Print out in .csv
today = time.strftime("%Y%m%d")
z = ArticleList(url)
z.to_csv(today + '_Article.csv', index = False)