import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
from datetime import date
import re
import string
from collections import Counter
import sys
import os
import squarify
from PySimpleGUI import PySimpleGUI as sg 

def dash_func():

  auth = tweepy.OAuthHandler('', 
  '')

  auth.set_access_token('', 
  '')

  ttapi = tweepy.API(auth)
  json_data = ''
  total_tweets = 1000
  positive = 0
  negative = 0
  neutral = 0
  topic = valores['topicIn']

  tweets = tweepy.Cursor(ttapi.search, q=topic +' -filter:retweets', result_type="recent").items(total_tweets)

  # Busca dos tweets
  for tweet in tweets:
      json_data += json.dumps(tweet._json, separators=(',', ':'))
      analysis = TextBlob(tweet.text)
      score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
      neg = score['neg']
      neu = score['neu']
      pos = score['pos']
      comp = score['compound']
    
      if neg > pos:
        negative += 1

      elif pos > neg:
        positive += 1
      
      elif pos == neg:
        neutral += 1

  json_correct_raw = '[' + json_data[:len(json_data)] + ']'
  json_correct = json_correct_raw.replace('}{', '},{')

  raw_data = json.loads(json_correct)
  dataframe_raw = pd.json_normalize(raw_data)

  # Filtragem de colunas desejadas

  selected_items = ['text', 'metadata.iso_language_code', 
  'retweet_count', 'favorite_count', 'created_at']
  
  columns_filter = dataframe_raw.filter(items = selected_items)

  # Gráficos por idioma
  language_ranking = columns_filter['metadata.iso_language_code'].value_counts()

  language_labels = [x.upper() for x in language_ranking.index.tolist()]
  language_values = language_ranking.values.tolist()

  # Gráfico de principais palavras
  filter_language = columns_filter['metadata.iso_language_code'] == 'en'

  dataframe_raw_en_only = columns_filter[filter_language]
  dataframe_raw_en_only = dataframe_raw_en_only['text']

  dataframe_no_user = dataframe_raw_en_only.apply(lambda tweet_txt: re.sub('@[^\s]+', '', tweet_txt))
  dataframe_no_user = pd.DataFrame(dataframe_no_user)
  dataframe_no_user.text = dataframe_no_user['text'].str.lower()

  top_words = Counter(" ".join(dataframe_no_user.text).split()).most_common(5000)

  selected_columns = ['Word', 'Appearances']
  dataframe_words = pd.DataFrame(top_words, columns = selected_columns)

  stop = stopwords.words('english')

  dataframe_words['Word'] = dataframe_words['Word'].apply(lambda x: ''.join([Word for Word in x.split() if Word not in (stop)]))

  len_min = 2
  filter_words = dataframe_words['Word'].map(len) > len_min

  dataframe_words = dataframe_words[filter_words]

  dataframe_words = dataframe_words.head(10)

  words = dataframe_words['Word'].str.upper()
  appearances = dataframe_words['Appearances']

  # Gráfico de likes e retweets
  total_likes = columns_filter.favorite_count.sum()
  total_retweets = columns_filter.retweet_count.sum()

  values_likes_retweets = [total_likes, total_retweets]
  labels_likes_retweets = ['Likes' + ' [' + str(total_likes) +']', 'Retweets'  + ' [' + str(total_retweets) +']']

  # Gráfico da quantidade na última hora
  dataframe_time = columns_filter.created_at

  today = datetime.now()
  dataframe_time = pd.DataFrame(dataframe_time)

  dataframe_time["Convertido"] = pd.to_datetime(dataframe_time['created_at'], format= '%a %b %d %H:%M:%S +0000 %Y')

  dataframe_time["Last Hour"] = ((dataframe_time["Convertido"] - today).dt.total_seconds() / 60)

  ft_hr = dataframe_time["Last Hour"] >= -60
  ft_ha_hr = dataframe_time["Last Hour"] >= -30
  ft_qt_hr = dataframe_time["Last Hour"] >= -15
  ft_min = dataframe_time["Last Hour"] >= -1

  dataframe_lasthour = dataframe_time[ft_hr]

  count_lh = dataframe_lasthour.shape[0]
  count_total = total_tweets - count_lh
  labels_tweets_time = ['Last hour ' + '[' +str(count_lh) + ' Tweets]', 'Previous Period' + ' ['+str(count_total) + ' Tweets]',]
  values_tweets_time = [count_lh, count_total]

  ## Gráfico de distribuição por tempo
  dataframe_percent = dataframe_time

  dataframe_last_half_hour = dataframe_percent[ft_ha_hr]
  dataframe_last_quarter_hour = dataframe_percent[ft_qt_hr]
  dataframe_last_min = dataframe_percent[ft_min]

  last_min_qt = dataframe_last_min.shape[0]
  last_15min_qt = dataframe_last_quarter_hour.shape[0] - last_min_qt
  last_halfhour_qt = dataframe_last_half_hour.shape[0] - (last_15min_qt + last_min_qt)
  last_hour_qt = count_lh - (last_halfhour_qt + last_15min_qt + last_min_qt)

  data_percent_time = {'Last Minute': last_min_qt, '1 and 15 minutes': last_15min_qt, '15 and 30 Minutes': last_halfhour_qt, '30 minutos and 1 Hour': last_hour_qt, '1 Hour or more': count_total}

  values_percent_posts = [value for value in data_percent_time.values() if value!=0]
  labels_percent_posts = [key for key,value in data_percent_time.items() if value!=0]

  # Gráfico de sentimentos
  def percentage(part , whole):
    return 100 * float(part)/float(whole)

  positive = percentage(positive, total_tweets)
  negative = percentage(negative, total_tweets)
  neutral = percentage(neutral, total_tweets)
  positive = format(positive, '.1f')
  negative = format(negative, '.1f')
  neutral = format(neutral, '.1f')

  labelsSentiments = ['Positive' , 'Neutral','Negative']
  sizesSentiments = [positive, neutral, negative]
  colorsSentiments = ['yellowgreen', 'blue','red']

  # Dashboard Final
  final_dashboard = plt.figure(figsize=(10, 5), dpi=80)
  final_dashboard.suptitle(str(topic) + ' Data Analysis', x = 1.5, y = 3.65 , fontsize=22)

  # Plot de palavras
  graph_words = final_dashboard.add_axes([0.25, 2.25, 0.45, 1])
  graph_words.barh(words, appearances)
  graph_words.set_title('Most Common Words',  y = 1.05, fontsize = 15)

  # Plot de likes e retweets
  graph_likes_retweets = final_dashboard.add_axes([1.25, 2.25, 0.45, 1])
  graph_likes_retweets.barh(labels_likes_retweets, values_likes_retweets, color = ['red', 'green'])
  graph_likes_retweets.set_title('Likes and Retweets', y = 1.05, fontsize = 15)

  # Plot de idiomas
  graph_language = final_dashboard.add_axes([2.25, 2.25, 0.45, 1])
  graph_language = squarify.plot(sizes = language_values, label = language_labels[:5], alpha=.99 )
  graph_language.set_title('Most Common Languages', y = 1.05, fontsize = 15)
  graph_language.axis('off')

  # Plot de sentimentos
  graph_sentiments = final_dashboard.add_axes([0.25, 0.75, 0.45, 1], aspect=0.25)
  graph_sentiments.pie(sizesSentiments, colors = colorsSentiments, autopct='%1.1f%%', radius = 1.5)
  graph_sentiments.set_title('Sentiment Analysis', y = 1.15, fontsize = 15)
  graph_sentiments.legend(labelsSentiments, bbox_to_anchor=(1.25, 1.0))

  # Plot de distribuição percentual
  graph_percentage_distribution = final_dashboard.add_axes([1.25, 0.75, 0.45, 1], aspect=0.25)
  graph_percentage_distribution.pie(values_percent_posts, autopct='%1.1f%%', radius = 1.5)
  graph_percentage_distribution.set_title('Tweet Posts Distribution', y = 1.15, fontsize = 15)
  graph_percentage_distribution.legend(labels_percent_posts, bbox_to_anchor=(1.25, 1.0))

  # Plot de contagem por períodos
  graph_hour_count_time = final_dashboard.add_axes([2.25, 0.75, 0.45, 1])
  graph_hour_count_time.bar(labels_tweets_time, values_tweets_time, color = ['Blue', 'Yellow'])
  graph_hour_count_time.set_title('Last Hour Posts and Previous', y = 1.05, fontsize = 15)

  plt.savefig("resultado", bbox_inches='tight')
  janela.close()

#########################

sg.theme('Reddit')
layout = [
    [sg.Text('Assunto'), sg.Input(key='topicIn')],
    [sg.Button('Pesquisar')]
    ]

janela = sg.Window('Dashboard Analytics', layout)

while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
      break
    if eventos == 'Pesquisar':
      if  valores['topicIn'] != '':
        dash_func()
      else:
        print("Tópico inválido.")

janela.close()