#Classifying Tweets using DatumBox
#the basic free subscription allows you to generate 1000 calls per day. 

#Get API Key from here: http://www.datumbox.com/machine-learning-api/
api_key = '437fcdd9f82be5bf01b5ce54503cae44'

####All this is the code to set up the DatumBox functions for use in Python###
#we can see how a package works using these definitions
from urllib2 import Request, urlopen
from urllib import urlencode
import json
class DatumBox():
	base_url = "http://api.datumbox.com/1.0/"

	def __init__(self, api_key):
		self.api_key = api_key

	def sentiment_analysis(self, text):
		"""Possible responses are "positive", "negative" or "neutral" """
		return self._classification_request(text, "SentimentAnalysis")

	def twitter_sentiment_analysis(self, text):
		"""Possible responses are "positive", "negative" or "neutral" """
		return self._classification_request(text, "TwitterSentimentAnalysis")

	def is_subjective(self, text):
		"""Returns boolean"""
		response = self._classification_request(text, "SubjectivityAnalysis")
		return response == "subjective"

	def topic_classification(self, text):
		"""Possible topics are "Arts", "Business & Economy", "Computers & Technology", "Health", "Home & Domestic Life", "News", "Recreation & Activities", "Reference & Education", "Science", "Shopping","Society" or "Sports"""
		return self._classification_request(text, "TopicClassification")

	def is_spam(self, text):
		"""Returns a boolean"""
		response = self._classification_request(text, "SpamDetection")
		return response == "spam"

	def is_adult_content(self, text):
		"""Returns a boolean"""
		response = self._classification_request(text, "AdultContentDetection")
		return response == "adult"

	def readability_assessment(self, text):
		"""Responses "basic", "intermediate" or "advanced" """
		return self._classification_request(text, "ReadabilityAssessment")

	def detect_language(self, text):
		"""Returns an ISO_639-1 language code"""
		return self._classification_request(text, "LanguageDetection")

	def is_commercial(self, text):
		"""Returns "commercial" or "noncommercial" """
		response = self._classification_request(text, "CommercialDetection")
		return response == "commercial"

	def is_educational(self, text):
		"""Returns boolean"""
		response = self._classification_request(text, "EducationalDetection")
		return response == "educational"

        def keyword_extract(self, text):
  		"""Returns a list of keywords from the given text"""
  		full_url = DatumBox.base_url + "KeywordExtraction.json"
 		text = self.remove_leading_at(text)
  		response = self._send_request(full_url, {'text' : text, 'n' : 1})
  		return response['1'].keys();

	def text_extract(self, text):
		"""Extracts text from a webpage"""
		return self._classification_request(text, "TextExtraction")

  	def document_similarity(self, text, text2):
  		"""Returns number between 0 (No similarity) and 1(Exactly equal)"""
  		full_url = DatumBox.base_url + "DocumentSimilarity.json"
 		text = self.remove_leading_at(text)
 		text2 = self.remove_leading_at(text2)
  		response = self._send_request(full_url, {'original': text, 'copy' : text2})
  		return response['Oliver'];

  	def _classification_request(self, text, api_name):
  		full_url = DatumBox.base_url + api_name + ".json"
 		text = self.remove_leading_at(text)
  		return self._send_request(full_url, {'text' : text})

  	def _send_request(self, full_url, params_dict):
  		params_dict['api_key'] = self.api_key
  		request = Request(url=full_url, data=urlencode(params_dict))
  		f = urlopen(request)
  		response = json.loads(f.read())
  		
  		
  		if "error" in response['output']:
  			raise DatumBoxError(response['output']['error']['ErrorCode'], response['output']['error']['ErrorMessage'])
  		else:
  			return response['output']['result']
  		
	def remove_leading_at(self, text):
		"""The datumbox API throws an unexpected error when the first charater is @ (Which is fairly common in tweets)"""
		return text.lstrip('@')

class DatumBoxError(Exception):
	def __init__(self, error_code, error_message):
		self.error_code = error_code
		self.error_message = error_message

	def __str__(self):
		return "Datumbox API returned an error: " + str(self.error_code) + " " + self.error_message
####All this is the code to set up the DatumBox functions###
  	
  	
#First set up a DataBox Class object - we'll just label it db
db = DatumBox(api_key)
text = "I have eaten Ben and Jerry's Ice Cream nonstop for the past 2 days. Down and out but getting better and fatter!"
db.topic_classification(text)
db.sentiment_analysis(text)
db.twitter_sentiment_analysis(text)
db.is_subjective(text)
db.is_spam(text)
db.is_adult_content(text)
db.readability_assessment(text)
db.detect_language(text)
db.is_commercial(text)
db.is_educational(text)
db.keyword_extract(text)
text2 = 'my dog ate my homework.'
db.document_similarity(text, text2)
text3 = 'my cat is my favorite pet'
db.document_similarity(text2, text3)    
    
#Let's pull in some tweets 
#and cluster and classify them (using our new DatumBox tool)
import twitter, json

CONSUMER_KEY = 'j77LqmDJS8XOxGmLgCLOsbUUc'
CONSUMER_SECRET ='9WxydrLjub2MHdMwKIRUC0WHITlOhtvybZVLuZzrOQCiw7wKXh'
OAUTH_TOKEN = '45766678-PVzgy1nmdfdUUEcFNRKUvZxJ7XKDAwEBjXRAN46tA'
OAUTH_TOKEN_SECRET = 'Z6R70r61kqeEo9EMDKbwyZJTXFRbC90LU13w6j7UWWUNd'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

