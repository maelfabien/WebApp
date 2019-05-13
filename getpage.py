#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl
from collections import OrderedDict
import shelve

global cache
cache = dict()

def getJSON(page):
    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'redirects': 'true',  # TODO: compléter ceci
      'prop' : 'text',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))

    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']

        return title, content
    
    except KeyError:
        # La page demandée n'existe pas
        return None, None

# Get all links of an html page
def get_links(html_page) :
    
    soup = BeautifulSoup(html_page, 'html.parser')
    soup = soup.find('div')

    link_get = []
    
    # 2.4
    for link in soup.findAll('p', recursive = False) :
        for l in link.findAll('a') :
            href = l.get('href')

            # 2.5 + 2.6
            if href != None and href[:6] == '/wiki/' :
                link_get.append(href[6:])
    # 2.7
    return link_get[:10]


def correct_txt(s) :
    s = unquote(s)
    s = s.split('#')[0]
    s = s.replace('_', ' ')
    return s

def principal(s) :
    lst = []
    for word in s :
        if ":" in word :
            pass
        else :
            lst.append(word)
    return lst


def randomSearch(page):
    
    init_page = page
    page = correct_txt(page)
    count = 0
    path = []
    
    try :

        while page != 'Philosophie' :

            if page in cache.keys() :
                path.append(page)
                hrefs = cache.get(page)
                page = getRawPage(hrefs)[0]

                count += 1
            
            else :
            
                page = correct_txt(page)
                path.append(page)
                
                hrefs = get_links(getRawPage(page)[1])
                hrefs = [correct_txt(h) for h in hrefs]
                #hrefs = principal(hrefs)
                hrefs = list(OrderedDict.fromkeys(hrefs))[0]

                cache[page] = hrefs
                page = getRawPage(hrefs)[0]
                
                count += 1
        
        path.append("Philosophie")
        
        return count, path

    except :
        
        return None, None


def getPage(page):
    
    # 4.1
    if page in cache.keys() :
        return page, cache[page]

    try :
        
        title = getRawPage(page)[0]
        title = correct_txt(title)
        
        hrefs = get_links(getRawPage(page)[1])
        
        # 4.2 + 4.3
        hrefs = [correct_txt(h) for h in hrefs]
        
        # 4.4
        #hrefs = principal(hrefs)
        
        # 4.3
        hrefs = list(OrderedDict.fromkeys(hrefs))
        if isinstance(hrefs, str) :
            hrefs = [hrefs]
        
        # Add both the title and the redirected title
        cache[title] = hrefs
        cache[page] = hrefs
        
        return title, cache[title]

    except :
        return (None, [])


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    # print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    #print(getJSON("Utilisateur:A3nm/INF344"))
    #print(getPage("Utilisateur:A3nm/INF344"))
    #print(getPage("Utilisateur:A3nm/INF344"))
    #print(getPage("Philosophique"))
    print(randomSearch("Zoologie"))
    #print(getPage("Philosophie"))
