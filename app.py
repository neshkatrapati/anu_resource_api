from flask import Flask, jsonify, send_from_directory, render_template, request, redirect
from regex_converter import *
import os, json
import random
import re



app = Flask(__name__)
#AutoIndex(app, browse_root=os.path.curdir)
#ext = Sitemap(app=app)
# Add this to enable regex parsing of the url.
app.url_map.converters['regex'] = RegexConverter




@app.route('/', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

from punj_bilingual import pbmod
from w2v import wvmod
from hindi_wordnet import hwmod
from apte import apmod

app.register_blueprint(pbmod, url_prefix='/pb')
app.register_blueprint(wvmod, url_prefix='/wv')
app.register_blueprint(hwmod, url_prefix='/hw')
app.register_blueprint(apmod, url_prefix='/ap')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug = True)
