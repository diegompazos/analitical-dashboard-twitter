# Twitter Analytics Dashboard
## Simple Analytical Dashboard using Twitter API

_To install the required libraries, you need to have the package installer pip installed. Refer to the documentation at: https://pypi.org/project/pip/_

Some packages are not native to Python and therefore need to be installed as well:

* ``` pip install pandas ```
* ```pip install textblob ```
* ``` pip install squarify ```
* ``` pip install nltk ```
* ```pip install tweepy ```
* ``` pip install PySimpleGUI ```
  
The following modules belonging to the NLTK library also need to be downloaded for proper functioning:

* ``` nltk.download('vader_lexicon') ```
* ``` nltk.download('vader_lexicon') ```

You need to create a developer account on Twitter (https://developer.twitter.com/en/docs/twitter-api) to use the Twitter API, and to obtain the necessary Keys and Tokens. <b>The approval of these keys may take from 5 to 15 days.</b>

### Observations:

Due to latency issues, the tool may occasionally show the alert "Not responding," but this does not imply a failure in generating the dashboard, which will be created normally.
The path specified for storing the dashboard should be as accurate as possible. By default, it will store the generated dashboard image in the project folder or in the user's folder within the C drive.
 
