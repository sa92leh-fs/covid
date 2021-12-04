{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "d626fafa-c9d1-42c7-8c6e-6eb4dd410b70",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__' (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [04/Dec/2021 21:30:39] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Dec/2021 21:30:39] \"GET /static/pics/abc.png HTTP/1.1\" 304 -\n",
      "[2021-12-04 21:30:48,867] ERROR in app: Exception on /submit [POST]\n",
      "Traceback (most recent call last):\n",
      "  File \"C:\\Users\\rook_\\AppData\\Local\\Temp/ipykernel_29608/3190551872.py\", line 29, in keyword_to_csv\n",
      "    tweets_list = [[tweet.text] for tweet in tweets]\n",
      "  File \"C:\\Users\\rook_\\AppData\\Local\\Temp/ipykernel_29608/3190551872.py\", line 29, in <listcomp>\n",
      "    tweets_list = [[tweet.text] for tweet in tweets]\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\cursor.py\", line 86, in __next__\n",
      "    return self.next()\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\cursor.py\", line 286, in next\n",
      "    self.current_page = next(self.page_iterator)\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\cursor.py\", line 86, in __next__\n",
      "    return self.next()\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\cursor.py\", line 167, in next\n",
      "    data = self.method(max_id=self.max_id, parser=RawParser(), *self.args, **self.kwargs)\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\api.py\", line 33, in wrapper\n",
      "    return method(*args, **kwargs)\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\api.py\", line 46, in wrapper\n",
      "    return method(*args, **kwargs)\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\api.py\", line 1268, in search_tweets\n",
      "    return self.request(\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\tweepy\\api.py\", line 257, in request\n",
      "    raise Unauthorized(resp)\n",
      "tweepy.errors.Unauthorized: 401 Unauthorized\n",
      "89 - Invalid or expired token.\n",
      "\n",
      "During handling of the above exception, another exception occurred:\n",
      "\n",
      "Traceback (most recent call last):\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\flask\\app.py\", line 2073, in wsgi_app\n",
      "    response = self.full_dispatch_request()\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\flask\\app.py\", line 1518, in full_dispatch_request\n",
      "    rv = self.handle_user_exception(e)\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\flask\\app.py\", line 1516, in full_dispatch_request\n",
      "    rv = self.dispatch_request()\n",
      "  File \"C:\\Users\\rook_\\anaconda3\\lib\\site-packages\\flask\\app.py\", line 1502, in dispatch_request\n",
      "    return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)\n",
      "  File \"C:\\Users\\rook_\\AppData\\Local\\Temp/ipykernel_29608/3190551872.py\", line 88, in submit\n",
      "    keyword_to_csv(str(Hashtag), int(Tweets))\n",
      "  File \"C:\\Users\\rook_\\AppData\\Local\\Temp/ipykernel_29608/3190551872.py\", line 41, in keyword_to_csv\n",
      "    time.sleep(3)\n",
      "NameError: name 'time' is not defined\n",
      "127.0.0.1 - - [04/Dec/2021 21:30:48] \"POST /submit HTTP/1.1\" 500 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "failed on_status, 401 Unauthorized\n",
      "89 - Invalid or expired token.\n"
     ]
    }
   ],
   "source": [
    "import tweepy\n",
    "import pandas as pd\n",
    "from flask import Flask, render_template, url_for,request,redirect\n",
    "import os\n",
    "from bs4 import BeautifulSoup\n",
    "from nltk.tokenize import WordPunctTokenizer\n",
    "import re\n",
    "from wordcloud import WordCloud, STOPWORDS\n",
    "import matplotlib.pyplot as plt\n",
    "token = WordPunctTokenizer()\n",
    "#picfolder = os.path.join('Project','templates')\n",
    "#app.config['UPLOAD_FOLDER'] = picfolder\n",
    "consumer_key = \"your private twitter accout key here\" \n",
    "consumer_secret = \"your private twitter accout key here\"\n",
    "access_token = \"your private twitter accout key here\"\n",
    "access_token_secret = \"your private twitter accout key here\"\n",
    "auth = tweepy.OAuthHandler(consumer_key, consumer_secret)\n",
    "auth.set_access_token(access_token, access_token_secret)\n",
    "api = tweepy.API(auth, wait_on_rate_limit=True)\n",
    "PIC_FOLDER = os.path.join('static', 'pics')\n",
    "app = Flask(__name__)\n",
    "app.config['UPLOAD_FOLDER'] = PIC_FOLDER\n",
    "\n",
    "\n",
    "    \n",
    "def keyword_to_csv(keyword,recent):\n",
    "    try:\n",
    "        tweets = tweepy.Cursor(api.search_tweets,q=keyword,lang='en').items(recent) #creates query method\n",
    "        tweets_list = [[tweet.text] for tweet in tweets] \n",
    "        #pulls text information from tweets\n",
    "        df = pd.DataFrame(tweets_list,columns=['Text'])\n",
    "        cleaned_tweets = []\n",
    "        for i in range(0,df.shape[0]):                                                              \n",
    "            cleaned_tweets.append(cleaning_tweets((df.Text[i])))\n",
    "        string = pd.Series(cleaned_tweets).str.cat(sep=' ')\n",
    "        wordcloud(string)\n",
    "        return df\n",
    "         #creates a csv from data frame\n",
    "    except BaseException as e:\n",
    "        print('failed on_status,',str(e))\n",
    "        time.sleep(3)\n",
    "        \n",
    "        \n",
    "\n",
    "def cleaning_tweets(t):\n",
    "    t = ''.join([c for c in t if ord(c) < 128])\n",
    "    t = re.sub(r\"(?:\\@|https?\\://)\\S+\", \"\", t)\n",
    "    del_amp = BeautifulSoup(t, 'lxml')\n",
    "    del_amp_text = del_amp.get_text()\n",
    "    re_list = ['@[A-Za-z0–9_]+', '#']\n",
    "    combined_re = re.compile( '|'.join( re_list) )\n",
    "    del_link_mentions = re.sub(combined_re, '', del_amp_text)\n",
    "    regex_pattern = re.compile(pattern = \"[\"\n",
    "        u\"\\U0001F600-\\U0001F64F\"  # emoticons\n",
    "        u\"\\U0001F300-\\U0001F5FF\"  # symbols & pictographs\n",
    "        u\"\\U0001F680-\\U0001F6FF\"  # transport & map symbols\n",
    "        u\"\\U0001F1E0-\\U0001F1FF\"  # flags (iOS)\n",
    "                           \"]+\", flags = re.UNICODE)\n",
    "    del_emoticons = re.sub(regex_pattern, '', del_link_mentions)\n",
    "    lower_case = del_emoticons.lower()\n",
    "    words = token.tokenize(lower_case)\n",
    "    result_words = [x for x in words if len(x) > 2]\n",
    "    return (\" \".join(result_words)).strip()\n",
    "\n",
    "\n",
    "def wordcloud(string):\n",
    "    stopwords = set(STOPWORDS)\n",
    "    stopwords.update([\"will\",\"pre\",\"\"]) #adding our own stopwords\n",
    "    wordcloud = WordCloud(width=1600, stopwords=stopwords,height=800,max_font_size=200,max_words=50,collocations=False, background_color='black').generate(string)\n",
    "    plt.figure(figsize=(40,30))\n",
    "    #plt.imshow(wordcloud, interpolation=\"bilinear\")\n",
    "    plt.axis(\"off\")\n",
    "    wordcloud.to_file(os.path.join(app.config['UPLOAD_FOLDER'], 'abd.png'))\n",
    "    #wordcloud.to_image('abd.png')\n",
    "    #plt.show()\n",
    "    \n",
    "    \n",
    "@app.route(\"/\")\n",
    "def html():\n",
    "    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'abc.png')\n",
    "    return render_template(\"Twitter.html\",image = full_filename)\n",
    "\n",
    "@app.route('/submit',methods = ['POST', 'GET'])\n",
    "def submit():\n",
    "    if request.method == 'POST':\n",
    "        Hashtag = request.form['Hashtag'] + \" -filter:retweets\" \n",
    "        Tweets = request.form['Tweets']\n",
    "        keyword_to_csv(str(Hashtag), int(Tweets))       \n",
    "        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'abd.png')\n",
    "    return render_template(\"Twitter.html\",image = full_filename,Hashtag=Hashtag,Tweets=Tweets)\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "54656afb-15f5-4b62-b5ca-e5e162b8fe2d",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
