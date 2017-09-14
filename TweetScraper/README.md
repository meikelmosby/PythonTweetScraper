# Python-TweetScraper enriched with Metadata 

### TweetScraper
- Scrape Tweets by specifying an "query" which stands for your desired hashtag
- The Scraping is done for the whole Timeseries so every tweet which was ever published with the hashtag you specified will be crawled

### Data processing

- The Script generates a .csv with the following datastructure in each row
- ["id", "timestamp", "tweet", "retweets", "likes","hasImage", "hasVideo", "hasUrl"])
- it contains the tweet-id, the timestamp, the tweet itself as a string, the amount of retweets, the amount of likes, if it contains a image, if it contains a video and if it contains a url

### Dependencies

- selenium
- beautifulsoup4
- csv
- geckodriver

##### For questions and more information contact:
 - Ratz Meikel: meikel-ratz@web.de





