from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# API para devolver los artículos más populares.  
@app.route("/popular-articles")
def popular_articles():
    articulos_populares=[]
    for x,y in output.iterrows():
        data = {
        "original_title": y['title'],
        "poster_link": y['url'],
        "text": y['text'] or "N/A",
        "lang": y['lang'],
        "total_events":y['total_events']/2
        }
        articulos_populares.append(data)
    return jsonify({
        "data":articulos_populares,
        "status":"success"
    })

# API para devolver los 10 artículos más similares usando el método content based filtering.

@app.route("/recommended-articles")
def recommended_articles():
    global liked_articles
    colums_names = ['url' , 'title' , 'text' , 'lang' , 'total_events']
    all_columns=pd.DataFrame(columns=colums_names)
    for x in liked_articles:
        recomen=get_recommendations(x["title"])
        all_columns=all_columns.append(recomen)
    all_columns.drop_duplicates(subset=["title"],inplace=True)
    arcticulos_populares=[]
    for x,y in all_columns.iterrows():
        data = {
        "original_title": y['title'],
        "poster_link": y['url'],
        "text": y['text'] or "N/A",
        "lang": y['lang'],
        "total_events":y['total_events']/2
        }
        arcticulos_populares.append(data)
    return jsonify({
        "data":arcticulos_populares,
        "status":"success"
    })

if __name__ == "__main__":
    app.run()
