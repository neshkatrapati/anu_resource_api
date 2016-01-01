from flask import Blueprint, jsonify
from regex_converter import *
import marisa_trie

pbmod = Blueprint('pun_bilingual', __name__)
#pbmod.url_map.converters['regex'] = RegexConverter

hf = marisa_trie.Trie().mmap('data/punjabi_bilingual/hin.forward.trie')
hb = marisa_trie.Trie().mmap('data/punjabi_bilingual/hin.backward.trie')
pf = marisa_trie.Trie().mmap('data/punjabi_bilingual/pan.forward.trie')
pb = marisa_trie.Trie().mmap('data/punjabi_bilingual/pan.backward.trie')

@pbmod.route('/')
def home():
    return 'Punjabi-Hindi Bilingual Dictionary'




def access_dict(i, o, word):
  word = word.encode('utf-8')
  intm = i.keys(word.decode('utf-8')+'%%')

  if len(intm) > 0:
    intm = intm[0].split('%%')[-1]
    hintm = o.keys(intm+'%%')
    if len(hintm) > 0:
        hintm = hintm[0].split('%%')
        t = {
            "synset" : hintm[-1],
            "id":hintm[0],
            "cat":hintm[1],
            "example":hintm[2]
          }
        return t
  return 'None'

def h(word):
  return access_dict(hb, hf, word)

def p(word):
  return access_dict(pb, pf, word)

def p2h(word):
  return access_dict(pb, hf, word)

def h2p(word):
  return access_dict(hb, pf, word)

@pbmod.route("/p2h/<regex('.*?'):word>")
def pun_to_hin(word):
  "Return hindi word given punjabi word"
  return jsonify(p2h(word))

@pbmod.route("/h/<regex('.*?'):word>")
def hin_mon(word):
  "Return hindi synsets"
  return jsonify(h(word))

@pbmod.route("/p/<regex('.*?'):word>")
def pun_mon(word):
  "Return hindi synsets"
  return jsonify(p(word))


@pbmod.route("/h2p/<regex('.*?'):word>")
def hin_to_pun(word):
  "Return hindi word given punjabi word"
  return jsonify(h2p(word))



def layer_html(f, word):
  p = f(word)
  if p == 'None':
    print word
    return p
  s = "<table border='1'>"
  for key, value in p.items():
    if key == 'id':
      continue
    s += "<tr>"
    s += "<td>"+key.capitalize()+"</td>"
    s += "<td><div class='wrappable'>"+value+"</div></td>"
    s += "</tr>"
  s += '</table>'
  return s



@pbmod.route("/p2h/<regex('.*?'):word>/html")
def pun_to_hin_html(word):
  "Return hindi word given punjabi word in html"
  return layer_html(p2h, word)


@pbmod.route("/h2p/<regex('.*?'):word>/html")
def hin_to_pun_html(word):
  "Return hindi word given punjabi word in html"
  return layer_html(h2p, word)

@pbmod.route("/h/<regex('.*?'):word>/html")
def hin_mon_html(word):
  "Return hindi synsets in html"
  return layer_html(h, word)

@pbmod.route("/p/<regex('.*?'):word>/html")
def pun_mon_html(word):
  "Return punjabi synsets in html"
  return layer_html(p, word)