#Collecting Search Results
q = '#LebronJames' 
count = 100
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']


#Assuming we have already set up the DatumBox "stuff"
db = DatumBox(api_key)

#Extract on the 4 pieces of data that we want (text, location, sentiment and subjective (T/F)
text = []
for s in statuses:
    textdict = {}
    textdict['text'] = s['text'].encode('ascii','replace') #this replaces unicode with ascii text
                                                    #and replaces thumbs up \U0001f44c and smily faces, etc. with ??
    textdict['location'] = s['user']['location'].encode('ascii','replace')
    textdict['twitter_sentiment'] =db.twitter_sentiment_analysis(textdict['text'])
    textdict['subjective'] =db.is_subjective(textdict['text'])
    text.append(textdict)

print text


myOutFile = open('C:\Users\Brandan\Desktop\STAT3700\BDA Final\LebronJamesTweets2.txt', 'w')
print >>myOutFile, '\tSubjective\tText\tLocation\tSentiment' #\t are tabs
for t in text:
    line ='\t'
    for (name, value) in t.items(): #items are subjective, text, location, and sentiment
        line = line + str(value) + '\t'
    print >>myOutFile, line
myOutFile.close()



#Open txt file in Excel and remove extra first and any extra columns at end
#Find and replace all comma with nothing and save as csv file
#'C:\Users\Kellie\SkyDrive\Complex Data Analytics\Student Notes\Module 2\M2L3\myOutFileMarijuanaTexts.csv

#How to export data to power a dendogram and node-link tree visualization as outlined in Figure 4.
import csv
import random
from nltk.metrics.distance import jaccard_distance
#Install cluster from Package Manager before running this 
from cluster import HierarchicalClustering

CSV_FILE = 'C:\Users\Brandan\Desktop\STAT3700\DonaldSterlingtext.csv'

#Note this will overwrite your linkedIn Data file if you already created it in notes - you can rename the linked in one first!

OUT_FILE = 'C:\Users\Brandan\Desktop\STAT3700\d3-data.json'

# Tweak this distance threshold and try different distance calculations 
# during experimentation
DISTANCE_THRESHOLD = 0.5
DISTANCE = jaccard_distance

# Adjust sample size as needed to reduce the runtime of the
# nested loop that invokes the DISTANCE function
SAMPLE_SIZE = 500

def cluster_tweets_by_words(csv_file):
    transforms = [('Donald', 'DonaldSterling'),]
    separators = ['/', 'and', '&']
    csvReader = csv.DictReader(open(csv_file), delimiter=',', quotechar='"')
    tweets = [row for row in csvReader]

    # Normalize and/or replace known abbreviations
    # and build up list of common titles
    all_words = []
    for i, _ in enumerate(tweets):
        if tweets[i]['Text'] == '':
            tweets[i]['Text'] = ['']
            continue
        words = [tweets[i]['Text']]
        for word in words:
            for separator in separators:
                if word.find(separator) >= 0:
                    words.remove(word)
                    words.extend([word.strip() for word in word.split(separator)
                                  if word.strip() != ''])

        for transform in transforms:
            words = [word.replace(*transform) for word in words]
        tweets[i]['Text'] = words
        all_words.extend(words)

        all_words = list(set(all_words))
    
    # Define a scoring function
    def score(word1, word2): 
        return DISTANCE(set(word1.split()), set(word2.split()))

    # Feed the class your data and the scoring function
    hc = HierarchicalClustering(all_words, score)

    # Cluster the data according to a distance threshold
    clusters = hc.getlevel(DISTANCE_THRESHOLD)

    # Remove singleton clusters
    clusters = [c for c in clusters if len(c) > 1]

    # Round up tweets who are in these clusters and group them together
    clustered_tweets = {}
    for cluster in clusters:
        clustered_tweets[tuple(cluster)] = []
        for tweet in tweets:
            for word in tweet['Text']:
                if word in cluster:
                    clustered_tweets[tuple(cluster)].append('%s %s'
                            % (tweet['Text'],tweet['Sentiment']))
    return clustered_tweets


def display_output(clustered_tweets):
    for words in clustered_tweets:
        common_words_heading = 'Common Words: ' + ', '.join(words)
        descriptive_terms = set(words[0].split())
        for word in words:
            descriptive_terms.intersection_update(set(word.split()))
        descriptive_terms_heading = 'Descriptive Terms: ' \
            + ', '.join(descriptive_terms)
        print descriptive_terms_heading
        print '-' * max(len(descriptive_terms_heading), len(common_words_heading))
        print '\n'.join(clustered_tweets[words])
        print

def write_d3_json_output(clustered_tweets):
    json_output = {'name' : 'My LinkedIn', 'children' : []}
    for words in clustered_tweets:
        descriptive_terms = set(words[0].split())
        for word in words:
            descriptive_terms.intersection_update(set(word.split()))

        json_output['children'].append({'name' : ', '.join(descriptive_terms)[:30], 
                                    'children' : [ {'name' : c.decode('utf-8', 'replace')} for c in clustered_tweets[words] ] } )
        f = open(OUT_FILE, 'w')
        f.write(json.dumps(json_output, indent=1))
        f.close()
    
clustered_tweets = cluster_tweets_by_words(CSV_FILE)
display_output(clustered_tweets)
write_d3_json_output(clustered_tweets)

#now we have a d3-data.json.json file with the output
#for the dendogram and node-link tree visualizations,
#Open these 2 html files in Browser (for me only Firefox works):
# node_link_tree.html and dendogram.html
