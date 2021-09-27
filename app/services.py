from elasticsearch import Elasticsearch
from elasticsearch import helpers

from database import SQLdatabase


# es = Elasticsearch()


# db = SQLdatabase()


#  СОЗДАНИЕ ИНДЕКСА
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


# mapping = {'some_new_index': {'mappings': {
#     'properties': {'created_date': {'type': 'date'},
#                    'rubrics': {'type': 'text'},
#                    'text': {'type': 'text'}}}}}

# ДОБАВЛЕНИЕ ЗАПИСИ
# data = {'text':'text','id':1}
# res = es.index(index='post_index', doc_type="_doc", id=1, body=data)

# print(res['result'])

def add_data_to_index(db: SQLdatabase, es: Elasticsearch) -> None:
    """Индексирование данных из БД"""

    def gendata(db):
        records = db.get_data()
        for data in records:
            yield {"id": data[0],
                   "text": data[1]}
    helpers.bulk(es, gendata(db), index="post_index")
    print('*' * 10, 'Data inserted to index', '*' * 10)


# gendata()


# with open('posts.csv', encoding="utf8") as f:
#     reader = csv.DictReader(f)
#     helpers.bulk(es, reader, index='some_new_index',)
def search_by_text(text) -> tuple:
    es = Elasticsearch(hosts=[{'host':'elasticsearch','port':9200}])

    # {

    #         "bool": {
    #             "must": {
    #                 "match": {
    #                     "text": text
    #                 }
    #             }
    #         }
    #     }
    # }
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
    # print(all_hits[0])
    list_id = []

    for rec in all_hits:
        # print(rec['_score'])
        list_id.append(rec['_source']['id'])
    # print(list_id)
    return tuple(list_id)


def delete_doc(id_rec: int, es: Elasticsearch):
    query_body = {"query": {"term": {"id": id_rec}}, "collapse": {"field": 'id'}}
    es_id = es.search(index="post_index", body=query_body)['hits']['hits'][0]['_id']
    es.delete(index="post_index", doc_type='_doc', id=es_id)

# search_by_text('здоровье')
# for doc in all_hits:
#     result.append(doc['_source'])
# result.sort(key=lambda x: datetime.strptime(x['created_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
# return result
