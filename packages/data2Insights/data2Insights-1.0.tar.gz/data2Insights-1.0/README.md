Python Package


Data2Insights of python packages can be used to integrate the data2insights services with your applications to enhance services with the data2insighs services. You can use this package easily in the popular framworks and libraries(EX:Python,Flask). Form the below installation command you can download the package.


Library Installation


 > pip3 install data2insights 


Python Text Analytics Models


The Text analysis models can take a text as the input and gives the appropriate predicted results for that model.The input text should contain only alphabets (or) combination of both alphabets and special characters (or) combination of both alphabets and digits,then user gets the predicted result for that model .



Emotion Model

The Emotion model of data2insights will take text as the input and returns the type of emotion of the given text as the response object.

Method Name :

classifiers.emotion(data='provide input text');  # for single text 
batchclassifiers.emotion(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.emotion(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
               "Classifier_id": "Emotion",
               "classifications": {
               "Prediction_accuracy": "36.04",
               "emotion": "Happy",
               "given_text": "hi"
               },
               "content_type": "application-json",
               "query_limit": "1000",
               "query_limit_remaining": "829",
               "query_limit_request": 1,
               "status_code": 200
        }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.emotion(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
	             "Processed_file location": "./outputfiles/3/emotion/data371.csv",
	             "msg": "file_processing_completed",
	             "status_code": 200
        }

Sentiment Model

The Sentiment model of data2insights will take text as the input and return the type of sentiment of the given text as the response object.

Method Name :

classifiers.sentiment(data='provide input text');  # for single text 
batchclassifiers.sentiment(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.sentiment(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Classifier_id": "Sentiment",
          "classifications": {
          "Prediction_accuracy": "99.59",
          "given_text": "hi",
          "sentiment": "Neutral"
          },
          "content_type": "application-json",
          "query_limit": "1000",
          "query_limit_remaining": "830",
          "query_limit_request": 1,
          "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.sentiment(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/sentiment/data372.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Topic Model

The Topic model of data2insights will take text as the input and return the type of topic of the given text as the response object.

Method Name :

classifiers.topic(data='provide input text');  # for single text 
batchclassifiers.topic(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.topic(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
             "Classifier_id": "Topic",
             "classifications": {
             "Prediction_accuracy": "38.10",
             "given_text": "hi",
             "topic": "beauty_style"
             },
             "content_type": "application-json",
             "query_limit": "1000",
             "query_limit_remaining": "815",
             "query_limit_request": 1,
             "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.topic(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/topic/data385.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Spam Model

The Spam model of data2insights will take text as the input and return whether the text is spam or not.

Method Name :

classifiers.spam(data='provide input text');  # for single text 
batchclassifiers.spam(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.spam(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Classifier_id": "Spam",
          "classifications": {
          "Prediction_accuracy": "80.28",
          "given_text": "hi",
          "spam": "NotSpam"
          },
          "content_type": "application-json",
          "query_limit": "1000",
          "query_limit_remaining": "820",
          "query_limit_request": 1,
          "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.spam(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/spam/data386.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Age Model

The Age model of data2insights will predict the age of, who wrote the given input text.

Method Name :

classifiers.age(data='provide input text');  # for single text 
batchclassifiers.age(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.age(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Classifier_id": "Age",
          "classifications": {
          "Prediction_accuracy": "99.08",
          "age": "18_24",
          "given_text": "hi"
          },
         "content_type": "application-json",
         "query_limit": "1000",
         "query_limit_remaining": "828",
         "query_limit_request": 1,
         "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.age(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/age/data388.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Gender Model

The Gender model of data2insights will predict the gender of the, who wrote the given input text either Male or Female.

Method Name :

classifiers.gender(data='provide input text');  # for single text 
batchclassifiers.gender(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.gender(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Classifier_id": "Gender",
          "classifications": {
          "Prediction_accuracy": "99.87",
          "gender": "Female",
          "given_text": "hi"
          },
          "content_type": "application-json",
          "query_limit": "1000",
          "query_limit_remaining": "817",
          "query_limit_request": 1,
          "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.gender(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/gender/data387.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

TweetSentiment Model

Twitter sentiment analysis identifies the opinion of tweet text which has only 280 characters of text as Positive,Neutral,Negative.

Method Name :

classifiers.tweetsentiment(data='provide input text');  # for single text 
batchclassifiers.tweetsentiment(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.tweetsentiment(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Classifier_id": "Tweet_sentiment",
          "classifications": {
          "Prediction_accuracy": "55.24",
          "given_text": "hi",
          "tweetsentiment": "Positive"
          },
         "content_type": "application-json",
         "query_limit": "1000",
         "query_limit_remaining": "819",
         "query_limit_request": 1,
         "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.tweetsentiment(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/tweetsentiment/data389.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Entity Model

The Entity model of data2insights will predict the entities in the given input text(Location,Person, Location, Organisation etc..).

Method Name :

classifiers.entity(data='provide input text');  # for single text 
batchclassifiers.entity(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.entity(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Extraction_id": "Entity",
          "content_type": "application-json",
          "extractions": {
          "entity": [],
          "given_text": "hi"
          },
          "query_limit": "1000",
          "query_limit_remaining": "827",
          "query_limit_request": 1,
          "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.entity(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/entity/data396.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

TweetEntity Model

The Twitter Entity Extraction service allows us to identify the entions,Hashtags,Symbols ,Url’s and User_profile_url’s from given twitter tweets.

Method Name :

classifiers.tweetentity(data='provide input text');  # for single text 
batchclassifiers.tweetentity(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.tweetentity(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Extraction_id": "Tweet_entity",
          "content_type": "application-json",
          "extractions": {
          "given_text": "hi",
          "tweetentity": {
          "Entities": [],
          "Hashtags": [],
          "symbols": [],
          "urls": [],
          "user_profiles_url": [],
          "users": []
         }
        },
         "query_limit": "1000",
         "query_limit_remaining": "818",
         "query_limit_request": 1,
         "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.tweetentity(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/tweetentity/data420.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Keyword Model

The Keyword model of data2insights will take text as the input and return keywords in the given text.

Method Name :

classifiers.keyword(data='provide input text');  # for single text 
batchclassifiers.keyword(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.keyword(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Extraction_id": "Keyword",
          "content_type": "application-json",
          "extractions": {
          "given_text": "hi",
          "keywords": []
          },
         "query_limit": "1000",
         "query_limit_remaining": "826",
         "query_limit_request": 1,
         "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.keyword(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/keyword/data397.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

UrlExtraction Model

The Url Extraction service allows us to identity the full content,title,html page,top image,authors,keyword,summary and publication date from the given url.

Method Name :

text->classifiers.urlextraction(data='provide input text');  # for single text 
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.urlextraction(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Extraction_id": "Url_extraction",
          "content_type": "application-json",
          "extractions": {
          "Response": {
          "ALL_IMAGES_URLS": [
          "https://i.stack.imgur.com/ziXaw.jpg?s=32&g=1"
          ],
          "AUTHORS": [],
          "FULL CONTENT": "I am using requests to get the image from remote URL. Since the images will always be 16x16, I want to convert them to base64 , so that I can embed them later to use in HTML img tag.

import requests import base64 response = requests.get(url).content print(response) b = base64.b64encode(response) src = "data:image/png;base64," + b

The output for response is:

response = b'GIF89a\x80\x00\x80\x00\xc4\x1f\x00\xff\xff\xff\x00\x00\x00\xff\x00\x00\xff\x88\x88"""\xffff\...

The HTML part is:

<img src="{{src}}"/>

But the image is not displayed.",
          "HTML_PAGE": "<div><p>I am using <code>requests</code> to get the image from remote URL. Since the images will always be 16x16, I want to convert them to <code>base64</code>, so that I can embed them later to use in HTML <code>img</code> tag.</p>

<pre><code>import requests
import base64
response = requests.get(url).content
print(response)
b = base64.b64encode(response)
src = "data:image/png;base64," + b
</code></pre>

<p>The output for <code>response</code> is:</p>

<pre><code>response = b'GIF89a\x80\x00\x80\x00\xc4\x1f\x00\xff\xff\xff\x00\x00\x00\xff\x00\x00\xff\x88\x88"""\xffff\...
</code></pre>

<p>The HTML part is:</p>

<pre><code>&lt;img src="{{src}}"/&gt;
</code></pre>

<p>But the image is not displayed.</p>

<p>How can I properly base-64 encode the <code>response</code>?</p>
    </div>",
      "KEYWORDS": [
      "url",
      "base64",
      "image",
      "tagimport",
      "src",
      "requests",
      "using",
      "response",
      "python",
      "html",
      "srcsrcbut"
    ],
      "PUBLICATION DATE": null,
      "SUMMARY": "I am using requests to get the image from remote URL.
Since the images will always be 16x16, I want to convert them to base64 , so that I can embed them later to use in HTML img tag.
import requests import base64 response = requests.get(url).content print(response) b = base64.b64encode(response) src = "data:image/png;base64," + bThe output for response is:response = b'GIF89a\x80\x00\x80\x00\xc4\x1f\x00\xff\xff\xff\x00\x00\x00\xff\x00\x00\xff\x88\x88"""\xffff\...
The HTML part is:<img src="{{src}}"/>But the image is not displayed.",
      "TITLE": "Python requests base64 image",
      "TOP_IMAGE": "https://cdn.sstatic.net/Sites/stackoverflow/Img/apple-touch-icon@2.png?v=73d79a89bded"
      },
     "given_url": "https://stackoverflow.com/questions/30280495/python-requests-base64-image"
     },
    "query_limit": "1000",
    "query_limit_remaining": "825",
    "query_limit_request": 1,
    "status_code": 200

            }

Personalitytraits Model

The Personality Traits model of data2insights will take text as the input and return the Personality Traits of the given text as the response object.

Method Name :

classifiers.personalitytraits(data='provide input text');  # for single text 
batchclassifiers.personalitytraits(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.personalitytraits(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
            Classifier_id: 'Topic',
            classifications: {
              Prediction_accuracy: '85.09',
              given_text: 'Welcome to d2i',
              topic: 'recreation'
            },
            content_type: 'application-json',
            query_limit: '5000',
            query_limit_remaining: '4935',
            query_limit_request: 1,
            status_code: 200
          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.personalitytraits(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
            "Processed_file location": "./outputfiles/102/personalityTraits/Sample-Spreadsheet-10-rows221.xls",
            "msg": "file_processing_completed",
            "status_code": 200
        }

Readability Model

The Readability model of data2insights will take text as the input and return the type of some metrics of the given text as the response object.

Method Name :

classifiers.readability(data='provide input text');  # for single text 
batchclassifiers.readability(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.readability(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Metrics": {
          "document_readability": {
          "Automated_Readability_Index": -11.6,
          "Coleman_liau_index": -33.81,
          "Dalechal": 0.05,
          "Flesch_Kindrade_Grade": -3.5,
          "Flesch_Reading_Score": 121.22,
          "Gunning_Fog": 0.4,
          "Linsear_Write": -0.5,
          "Smog_index": 0.0
        },
        "given_text": "hi"
      },
         "Metrix_id": "Document_readability",
         "content_type": "application-json",
         "query_limit": "1000",
         "query_limit_remaining": "824",
         "query_limit_request": 1,
         "status_code": 200

          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.readability(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/readability/data421.csv",
          "msg": "file_processing_completed",
          "status_code": 200

        }

Similarity Model

The Similarity model of data2insights will find the similarity between two texts.

Method Name :

text->classifiers.similarity(data1='provide text',data2='provide text');  # for single text 
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.similarity(data1='provide text',data2='provide text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Metrics": {
          "Cosine_similarity": 0.0,
          "Jaccard_similarity": 0.0,
          "given_text1": "hi",
          "given_text2": "hello"
          },
          "Metrix_id": "Document_similarity",
          "content_type": "application-json",
          "query_limit": "1000",
          "query_limit_remaining": "823",
          "query_limit_request": 1,
          "status_code": 200

          }

QandA Model

The Q&A model of data2insights will find the answer for the given question from the given paragraph.

Method Name :

classifiers.QA(question='provide question', paragraph='provide paragraph');  # for single text 
batchclassifiers.QA(column1='provide question column number',column2='provide paragraph column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.QA(question='provide question', paragraph='provide paragraph')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
            content_type: 'application-json',
            'q&a': {
              Answer: 'welcome to data2insights',
              given_paragraph: 'welcome to data2insights',
              given_question: 'welcome to d2i?'
            },
            query_limit: '5000',
            query_limit_remaining: '4923',
            query_limit_request: 1,
            status_code: 200
          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.QA(column1='provide question column number',column2='provide paragraph column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
            "Processed_file location": "./outputfiles/102/QandA/Sample-Spreadsheet-10-rows221.xls",
            "msg": "file_processing_completed",
            "status_code": 200
        }

HempTopic Model

The HempTopic model of data2insights will helps you in identifying topics.

Method Name :

classifiers.hemptopic(data='provide input text');  # for single text 
batchclassifiers.hemptopic(column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.hemptopic(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Classification_id": "Hemptopic",
          "classifications": {
          "Prediction_accuracy": "83.65",
          "given_text": "hi",
          "hemptopic": "Beauty"
          },
          "content_type": "application-json",
          "query_limit": "1000",
          "query_limit_remaining": "814",
          "query_limit_request": 1,
          "status_code": 200


          }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.hemptopic(column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Processed_file location": "./outputfiles/3/hemptopic/data502.csv",
          "msg": "file_processing_completed",
          "status_code": 200
         }

BertEntity Model

The BertEntity model of data2insights will helps you to identify the entities.

Method Name :

classifiers.bertentity(data='provide input text');  # for single text 
batchclassifiers.bertentity((column='provide column number',files={'file': open('provide full path of file', 'rb')}); # for batch process
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.bertentity(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
          "Extraction_id": "Bertentity",
          "content_type": "application-json",
          "extractions": {
          "Bertentity": [
          {
           "bertentity": "O",
           "text": "hi"
          }
        ],
         "given_text": "hi"
        },
         "query_limit": "1000",
         "query_limit_remaining": "813",
         "query_limit_request": 1,
         "status_code": 200
        }
Example for batch text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.batchclassifiers.bertentity((column='provide column number',files={'file': open('provide full path of file', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
            "Processed_file location": "./outputfiles/3/bertentity/data501.csv",
            "msg": "file_processing_completed",
            "status_code": 200
         }

Summarization Model

The Summarization model of data2insights will helps you summarize the given text.

Method Name :

text->classifiers.summarization(data='provide input text');  # for single text 
Example for single text :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.classifiers.summarization(data='provide input text')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    

Python Vision Analytics Models


The Vision analysis models can take a image as the input and gives the appropriate predicted results for that model.The input image should contain .png (or) .jpeg formats only and it should be either local file or remote file url.



Logo Model

The Logo model of data2insights will predict the 27 types of logos from the given input image.

Method Name :

visionclassifiers.logo(data='provide image url');  
visionclassifiers.logoupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.logo(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
        "Classifier_id": "Logo",
        "classifications": {
        "Logos": []
        },
        "content_type": "application-json",
        "query_limit": "1000",
        "query_limit_remaining": "812",
        "query_limit_request": 1,
        "status_code": 200

      }
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.logoupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
        "Classifier_id": "Logo",
        "classifications": {
        "Logos": []
        },
        "content_type": "application-json",
        "query_limit": "1000",
        "query_limit_remaining": "774",
        "query_limit_request": 1,
        "status_code": 200
      }

Bird Model

The Bird model of data2insights will predict the 27 types of birds from the given input image.

Method Name :

visionclassifiers.bird(data='provide image url');  
visionclassifiers.birdupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.bird(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {"Classifier_id": "Bird",
  "classifications": {
    "Birds": [
      {
        "Bird": "toucan_bird",
        "Coordinates": {
          "Bottom": 771.510648727417,
          "Left": 53.76867055892944,
          "Right": 1191.6043281555176,
          "Top": 14.702987670898438
        },
        "Prediction_accuracy": 99,
        "bird": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "794",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.birdupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
       "Classifier_id": "Bird",
  "classifications": {
    "Birds": [
      {
        "Bird": "parrot_bird",
        "Coordinates": {
          "Bottom": 523.5589575767517,
          "Left": 60.50408989191055,
          "Right": 711.0763740539551,
          "Top": 58.13420504331589
        },
        "Prediction_accuracy": 92,
        "bird": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "772",
  "query_limit_request": 1,
  "status_code": 200
}

Transport Model

The Transport model of data2insights will predict the vehicle types from the given input image.

Method Name :

visionclassifiers.transport(data='provide image url');  
visionclassifiers.transportupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.transport(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Transport",
  "classifications": {
    "Transports": [
      {
        "Coordinates": {
          "Bottom": 800.0,
          "Left": 46.82081937789917,
          "Right": 1174.506425857544,
          "Top": 8.72507095336914
        },
        "Prediction_accuracy": 76,
        "Transport": "auto",
        "transport": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "785",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.transportupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Transport",
	"classifications": {
		"Transports": [{
			"Coordinates": {
				"Bottom": 502.32422828674316,
				"Left": 41.04209750890732,
				"Right": 651.0549342632294,
				"Top": 30.10187178850174
			},
			"Prediction_accuracy": 31,
			"Transport": "aeroplane",
			"transport": 1
		}]
	},
	"content_type": "application-json",
	"query_limit": "1000",
	"query_limit_remaining": "771",
	"query_limit_request": 1,
	"status_code": 200

}

Plant Model

The Plant model of data2insights will predict the plant types from the given input image.

Method Name :

visionclassifiers.plant(data='provide image url');  
visionclassifiers.plantupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.plant(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {"Classifier_id": "Plant",
  "classifications": {
    "Plants": [
      {
        "Coordinates": {
          "Bottom": 754.0493965148926,
          "Left": 9.73820686340332,
          "Right": 1200.0,
          "Top": 27.520751953125
        },
        "Plant": "plants_indoor",
        "Prediction_accuracy": 58,
        "plant": 1
      },
      {
        "Coordinates": {
          "Bottom": 800.0,
          "Left": 54.79602813720703,
          "Right": 1131.5191984176636,
          "Top": 10.229825973510742
        },
        "Plant": "plants_outdoor",
        "Prediction_accuracy": 53,
        "plant": 2
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "803",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.plantupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Plant",
 "classifications": {
   "Plants": [
     {
       "Coordinates": {
         "Bottom": 490.9296751022339,
         "Left": 0.0,
         "Right": 730.0,
         "Top": 24.103980362415314
       },
       "Plant": "plants_indoor",
       "Prediction_accuracy": 54,
       "plant": 1
     }
   ]
 },
 "content_type": "application-json",
 "query_limit": "1000",
 "query_limit_remaining": "769",
 "query_limit_request": 1,
 "status_code": 200

}

Age Model

The Age model of data2insights will predict the age of the persons from the given input image.

Method Name :

visionclassifiers.age(data='provide image url');  
visionclassifiers.ageupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.age(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
        "Classifier_id": "Age",
  "classifications": {
    "Faces": [
      {
        "Age": "31-55",
        "Coordinates": {
          "Bottom": 287.21981048583984,
          "Left": 505.4616093635559,
          "Right": 690.896487236023,
          "Top": 18.590307235717773
        },
        "Face": 1,
        "Predicted_accuracy": 51
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "798",
  "query_limit_request": 1,
  "status_code": 200

}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.ageupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {

 "Classifier_id": "Age",
 "classifications": {
   "Faces": []
 },
 "content_type": "application-json",
 "query_limit": "1000",
 "query_limit_remaining": "761",
 "query_limit_request": 1,
 "status_code": 200

}

Gender Model

The Gender model of data2insights will predict the gender of the persons from the given input image.

Method Name :

visionclassifiers.gender(data='provide image url');  
visionclassifiers.genderupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.gender(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Gender",
  "classifications": {
  "Faces": [
      {
        "Coordinates": {
          "Bottom": 295.8600044250488,
          "Left": 507.1301221847534,
          "Right": 694.7623014450073,
          "Top": 10.44924259185791
        },
        "Face": 1,
        "Gender": "Male",
        "Predicted_accuracy": 99
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "777",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.genderupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Gender",
  "classifications": {
    "Faces": []
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "763",
  "query_limit_request": 1,
  "status_code": 200

}

Emotion Model

The Emotion model of data2insights will predict the emotion of the person from the given input image.

Method Name :

visionclassifiers.emotion(data='provide image url');  
visionclassifiers.emotionupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.emotion(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {"Classifier_id": "Emotion",
  "classifications": {
    "Faces": [
      {
        "Coordinates": {
          "Bottom": 283.68217945098877,
          "Left": 519.590413570404,
          "Right": 677.3368835449219,
          "Top": 43.988871574401855
        },
        "Emotion": "Neutral",
        "Face": 1,
        "Predicted_accuracy": 54
      },
      {
        "Coordinates": {
          "Bottom": 282.6207637786865,
          "Left": 510.5981111526489,
          "Right": 689.1172885894775,
          "Top": 29.67963218688965
        },
        "Emotion": "Surprise",
        "Face": 2,
        "Predicted_accuracy": 37
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "792",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.emotionupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Emotion",
  "classifications": {
    "Faces": []
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "762",
  "query_limit_request": 1,
  "status_code": 200

}

Color Model

The Color model of data2insights will predict the different color from the given input image.

Method Name :

visionclassifiers.color(data='provide image url');  
visionclassifiers.colorupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.color(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
        "Classifier_id": "Color",
  "classifications": {
    "Faces": [
      {
        "Color": "white_people",
        "Coordinates": {
          "Bottom": 791.8387413024902,
          "Left": 224.97146129608154,
          "Right": 987.045407295227,
          "Top": 47.0322847366333
        },
        "Face": 1,
        "Predicted_accuracy": 99
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "799",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.colorupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Color",
  "classifications": {
    "Faces": [
      {
        "Color": "white_people",
        "Coordinates": {
          "Bottom": 513.8462805747986,
          "Left": 38.191078901290894,
          "Right": 642.4347186088562,
          "Top": 38.06664854288101
        },
        "Face": 1,
        "Predicted_accuracy": 96
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "760",
  "query_limit_request": 1,
  "status_code": 200

}

Scene Model

The Scene model of data2insights will predict the different scenes from the given input image.

Method Name :

visionclassifiers.scene(data='provide image url');  
visionclassifiers.sceneupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.scene(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {"Classifier_id": "Scene",
  "classifications": {
    "Scenes": [
      {
        "Coordinates": {
          "Bottom": 795.6767559051514,
          "Left": 211.76365613937378,
          "Right": 954.124116897583,
          "Top": 36.2668514251709
        },
        "Prediction_accuracy": 48,
        "Scene": "Office_building",
        "scene": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "790",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.sceneupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Scene",
  "classifications": {
    "Scenes": [
      {
        "Coordinates": {
          "Bottom": 795.6767559051514,
          "Left": 211.76365613937378,
          "Right": 954.124116897583,
          "Top": 36.2668514251709
        },
        "Prediction_accuracy": 48,
        "Scene": "Office_building",
        "scene": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "790",
  "query_limit_request": 1,
  "status_code": 200

}

Weather Model

The Weather model of data2insights will predict the weather in the given input image.

Method Name :

visionclassifiers.weather(data='provide image url');  
visionclassifiers.weatherupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.weather(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Weather",
  "classifications": {
    "Scenes": [
      {
        "Coordinates": {
          "Bottom": 786.3454818725586,
          "Left": 22.405779361724854,
          "Right": 1196.6458797454834,
          "Top": 62.87107467651367
        },
        "Prediction_accuracy": 90,
        "Weather": "weather_cloudy",
        "scene": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "789",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.weatherupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Weather",
	"classifications": {
		"Scenes": [{
			"Coordinates": {
				"Bottom": 521.9473385810852,
				"Left": 9.529821276664734,
				"Right": 723.5642737150192,
				"Top": 29.81929510831833
			},
			"Prediction_accuracy": 99,
			"Weather": "weather_snowy",
			"scene": 1
		}]
	},
	"content_type": "application-json",
	"query_limit": "1000",
	"query_limit_remaining": "764",
	"query_limit_request": 1,
	"status_code": 200

}

Violence Model

The Violence model of data2insights will predict the violence from the given input image.

Method Name :

visionclassifiers.violence(data='provide image url');  
visionclassifiers.violenceupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.violence(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {"Classifier_id": "Violence",
  "classifications": {
    "Scenes": [
      {
        "Coordinates": {
          "Bottom": 797.3269462585449,
          "Left": 111.29786968231201,
          "Right": 1200.0,
          "Top": 0.0
        },
        "Prediction_accuracy": 99,
        "Violence": "war",
        "scene": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "787",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.violenceupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Violence",
  	"classifications": {
  		"Scenes": [{
  			"Coordinates": {
  				"Bottom": 527.7309834957123,
  				"Left": 62.09136366844177,
  				"Right": 730.0,
  				"Top": 0.0
  			},
  			"Prediction_accuracy": 99,
  			"Violence": "war",
  			"scene": 1
  		}, {
  			"Coordinates": {
  				"Bottom": 527.7526861429214,
  				"Left": 13.07406336069107,
  				"Right": 720.9626841545105,
  				"Top": 16.71631395816803
  			},
  			"Prediction_accuracy": 60,
  			"Violence": "violence",
  			"scene": 2
  		}]
  	},
  	"content_type": "application-json",
  	"query_limit": "1000",
  	"query_limit_remaining": "766",
  	"query_limit_request": 1,
  	"status_code": 200

}

TLO Model

The Tlo model of data2insights will predict the trees,laks, and oceans from the given input image.

Method Name :

visionclassifiers.tlo(data='provide image url');  
visionclassifiers.tloupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.tlo(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {"Classifier_id": "Tlo",
  "classifications": {
    "Scenes": [
      {
        "Coordinates": {
          "Bottom": 784.9786281585693,
          "Left": 15.252542495727539,
          "Right": 1200.0,
          "Top": 68.20473670959473
        },
        "Prediction_accuracy": 99,
        "Tlo": "lake",
        "scene": 1
      }
    ]
  },
  "content_type": "application-json",
  "query_limit": "1000",
  "query_limit_remaining": "788",
  "query_limit_request": 1,
  "status_code": 200
}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.tloupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {
  "Classifier_id": "Tlo",
	"classifications": {
		"Scenes": [{
			"Coordinates": {
				"Bottom": 510.66392064094543,
				"Left": 18.766419291496277,
				"Right": 719.1625744104385,
				"Top": 101.74509018659592
			},
			"Prediction_accuracy": 99,
			"Tlo": "lake",
			"scene": 1
		}]
	},
	"content_type": "application-json",
	"query_limit": "1000",
	"query_limit_remaining": "765",
	"query_limit_request": 1,
	"status_code": 200

}

General Objects Model

The Object model of data2insights will predict the different types of general objects from the given input image.It predicts 545 types of objects.

Method Name :

visionclassifiers.generalobject(data='provide image url');  
visionclassifiers.generalobjectupload(files={'file': open('provide image full path', 'rb')});
Example for image URL :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.generalobject(data='provide image url')

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {

	"Classifier_id": "General_Object",

	"classifications": {

		"GeneralObjects": [

			{

				"Class": "Clothing",

				"Coordinates": {

					"Bottom": 781.9650173187256,

					"Left": 326.60393714904785,

					"Right": 913.2122039794922,

					"Top": 258.1010580062866

				},

				"Object": 1,

				"Score": 73

			},

			{

				"Class": "Face",

				"Coordinates": {

					"Bottom": 274.97315406799316,

					"Left": 508.36490392684937,

					"Right": 689.9345397949219,

					"Top": 28.40385138988495

				},

				"Object": 2,

				"Score": 54

			},

			{

				"Class": "Person",

				"Coordinates": {

					"Bottom": 795.4741477966309,

					"Left": 309.1881036758423,

					"Right": 943.9865827560425,

					"Top": 30.157431960105896

				},

				"Object": 3,

				"Score": 42

			},

			{

				"Class": "Man",

				"Coordinates": {

					"Bottom": 794.6691036224365,

					"Left": 319.6103096008301,

					"Right": 909.6429347991943,

					"Top": 29.600465297698975

				},

				"Object": 4,

				"Score": 40

			}

		]

	},

	"content_type": "application-json",

	"status_code": 200,

	"query_limit": "10000",

	"query_limit_remaining": "9287",

	"query_limit_request": 1

}
Example for upload local image :

from data2Insights import data2insights

# Use the API key,account Id and email Id  from your account,
credentials = data2insights('provide accountid','provide apikey','provide userid')

# Pass the input as parameter to the method
credentials.visionclassifiers.generalobjectupload(files={'file': open('provide image full path', 'rb')})

Output:

#This is exactly the parsed JSON that the Data2Insights API returns!
    {

	"Classifier_id": "General_Object",

	"classifications": {

		"GeneralObjects": [

			{

				"Class": "Clothing",

				"Coordinates": {

					"Bottom": 781.9650173187256,

					"Left": 326.60393714904785,

					"Right": 913.2122039794922,

					"Top": 258.1010580062866

				},

				"Object": 1,

				"Score": 73

			},

			{

				"Class": "Face",

				"Coordinates": {

					"Bottom": 274.97315406799316,

					"Left": 508.36490392684937,

					"Right": 689.9345397949219,

					"Top": 28.40385138988495

				},

				"Object": 2,

				"Score": 54

			},

			{

				"Class": "Person",

				"Coordinates": {

					"Bottom": 795.4741477966309,

					"Left": 309.1881036758423,

					"Right": 943.9865827560425,

					"Top": 30.157431960105896

				},

				"Object": 3,

				"Score": 42

			},

			{

				"Class": "Man",

				"Coordinates": {

					"Bottom": 794.6691036224365,

					"Left": 319.6103096008301,

					"Right": 909.6429347991943,

					"Top": 29.600465297698975

				},

				"Object": 4,

				"Score": 40

			}

		]

	},

	"content_type": "application-json",

	"status_code": 200,

	"query_limit": "10000",

	"query_limit_remaining": "9287",

	"query_limit_request": 1

}
