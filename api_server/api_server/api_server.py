from elasticsearch import Elasticsearch, ConnectionError, TransportError
from flask import Flask, jsonify
from flask import request
from flask import abort


app = Flask(__name__)
es = Elasticsearch(['localhost'], http_auth=('elastic', 'changeme'), )


@app.route('/ask')
def search():
    question = request.args.get('q')
    if question is None:
        abort(400, "q param must be defined")

    try:
        res = es.search(index="nhs", body={
            "query": {
                "match": {
                    "main_content": question
                }
            }
        })
    except ConnectionError as e:
        abort(500, "Could not connect to elasticsearch")
    except TransportError as e:
        abort(e.status_code, e.info)
    except:
        abort(500)

    json_response = []

    for hit in res['hits']['hits']:
        json_response.append({
            'title': hit['_source']['title'],
            'url': hit['_source']['url'],
            'main_content': hit['_source']['main_content'],
            'relevance_score': hit['_score']
        })

    return jsonify(json_response)


if __name__ == "__main__":
    app.run()