# My new (and first) Flask app: SEO_keyword_extract - version 1.5;
#
# New scraper (Flask) idea - scrape keywords from blogs;
#
# Author: Andrei C. Cojocaru
# Github: https://github.com/andreireporter13
# LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
# Twitter: https://twitter.com/andrei_reporter
# Website: https://ideisioferte.ro && https://webautomation.ro
#
# Libraries for request and prepare text to extract keywords;
import requests
from bs4 import BeautifulSoup
from rake_nltk import Rake
from fake_useragent import UserAgent

#
from time import sleep

# Flask dependencies;
from flask import Flask, render_template, request, flash, url_for


app = Flask(__name__)
app.secret_key = "cocolin@_linxus_111221_#1101"


#--------------------------------------------> functions for extract text <-------------------------------------------------
def set_headers():

    """ 
    This function is about setting headers for new requests. Is important step to scraping!
    """
    user_agent = UserAgent() # after set a random fake_useragent;

    HEADERS = {
        'User-Agent': user_agent.random,
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return HEADERS


def extract_text(link):

    """ 
    This function extract text from link and return all text with h1, h2, h3 and p elements;
    """

    response = requests.get(link, headers=set_headers())
    sleep(1.5)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

        # concatenate text here...
        concat_text = ''

        # try find h1;
        try:
            h1 = soup.find('h1').text

            if h1: 
                concat_text += h1 + '\n'

        except:
            h1 = ''       

        # try to find h2;
        try:
            h2 = soup.find_all('h2')

            # if h2 exist in the blog post;
            if h2:
                for elem_h2 in h2:
                    concat_text += elem_h2.text + '\n'

        except:
            h2 = ''


        # try to find h3;
        try:
            h3 = soup.find_all('h3')

            # if h3 exist in the blog post;
            if h3:               
                for elem_h3 in h3: 
                    concat_text += elem_h3.text + '\n'

        except:
            h3 = ''

        # try to find p;
        try:
            p_elements = soup.find_all('p')

            # Concatenate all elements;
            if p_elements:
                for p in p_elements:
                    concat_text += p.text + '\n'

        except:
            p_elements = ''


        return concat_text


    else: 
        return 'We have not acces to this site!!!'

#----------------------------------------------> END of functions <------------------------------------------------


#----------------------------------------------> START Flask <---------------------------------------------------
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.form['place_link'].strip()
        if data.startswith('https://') or data.startswith('http://'):

            # create r instance of class Rake();
            r = Rake()
            r.extract_keywords_from_text(extract_text(data))

            # return data in dict to html;
            data_dict= {}
            for rating, keywords in r.get_ranked_phrases_with_scores():
                if rating > 10:
                    data_dict.update({round(rating, 1): keywords})
                    
            return render_template('result.html', data_dict=data_dict)
        else:
            data_dict = {'0x0': 'Invalid link'}
            return render_template('result.html', data_dict=data_dict)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)