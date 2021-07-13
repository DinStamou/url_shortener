from flask import Flask, request, Response, json, redirect, url_for
import hashlib
from dicttoxml import dicttoxml

app = Flask(__name__)
app.secret_key = "super secret key"
url_storage = {}

@app.route('/api/v1/shorten/<path:subpath>', methods=['POST'])

def shorten(subpath):
    url = subpath
    
    if not url.startswith(("http://", "https://")):
      return Response("http:// or https:// needed ", 400)

    hs = hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    url_storage.update({hs[0:10]:url})

    short_url = "https://domain.ltd/" + hs[0:10]
    
    data = {"url" : short_url}

    if request.content_type == 'application/xml':
      xmldata = dicttoxml(data, custom_root='data', attr_type=False)
      return Response(xmldata, mimetype='application/xml')
    
    return Response(json.dumps(data), mimetype='application/json')
    

@app.route('/api/v1/lookup/<identifier>', methods=['GET'])

def lookup(identifier):

    try:
      lookup_key = url_storage[identifier]
      data = {"original_url" : lookup_key}

    except KeyError:
      return Response("No url found!", 400)
    
    if request.content_type == 'application/xml':
      xmldata = dicttoxml(data, custom_root='data', attr_type=False)
      return Response(xmldata, mimetype='application/xml')

    return Response(json.dumps(data), mimetype='application/json')
    

@app.route('/<id>', methods=['GET'])

def original(id):
    
    try:
      original_url = url_storage[id]
      return redirect(original_url)

    except KeyError:
      return Response("No url found!", 400)
