# from elasticsearch import Elasticsearch, helpers
# from datetime import datetime
# import csv
#
# es = Elasticsearch()
#
# # with open('posts.csv', encoding="utf8") as f:
# #     reader = csv.DictReader(f)
# #     helpers.bulk(es, reader, index='my-index',)
#
# looking = input()
# query_body = {
#   "query": {
#     "bool": {
#       "must": {
#         "match": {
#           "text": looking
#         }
#       }
#     }
#   }
# }
# result = es.search(index="my-index", body=query_body, size=20)
# all_hits =result['hits']['hits']
# for doc in all_hits:
#     print(doc['_source'])
import os
from pathlib import Path

from elasticsearch import Elasticsearch
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from elasticsearch.exceptions import ConnectionError, TransportError
from database import SQLdatabase
from services import add_data_to_index
from services import create_index
from services import delete_doc
from services import search_by_text
import time
state =0

app = Flask(__name__)
# state += 1
# print('\n'*3,state)
#
# state += 1
es = Elasticsearch(hosts=[{'host':'elasticsearch','port':9200}])
# state += 1
# print('\n'*3,state)
#
db = SQLdatabase()
# state += 1
# print('\n'*3,state)
#

while True:
    try:
        es.search(index="")
        break
    except (
        ConnectionError,
        TransportError
    ):
        print('\n',"error connection",'\n')
        time.sleep(1)
#
create_index(es=es)
# state += 1
# print('\n'*3,state)
#
add_data_to_index(db, es)
# state += 1
# print('\n'*3,state)







SWAGGER_URL = '/swagger'
API_URL = '/swag/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-Flask-REST"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)




@app.route("/swag/swagger.yaml")
def specs():
    return send_from_directory(os.getcwd(), "swagger.yaml")


@app.route('/', methods=['POST'])
def get_record():
    try:
        db = SQLdatabase()
        text = request.form.get('text')
        response = db.get_records(search_by_text(text))
    except Exception as e:
        return {'error': str(e)}, 500
    return jsonify(response)


@app.route('/delete/<int:id_rec>', methods=['DELETE'])
def delete_record(id_rec):
    db = SQLdatabase()
    try:
        db.delete_record(id_rec)
        delete_doc(id_rec, es)
        return {'succes': True}
    except IndexError:
        return {'error': 'record not found'}, 404


if __name__ == '__main__':
    # es = Elasticsearch()
    # test['elstic'] = True
    #
    # db = SQLdatabase()
    # test['sql'] = True
    # create_index(es=es)
    # test['elstic create'] = True
    # add_data_to_index(db, es)
    # test['sql to elstic'] = True
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=80)
