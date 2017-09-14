#author Meikel Ratz 
#Script for scraping the twitter page by hashtags

#some code was used from "http://stackoverflow.com/questions/34942103/headless-endless-scroll-selenium"

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import urllib,sys



reload(sys)
sys.setdefaultencoding("utf-8")

#name of the .csv file your data will be written to 

csvFile = "destination.csv"

#writes the header of the csv file 
with open(csvFile, 'wb') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["id", "timestamp", "tweet", "retweets", "likes","hasImage", "hasVideo", "hasUrl"])
    writer.writeheader()


class wait_for_more_than_n_elements_to_be_present(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except StaleElementReferenceException:
            print '[-] an Error occured!!'
            return False


#specify your query you want the data to be crawled of 
#encoding should always be %23

#some code was used from http://stackoverflow.com/questions/34942103/headless-endless-scroll-selenium

query = "deutschlandlacrosse"
url = "https://twitter.com/search?src=typd&q=%23"+query

print '[*] The crawling beginns..'


driver = webdriver.Firefox(executable_path=r'/path/to/geckodriver/executable')
driver.get(url)

# initial wait for the tweets to load
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

# scroll down to the last tweet until there is no more tweets loaded
while True:
    tweets = driver.find_elements_by_css_selector("li[data-item-id]")
    number_of_tweets = len(tweets)

    driver.execute_script("arguments[0].scrollIntoView();",tweets[-1])

    try:
        wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
        print '[+] keep crawling, crawling , crawling ...'
    except TimeoutException:
        print '[-] Timeout has happend.. please try again..'
        break

page_source = driver.page_source
print '[+] All Tweets are crawled'
driver.close()

#get the relevant information of the tweet (structure stays always the same)
#we get the userId, timestamp, tweet(with hashtags not seperated), count of retweets and likes, images and media

#create the BS4-Object with the scraped page-source

soup = BeautifulSoup(page_source, "html5lib")

print '[*] Data processing has begun...'


#get the userId, timestamp, text of a tweet 

#navigate to the div 'tweet' and after that to the div 'content' for each tweet
for tweet in soup.select("div.tweet div.content"):
    #get the user - ID by getting the content of the attribute 'data-user-id' of the 'a' Tag 
    userId 		= tweet.a.get('data-user-id')

    #get the timestamp by navigating into the small - Tag of the HTML Object and then the 'a' Object and getting the attribute of the 'title'  
    timestamp 	= tweet.small.a.get('title')

    #get the full-tweet by navigating into the 'p' - Tag of the HTML-Objekt and getting the attribute of the 'text' 
    tweetText 	= tweet.p.text
    hasImage = 0
    hasVideo = 0 
    hasUrl = 0
    urlName = "NA"

	#get the favorites for a tweet

    for tag in tweet.select("div.stream-item-footer div.ProfileTweet-actionCountList span.ProfileTweet-action--favorite"):
		likes = tag.span.get('data-tweet-stat-count')


		#get the retweets for a tweet
    for tag in tweet.select("div.stream-item-footer div.ProfileTweet-actionCountList span.ProfileTweet-action--retweet"):
        retweets = tag.span.get('data-tweet-stat-count')
    		#specify the row of data which will be written into the .csv

     #get if tweet contains image
    for tag in tweet.select("div.AdaptiveMedia div.AdaptiveMedia-container div.AdaptiveMedia-singlePhoto"):
    	hasImage=1

  	for tag in tweet.select("div.AdaptiveMedia div.AdaptiveMedia-container div.AdaptiveMedia-triplePhoto"):
  		hasImage=1

    for tag in tweet.select("div.AdaptiveMedia div.AdaptiveMedia-container div.AdaptiveMedia-doublephoto"):
    	hasImage=1

            #get if tweet contains video 
    for tag in tweet.select("div.AdaptiveMedia div.AdaptiveMedia-container div.AdaptiveMedia-video"):
        hasVideo=1


            #get if tweet contains media 
    for tag in tweet.select("div.js-media-container"):
        hasUrl=1

    tweet_data =[userId, timestamp, tweetText,retweets,likes,hasImage,hasVideo,hasUrl]       
                              
    #write the data

    print '[+] Tweet been processed and written'
    writer = csv.writer(open(csvFile, "a"))
    writer.writerow(tweet_data)
    
print '[*] Success.'




