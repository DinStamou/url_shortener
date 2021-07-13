from flask import Flask, request, Response, json, redirect, url_for
import hashlib
from dicttoxml import dicttoxml

# Initialization of Flask application, you can add here a secret key
app = Flask(__name__)
app.secret_key = "super secret key"

# Dictionary initialization
url_storage = {}

# Shorten endpoint
@app.route('/api/v1/shorten/<path:subpath>', methods=['POST'])

def shorten(subpath):
    url = subpath
    
    # Check if the URL starts with https or http
    if not url.startswith(("http://", "https://")):
      return Response("http:// or https:// needed ", 400)
    
    # Hash the URL with SHA256
    hs = hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    # Store it to the dictionary
    url_storage.update({hs[0:10]:url})

    # Create the shortened URL
    short_url = "https://domain.ltd/" + hs[0:10]
    
    # Create the data to be sent as response
    data = {"url" : short_url}
    
    # Return the XML Response if needed
    if request.content_type == 'application/xml':
      xmldata = dicttoxml(data, custom_root='data', attr_type=False)
      return Response(xmldata, mimetype='application/xml')
    
    # Standard JSON response
    return Response(json.dumps(data), mimetype='application/json')
    
# Lookup endpoint creation
@app.route('/api/v1/lookup/<identifier>', methods=['GET'])

def lookup(identifier):

    # Lookup of the key to the dictionary
    try:
      lookup_key = url_storage[identifier]
      data = {"original_url" : lookup_key}

    except KeyError:
      return Response("No url found!", 400)
    
    # XML Response if needed
    if request.content_type == 'application/xml':
      xmldata = dicttoxml(data, custom_root='data', attr_type=False)
      return Response(xmldata, mimetype='application/xml')
    
    # Standard JSON response
    return Response(json.dumps(data), mimetype='application/json')
    
# Redirect endpoint
@app.route('/<id>', methods=['GET'])

def original(id):
    
    try:
      original_url = url_storage[id]
      return redirect(original_url)

    except KeyError:
      return Response("No url found!", 400)
