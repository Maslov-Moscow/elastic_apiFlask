import os
import time

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from elasticsearch.exceptions import TransportError
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

from database import SQLdatabase
from services import add_data_to_index
from services import create_index
from services import delete_doc
from services import search_by_text

app = Flask(__name__)
es = Elasticsearch(hosts=[{'host': 'elasticsearch', 'port': 9200}])
db = SQLdatabase()

while True:
    """Ожидание загрузки еластика """
    try:
        es.search(index="")
        break
    except (
            ConnectionError,
            TransportError
    ):
        print('\n', "Waiting elastic", '\n')
        time.sleep(2)

create_index(es=es)
add_data_to_index(db, es)

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
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=80)
