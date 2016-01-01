#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import json

word = "गढ़ना"

os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-7-openjdk-amd64/'
os.environ['CLASSPATH'] = './JHWNL.jar'

from jnius import autoclass

JHWNL = autoclass('in.ac.iitb.cfilt.jhwnl.JHWNL')
Dictionary = autoclass('in.ac.iitb.cfilt.jhwnl.dictionary.Dictionary')
IndexWord = autoclass('in.ac.iitb.cfilt.jhwnl.data.IndexWord')

JHWNL.initialize('./config/HindiWN2.properties')

demoIWSet = Dictionary.getInstance().lookupAllIndexWords(word.strip())
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

print json.dumps(data, indent = 2)