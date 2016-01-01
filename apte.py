from flask import Blueprint, jsonify
from regex_converter import *
import marisa_trie

apmod = Blueprint('apte', __name__)
#pbmod.url_map.converters['regex'] = RegexConverter

at = marisa_trie.Trie().mmap('data/apte/all.trie')


def access(word):
  word = word.strip().encode('utf-8')
  intm = at.keys(word.decode('utf-8')+'%%')

  if len(intm) > 0:
    # print intm
    intm = intm[0].split('%%')
    t = {'word':word}
    t['pratipadik'] = intm[1]
    t['grammar'] = intm[2]
    t['senses'] = intm[3].split('&$&')
    return t
  return 'None'


@apmod.route("/<regex('.*?'):word>/")
def apte_json(word):
  "Returns results from Apte Sanskrit-Hindi Dictionary"
  return jsonify(access(word))

@apmod.route("/<regex('.*?'):word>/html/")
def apte_html(word):
  "Returns results from Apte Sanskrit-Hindi Dictionary in HTML"
  data = access(word)
  if data != 'None':
    s = "<table border=1 style='text-align:center'>"
    s += "<tr><td>Word : "+word+"</td>"
    s += "<td>Pratipadik : "+data['pratipadik']+"</td>"
    s += "<td>Grammar : "+data['grammar']+"</td></tr>"
    s += "<tr><td colspan='3'>Senses</td></tr>"
    for index, sense in enumerate(data['senses']):
      s += "<tr><td colspan='3'>"+str(index+1)+" : "+sense+"</td></tr>"
    s += "</table>"
    return s
  return data
