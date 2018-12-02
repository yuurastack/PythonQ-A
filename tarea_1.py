#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:09:23 2015

@author: Yuura
"""
from bs4 import BeautifulSoup
from Tkinter import *
import re

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc


import urllib2
import urllib
import json
from urllib2 import HTTPError

palabras = ["fue ","es ","era ","is ","was ","comes ","hails ","queda "," encuentra"] # lista que contiene string para la busqueda con expresiones regulares 
quienEs = ["es ", "is "]
quienEra = ["era ", "was "]
dondeFue = ["queda ", "hails ", "encuentra ", "is located"]
result = range(100)
tam = range(100)            

def BubbleSort2(lst):  #funcion que permite  ordenar las busquedas
    lst = list(lst)  
    swapped = True  
    while swapped:  
        swapped = False  
        for i in range(len(lst)-1):  
            if len(lst[i]) < len(lst[i+1]):  
                lst[i], lst[i+1] = lst[i+1], lst[i]  
                swapped = True  
    return lst 


class _DeHTMLParser(HTMLParser): # clase permite parsear  los html a texto
   
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()
    


def creartxt(clave, count): # permite crear archivo .txt
    archi=open(clave + str(count) + '.txt','w')
    archi.close()

def grabartxt(clave, count, page): #guarda el .txt
    archi=open(str(clave) + str(count) + '.txt','a')
    archi.write(page)
    archi.close()

def dehtml(text): #funcion que realiza el parseo
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        #print_exc(file=stderr)
        return text
def limpia():  #limpia el texto con el boton limpiar
    e.delete(0,END)

def busqueda(): # realiza la busqueda|
    clave = e #toma el texto escrito
    x = 10
    if "quien es " in clave:
        x = 0
        newclave= clave.replace("quien es ","")
        clave = str(newclave) + " es"
    if "who is " in clave:
        x = 0
        newclave= clave.replace("who is ","")
        clave = str(newclave) + " is"
    if "quien fue" in clave:
        x = 1
        newclave= clave.replace("quien fue ","")
        clave = str(newclave) + " fue"
    if "who was" in clave:
        x = 1
        newclave= clave.replace("who was ","")
        clave = str(newclave) + " was"
    if "donde queda " in clave:
        x = 2
        newclave= clave.replace("donde esta ","")
        clave = str(newclave) + " está ubicada"
    if "where is " in clave:
        x = 2
        newclave= clave.replace("where is ","")
        clave = str(newclave) + " is located"
    print x
    # algunos contadores
    n=0
    li=0

    ocurrencia = 1
    
    query = urllib.urlencode({'q'   : "\""+clave+"\"", # aplicamos expresion regular para la busqueda, priorisamos si es que la busqueda tiene el string ubicacion  
                          'v'   : '1.0',      
                          'rsz' : '8',
                          'hl' : 'en',
                          'gl': 'US'})
	
    try:
        url = 'http://ajax.googleapis.com/ajax/services/search/web?%s' \
  % (query) #permite la busqueda
        print url
        resultados = urllib.urlopen(url).read()
        j = json.loads(resultados)
        resultados = j['responseData']['results']
    except:
        print "Error de carga del Json"
    for i in resultados:
        #creartxt(clave, n) #crea textos
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            infile = opener.open(i['url'])
            page = infile.read()
        except HTTPError,k:
            k.code
            k.read()
            
        grabartxt(clave, n, dehtml(page)) #graba el archivo
        
        strArchivo = open(str(clave)+str(n)+'.txt','r')
        
        text = strArchivo.read()
        busqueda = palabras
        if x == 0:
            busqueda = quienEs
        if x == 1:
            busqueda = quienEra
        if x == 2:
            busqueda = dondeFue
        for searchWord in busqueda:                    #buscamos en cada .txt obtenido la expresion regular exp con el metodo re.search que no envia directo al trozo de codigo que contiene esta expresion regular, guardamos el trozo de texto que contiene la expresion regular en result
            exp = "[\(\"]{0,3}" + newclave + "[\)\"\s]{0,3}"+searchWord+"(.{0,200})(\?|\n|\.|\>)"
            exp = re.compile(exp,re.IGNORECASE)
            if re.search(exp,text)!=None:
                    #nu = len(re.findall(exp, text))
                    meme = re.search(exp,text)
                    if re.search('\?',meme.group()) == None:
                        phrase = meme.group()
                        try:
                            #print "--->link" + ": " + i['url'] 
                            print "Ocurrencia #" + str(ocurrencia)
                            print phrase
                            ocurrencia=ocurrencia+1
                        except:
                            print "Error de Codicicacion"
                    rt=re.search(exp,text).group()
                    result[li]=str(rt)
                    li=li+1     
        n=n+1 
    
    b=BubbleSort2(result[0:li])
    b.reverse()
    limitacion=0
    for i in b:
        if limitacion<4:
            #print i
            limitacion=limitacion+1

e = raw_input("Buscador: ")
busqueda()