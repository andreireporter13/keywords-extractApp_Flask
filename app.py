# My new (and first) Flask app: SEO_keyword_extract - v1.0;
#
# New scraper idea - scrape keywords from blogs;
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

# Flask dependencies;
from flask import Flask, render_template, request, flash, url_for


app = Flask(__name__)
app.secret_key = "cocolino_linxus_111221"
app.config['SECRET_KEY'] = '$$$MY_SeCreT_KeY**##@##$##$____@#'


#--------------------------------------------> functions for extract text <-------------------------------------------------
def set_headers():

    """ 
    This function is about setting headers for new requests. Is import step to scraping!
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

    response = requests.get(link, headers=set_headers())
    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

        # try find h1;
        try:
            h1 = soup.find('h1').text
        except:
            h1 = ''
        
        # try to find p;
        try:
            p_elements = soup.find_all('p')
        except:
            p_elements = ''
        
        # try to find h2;
        try:
            h2 = soup.find('h2').text
        except:
            h2 = ''

        # try to find h3;
        try:
            h3 = soup.find('h2').text
        except:
            h3 = ''
        
        # Concatenate all elements;
        new_text = ''
        for p in p_elements:
            new_text += p.text + '\n'

        concat_text = h1 + '\n' + h2 + '\n' + h3 + '\n' + new_text

        return concat_text
    
    else: 
        return 'We have not acces to this site!!!'

#----------------------------------------------> END of functions <------------------------------------------------


#----------------------------------------------> START Flask <---------------------------------------------------
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.form['place_link']
        if data.startswith('https://') or data.startswith('http://'):

            # create a Rake() instance;
            new_text = extract_text(data)
            r = Rake()
            r.extract_keywords_from_text(extract_text(data))

            data_dict= {}
            for rating, keywords in r.get_ranked_phrases_with_scores():
                if rating > 10:
                    data_dict.update({rating: keywords})
                    
            return render_template('result.html', data_dict=data_dict)
        else:
            data_dict = {2: 'Invalid link'}
            return render_template('result.html', data_dict=data_dict)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)