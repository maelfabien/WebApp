#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage
from getpage import randomSearch
import pandas as pd

app = Flask(__name__)

app.secret_key = b'(\xee\x00\xd4\xce"\xcf\xe8@\r\xde\xfc\xbdJ\x08W'

global table_content
df = pd.read_csv('score.txt', sep=",", header=None)
df.columns = (["Page", "Score", "Auto"])

global val

@app.route('/histo', methods=("POST", "GET"))
def html_table():
    
    return render_template('histo.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/newgame', methods=['GET', 'POST'])
def newgame() :
    #if request.method == 'POST':
    session['score'] = 0
    
    if 'start_auto' in request.form :
        session['article'] = request.form['start']
        return redirect('/autogame')
    else :
        session['article'] = request.form['start']
        return redirect('/game')

@app.route('/game', methods=['GET'])
def game() :
    session['title'], session['hrefs'] = getPage(session['article'])
    
    if session['title'] == 'Philosophie' :
        with open("score.txt", "a") as d:
            d.write(str(str(session['article']) + ',' + str(session['score']) + ',' + 'False')+'\n')
            d.close()
            
        flash("C'est gagné! Votre score est de : " + str(session['score']), "Won")
        return redirect('/')
        
    if session['title'] == None :
        flash("Perdu... La page demandée n'existe pas.", "Lost")
        return redirect('/')

    if session['hrefs'] == [] :
        flash("Perdu... La page demandée n'a pas de liens.", "Lost")
        return redirect('/')
        
    else :
        session['score'] += 1
        return render_template('game.html', title=session['title'], hrefs=session['hrefs'] )

@app.route('/autogame', methods=['GET'])
def autogame() :
    
    session['score_auto'], session['path_auto'] = randomSearch(session['article'])
    if session['score_auto'] == None :
        flash("Perdu... La page demandée n'existe pas", "Lost")
    else :
        flash("La page a été trouvée en : " + str(session['score_auto']) + " étapes.", "Won")
        flash("La chemin trouvé est : " + ', '.join([str(s) for s in (session['path_auto'])]), "Won")
    
    with open("score.txt", "a") as d:
        d.write(str(str(session['article']) + ',' + str(session['score_auto']) + ',' + 'True')+'\n')
        d.close()

    return redirect('/')


@app.route('/move', methods=['POST'])
def move() :
    if request.form['destination'] in session['hrefs'] :
        session['article'] = request.form['destination']
        return redirect('/game')
    else :
        flash("Vous jouez sur plusieurs onglets.", "Lost")
        return redirect('/')


@app.route('/tuto')
def tuto():
    return render_template('tuto.html')

# Si vous définissez de nouvelles routes, faites-le ici

if __name__ == '__main__':
    app.run(debug=True)
