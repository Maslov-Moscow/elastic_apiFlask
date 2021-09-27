from elasticsearch import Elasticsearch
from elasticsearch import helpers

from database import SQLdatabase


def create_index(es: Elasticsearch) -> None:
    """Создание индекс в еластике """
    mapping = {
        "mappings": {
            "properties": {
                "text": {
                    "type": "text"
                },
                "id": {
                    "type": "integer"
                }
            }
        }
    }
    es.indices.create(
        index="post_index",
        body=mapping)
    current_mapping = es.indices.get_mapping("post_index")
    print(current_mapping)
    print('*' * 10, 'Index created', '*' * 10)


def add_data_to_index(db: SQLdatabase, es: Elasticsearch) -> None:
    """Индексирование данных из БД"""

    def gendata(db):
        records = db.get_data()
        for data in records:
            yield {"id": data[0],
                   "text": data[1]}

    helpers.bulk(es, gendata(db), index="post_index")
    print('*' * 10, 'Data inserted to index', '*' * 10)


def search_by_text(text: str) -> tuple:
    es = Elasticsearch(hosts=[{'host': 'elasticsearch', 'port': 9200}])
    query_body = {
        "query": {
            "match": {
                "text": {
                    "query": text
                }
            }
        },
        "collapse": {
            "field": 'id'
        }
    }

    result = es.search(index="post_index", body=query_body, size=20, )
    all_hits = result['hits']['hits']
    list_id = []

    for rec in all_hits:
        list_id.append(rec['_source']['id'])
    return tuple(list_id)


def delete_doc(id_rec: int, es: Elasticsearch) -> None:
    query_body = {"query": {"term": {"id": id_rec}}, "collapse": {"field": 'id'}}
    es_id = es.search(index="post_index", body=query_body)['hits']['hits'][0]['_id']
    es.delete(index="post_index", doc_type='_doc', id=es_id)
