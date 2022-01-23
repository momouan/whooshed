import json
from flask import Flask, render_template, redirect, url_for, request, Response
import spacy
import numpy
import requests
from bs4 import BeautifulSoup as bs
import requests
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

#fonction qui retourne les mots similaires d'un mot
def getSimilarity(mot):
    nlp = spacy.load("en_core_web_lg")
    ms = nlp.vocab.vectors.most_similar(numpy.asarray([nlp.vocab.vectors[nlp.vocab.strings[mot]]]), n=30)
    liste=[nlp.vocab.strings[w].lower() for w in ms[0][0]]    
    return set(liste)

def liste_to_keywords(liste):
    res =" OR ".join(str(x) for x in liste)      
    return res

def create_corpus():
    with open('data.json') as json_file:
        data = json.load(json_file)
    schema = Schema(ty=TEXT(stored=True), arURL=TEXT(stored=True), entity=TEXT(stored=True))
    ix = create_in("indexdir7", schema)
    writer = ix.writer()
    for i in data:
        writer.add_document(ty=u""+str(data[i][1]), arURL=u""+str(data[i][2]),entity=u""+str(data[i][0]))
    writer.commit()
    return ix

def search_corpus(mots,ty,ix):
    link_result=[]
    with ix.searcher() as searcher:
        query = QueryParser("entity", ix.schema).parse(mots)
        results = searcher.search(query)
        for i in results:
            if ty=="All":
                if i['arURL'] not in link_result:
                    link_result.append(i['arURL'])
            else:
                if i['ty']==ty:
                    if i['arURL'] not in link_result:
                        link_result.append(i['arURL'])

    return link_result



#liste=getSimilarity("paris")
#mots=liste_to_keywords(liste)
#ix=create_corpus()
#r=search(mots,ix)
#print(r)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "GET":
        q = request.args.get("q")
        t = request.args.get("type")
        liste_mots=getSimilarity(q)
        mots=liste_to_keywords(liste_mots)
        print(mots)
        r=search_corpus(mots,t,ix)
        return render_template("res.html",res=r)


if __name__ == "__main__":
    ix=create_corpus()
    app.run(debug=True)
    