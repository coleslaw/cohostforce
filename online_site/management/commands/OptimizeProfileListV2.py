from django.core.management.base import BaseCommand
from online_site.models import Profile, ContestResult
from online_site.documents import ProfileDocument, ContestResultDocument
from elasticsearch_dsl import Document, Integer, Text, Object
import glob
import pandas as pd
import os
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch

import threading

# Khóa để đồng bộ hóa truy cập vào tài nguyên chung
lock = threading.Lock()
def get_file_name(file_path):
    cur_file = os.path.basename(file_path)
    username = os.path.splitext(cur_file)[0]
    return username
def process_file(file_path, es):
    name = get_file_name(file_path)
    index_name = 'list_substring_v2'
    s = name.lower()
    n = len(s)
    for length in range(1, n + 1):
        vt = []
        for i in range(n - length + 1):
            if s[i:i + length].isalnum():
                vt.append(s[i:i + length])
        vt = sorted(list(set(vt)))
        for keyname in vt:
            query = {
                "query": {
                    "term": {
                        "keyname": keyname
                    }
                },
                "_source": False,
                "size": 10000
            }

            with lock:
                result = es.search(index=index_name, body=query)
                ids = [hit['_id'] for hit in result['hits']['hits']]

                if len(ids) > 0:
                    assert len(ids) == 1, f"co nhieu {keyname} trong index"
                    update_query = {
                        "script": {
                            "source": "ctx._source.list_name.add(params['name'])",
                            "params": {
                                "name": name
                            }
                        }
                    }
                    es.update(index=index_name, id=ids[0], body=update_query)
                    print(f"Updated list_name for keyname {keyname}")

                else:
                    new_doc = {
                        "keyname": keyname,
                        "list_name": [name]
                    }
                    response = es.index(index=index_name, document=new_doc)
                    if response['result'] == 'created':
                        print(f"Created new document have {keyname} of {name}")
                    else:
                        print("Failed to create document.")

def add_profiles(all_files):
    index_name = 'list_substring_v2'
    es = Elasticsearch(
        ['https://daa681.es.us-east-1.aws.found.io'],
        http_auth=('elastic', 'xhBqmy8XqOYQSZYjspBVsnPK'),
        scheme="https",
    )
    es.indices.create(index=index_name, ignore=400)

    threads = []
    for file_path in all_files:
        thread = threading.Thread(target=process_file, args=(file_path,es))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

class Command(BaseCommand):
    help = 'Load csv files into models'

    def add_arguments(self, parser):
        parser.add_argument('csv_dir', help="Directory containing CSV files")

    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        all_files = glob.glob(csv_dir + '/*.csv')
        add_profiles(all_files)
