import json

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, errors
import re
from datetime import datetime
from bson.json_util import dumps
from pymongo.errors import PyMongoError

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['Spotify']

# Pagina principale

# Definisci la mappatura degli attributi per ogni collezione
collection_attributes = {
    'artist': ['_id', 'artists', 'popularity'],
    'generes': ['_id', 'genres', 'popularity'],
    'song': ['_id', 'name', 'popularity']
}

@app.route('/')
def index():
    return render_template('index2.html')

# Elenco dei documenti per una collezione
@app.route('/collection/<collection_name>', methods=['GET'])
def get_collection(collection_name):
    collection = db[collection_name]

    if collection is None:
        return jsonify({'error': 'Invalid collection name'}), 404

    attributes = collection_attributes.get(collection_name)

    if attributes is None:
        return jsonify({'error': 'Attributes not defined for collection'}), 400

    items = list(collection.find({}, {attr: 1 for attr in attributes}).limit(25))

    # Converte l'oggetto ObjectId in stringa
    for item in items:
        item['_id'] = str(item['_id'])

    return jsonify(items)

from bson import json_util

from bson import json_util

from bson import json_util

@app.route('/collection/<collection_name>/search')
def search_collection(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid collection name'}), 404

    attributes = request.args.getlist('attributes')
    if not attributes:
        return jsonify({'error': 'Attributes not defined for collection'}), 400

    search_query = request.args.get('query')
    if not search_query:
        return jsonify({'error': 'Query not defined'}), 400

    try:
        collection = db[collection_name]
        query = {'$or': []}
        for attr in attributes:
            if search_query.isdigit():
                query['$or'].append({attr: {'$gt': float(search_query)}})
            else:
                regex_pattern = re.compile(re.escape(search_query), re.IGNORECASE)
                query['$or'].append({attr: {'$regex': regex_pattern}})

        if len(query['$or']) == 0:
            return jsonify({'error': 'Empty $or array in query'}), 400

        projection = {attr: 1 for attr in attributes}
        projection['_id'] = 1  # Aggiungi il campo _id alla proiezione
        items = list(collection.find(query, projection).limit(25))

        results = []
        for item in items:
            item['_id'] = str(item['_id'])  # Converte l'oggetto ObjectId in stringa
            results.append(item)

        return jsonify(results)  # Utilizza dumps() per serializzare in JSON




    except errors.PyMongoError as e:
        return jsonify({'error': str(e)}), 500




@app.route('/collection/<collection_name>/<document_id>/attributes')
def get_document_attributes(collection_name, document_id):

    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid collection name'}), 404

    collection = db[collection_name]
    document = collection.find_one({"_id": ObjectId(document_id)})
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    attributes = {key: value for key, value in document.items() if key != '_id'}
    return jsonify(attributes)

@app.route('/collection/<collection_name>/attributes')
def get_collection_attributes(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid collection name'}), 404

    collection = db[collection_name]
    attributes = collection.find_one()  # Assuming all documents have the same attributes
    if not attributes:
        return jsonify({'error': 'No attributes found'}), 500

    attribute_names = list(attributes.keys())
    attribute_names.remove('_id')  # Exclude the _id attribute
    return jsonify(attribute_names)

@app.route('/collection/<collection_name>/insert', methods=['POST'])
def insert_document(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid collection name'}), 404

    try:
        collection = db[collection_name]
        data = request.get_json()
        attributes = data.get('attributes')
        document = {}

        for attr in attributes:
            attribute = attr['attribute']
            value = attr['value']

            # Verifica se il valore è numerico e converte in float o int
            if isinstance(value, (int, float)):
                document[attribute] = value
            else:
                try:
                    document[attribute] = int(value)
                except ValueError:
                    try:
                        document[attribute] = float(value)
                    except ValueError:
                        document[attribute] = value

        result = collection.insert_one(document)
        # Invia una risposta con un messaggio di conferma
        response = {'inserted_id': str(result.inserted_id), 'message': 'Elemento inserito correttamente'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/collection/<collection_name>/<document_id>/remove', methods=['POST'])
def delete_document(collection_name, document_id):
    collection = db[collection_name]
    document_id = ObjectId(document_id)  # Converti il document_id in ObjectId
    collection.delete_one({'_id': document_id})
    return jsonify('Element deleted successfully')

@app.route('/collection/<collection_name>/remove/<attribute>', methods=['DELETE'])
def remove_attribute(collection_name, attribute):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid collection name'}), 404

    try:
        collection = db[collection_name]
        collection.update_many({}, {'$unset': {attribute: 1}})
        return jsonify({'message': 'Attribute removed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/collection/<collection_name>/<document_id>/edit', methods=['POST'])
def edit_document(collection_name, document_id):
    document_id = ObjectId(document_id)
    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid collection name'}), 404

    collection = db[collection_name]
    document = collection.find_one({'_id': document_id})
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    data = request.get_json()
    attributes = data.get('attributes')

    for attribute, value in attributes.items():
        document[attribute] = value

    collection.replace_one({'_id': document_id}, document)
    return jsonify({'message': 'Document updated successfully'})











# Dettaglio di un documento per una collezione
@app.route('/collection/<collection_name>/<document_id>', methods=['GET'])
def get_document(collection_name, document_id):
    collection = db[collection_name]
    document = collection.find_one({'_id': document_id})
    return jsonify(document)



'''
@app.route('/collection/<collection_name>/<document_id>/remove_attribute', methods=['POST'])
def remove_attribute(collection_name, document_id):
    collection = db[collection_name]
    data = request.json
    attribute_name = data.get('attribute_name')
    collection.update_one({'_id': document_id}, {'$unset': {attribute_name: 1}})
    return jsonify('Attribute removed successfully')
'''

@app.route('/query1')
def pagina():
    return render_template('query1.html')

@app.route('/collection/<collection_name>/<parameter>/top/10', methods=['GET'])
def get_top_parameter(collection_name, parameter):
    collection = db[collection_name]

    if collection is None:
        return jsonify({'error': 'Invalid collection name'}), 404

    # Verifica che il parametro selezionato sia valido
    valid_parameters = ['danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity']
    if parameter not in valid_parameters:
        return jsonify({'error': 'Invalid parameter'}), 400

    # Ottieni i primi 10 documenti ordinati per il parametro selezionato in ordine decrescente
    items = list(collection.find().sort(parameter, -1).limit(10))

    # Converte l'oggetto ObjectId in stringa
    for item in items:
        item['_id'] = str(item['_id'])

    return jsonify(items)

    return jsonify(items)
@app.route('/query2')
def pagina2():
    return render_template('query2.html')

# Funzione per eseguire la query
# Trova tutti gli artisti che hanno pubblicato canzoni con una danceability superiore a 0.6 e un'energia superiore a 0.8:
def findArtistsWithConditions():
    songCollection = db['song']
    artistCollection = db['artist']

    songQuery = {"danceability": {"$gt": 0.6}, "energy": {"$gt": 0.8}}
    artistIds = songCollection.distinct("artists", songQuery)
    artistQuery = {"_id": {"$in": artistIds}}
    artists = list(artistCollection.find(artistQuery))

    # Converte l'oggetto ObjectId in stringa
    for artist in artists:
        artist['_id'] = str(artist['_id'])

    return artists

@app.route('/artists')
def get_artists():
    try:
        artists = findArtistsWithConditions()
        return jsonify(artists)
    except errors.PyMongoError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query3')
def pagina3():
    return render_template('query3.html')

from bson import ObjectId

from bson import json_util

@app.route('/popular-songs')
def popular_songs():
    year = request.args.get('year')

    try:
        # Converti l'anno in un intero
        year = int(year)

        # Esegui la query per ottenere le canzoni popolari per l'anno specificato
        songs = db.song.find({'year': year}).sort('popularity', -1).limit(10)

        results = []
        for song in songs:
            # Converte l'oggetto ObjectId in una rappresentazione JSON
            song['_id'] = str(song['_id'])
            results.append(song)

        return jsonify({'songs': results})

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid year'}), 400

    except errors.PyMongoError as e:
        return jsonify({'error': str(e)}), 500





if __name__ == '__main__':
    app.run()
