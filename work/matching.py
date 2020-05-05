import os
from elasticsearch import Elasticsearch

url = os.environ.get('ELASTIC_URL', 'http://elastic:9200')
es = Elasticsearch([url])


def find_match(txt, log=False):
    if len(txt) < 5:
        return

    body = {
        "query": {
            "match": {
                "text": {
                    "query": txt,
                    "fuzziness": "auto"
                }
            }
        },
        "min_score": 10
    }

    res = es.search(index="robin", body=body)
    hits = res['hits']['hits']
    if len(hits) == 0:
        return None

    if log:
        # print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in hits:
            print("{resource} {line} ({score}): {text}".format(**hit["_source"], score=hit["_score"]))

    return [{
        'score': hit['_score'],
        'rec': txt,
        **hit["_source"]
    } for hit in hits]

if __name__ == "__main__":
    source = 'Truly a sad and pathetic performance. But I know you are capable of doing far, far better'
    find_match(source)
