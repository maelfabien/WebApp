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
    
    if session['title'] == 'Philosophy' :
        with open("score.txt", "a") as d:
            d.write(str(str(session['article']) + ',' + str(session['score']) + ',' + 'False')+'\n')
            d.close()
            
        flash("You won ! Your score is : " + str(session['score']), "Won")
        return redirect('/')
        
    if session['title'] == None :
        flash("The desired page " + session['article'] + " does not exist.", "Lost")
        return redirect('/')

    if session['hrefs'] == [] :
        flash("The desired page has no hyper-links.", "Lost")
        return redirect('/')
        
    else :
        session['score'] += 1
        session['article'] = session['title']
        return render_template('game.html', title=session['article'], hrefs=session['hrefs'] )

@app.route('/autogame', methods=['GET'])
def autogame() :
    
    session['score_auto'], session['path_auto'] = randomSearch(session['article'])
    if session['score_auto'] == None :
        flash("The desired page " + session['article'] + " does not exist.", "Lost")
    elif session['score_auto'] > 75 :
        flash("Page not found in 75 steps.", "Lost")
    else :
        flash("The desired page was found in : " + str(session['score_auto']) + " steps.", "Won")
        flash("The chosen path is : " + ', '.join([str(s) for s in (session['path_auto'])]), "Won")
    
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
        flash("You have several tabs opened.", "Lost")
        return redirect('/')


@app.route('/tuto')
def tuto():
    return render_template('tuto.html')

# Si vous définissez de nouvelles routes, faites-le ici

if __name__ == '__main__':
    app.run(debug=True)
