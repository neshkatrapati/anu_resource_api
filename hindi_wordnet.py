#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import json
from flask import Blueprint, jsonify
from regex_converter import *

hwmod = Blueprint('hw', __name__)

os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-7-openjdk-amd64/'
os.environ['CLASSPATH'] = './data/hindi_wordnet/JHWNL_1_2/JHWNL.jar'

from jnius import autoclass


JHWNL = autoclass('in.ac.iitb.cfilt.jhwnl.JHWNL')
Dictionary = autoclass('in.ac.iitb.cfilt.jhwnl.dictionary.Dictionary')
IndexWord = autoclass('in.ac.iitb.cfilt.jhwnl.data.IndexWord')

JHWNL.initialize('./data/hindi_wordnet/JHWNL_1_2/config/HindiWN.properties')


def lookup(word):

    word = word.encode('utf-8')
#    word = "गढ़ना"
    demoIWSet = Dictionary.getInstance().lookupAllIndexWords(word)
    demoIndexWord = demoIWSet.getIndexWordArray()

    data = {}
    data['source'] = word.strip()
    data['size'] = 0
    sense_number = 0
    for diw in demoIndexWord:
        size = diw.getSenseCount();
        data['size'] += size
        synsetOffsets = diw.getSynsetOffsets();
        synsetArray = diw.getSenses();
        for synset in synsetArray:
          syn = [w.toString() for w in synset.getWords()]
          data[sense_number] = {'synset' : syn, 'pos' : synset.getPOS().toString()}
          sense_number += 1

    return data

@hwmod.route("/<regex('.*?'):word>/")
def hw_lookup(word):
  "Returns synset given a word from wordnet"
  return jsonify(lookup(word))


@hwmod.route("/<regex('.*?'):word>/html")
def hw_lookup_html(word):
  "Returns synset given a word from wordnet in html"
  data = lookup(word)
  s = "<table border='1'>"
  s += "<tr><td colspan=3>Word :: "+data['source']+"</td></tr>"
  s += "<tr><td>ID</td><td>CAT</td><td>SYNSET</td></tr>"
  for key, value in data.items():
    if key not in ['source', 'size']:
      s += "<tr>"
      s += "<td><div class='wrappable'>"+str(key + 1)+"</div</td>"
      s += "<td><div class='wrappable'>"+value['pos']+"</div></td>"
      s += "<td><div class='wrappable'>"+",".join(value['synset'])+"</div></td>"
      s += "</tr>"
  s += "</table>"
  return s
