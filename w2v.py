from gensim.models.word2vec import Word2Vec
import sys
import os
import numpy
from time import time
import json
from scipy.spatial.distance import cosine
from flask import Blueprint, jsonify
from regex_converter import *


wvmod = Blueprint('wv', __name__)
model_file = 'data/w2v/w2vsample.bin'
#model_file = 'data/w2v/charles.sgram.5min.bin'
model = Word2Vec.load_word2vec_format(model_file,binary=True,encoding='latin-1')
s = time()
model.init_sims(replace=True)
e = time()
print e - s, "Seconds to load the model"

def get_similars(word):
    try:
        s = model.most_similar(word)
        if len(s) > 0:
            t = []
            for w in s:
                t.append(w[0])
            print t
            return t
    except Exception as e:
        pass

    return 'None'


@wvmod.route("/h/<regex('.*?'):word>/html/")
def hin_similar_html(word):
    #print word
    try:
        word = convert(word.encode('utf-8'))
        words = get_similars(word)
        if type(words) is list:
            s = "<table border='1'>"
            s += "<tr><td>Similar Words of " + convert(word, False) + "</td></tr>"
            s += "<tr><td><div class='wrappable'>"
            t = convert(";".join(words), False).split(';')
            s += "&emsp;".join(t)
            s += "</div></td></tr>"
            s += '</table>'
            return s
    except Exception as e:
        pass

    return 'None'

@wvmod.route("/h/<regex('.*?'):word>/")
def hin_similar(word):
    word = convert(word.decode('utf-8'))
    return json.dumps(get_similars(word))


def convert(word, to = True):
    open('tools/convertor/test','w').write(word)
    if to:
        command = "perl tools/convertor/convertor_indic.pl -f=text -l=hin -s=utf -t=wx -i=tools/convertor/test > tools/convertor/outp"
        os.system(command)
        t =  open('tools/convertor/outp').read()
        print t
        return t
    if to == False:
        command = "perl tools/convertor/convertor_indic.pl -f=text -l=hin -s=wx -t=utf -i=tools/convertor/test > tools/convertor/outp"
        print command
        os.system(command)
        return open('tools/convertor/outp').read()




