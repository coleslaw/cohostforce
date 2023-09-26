from django.core.management.base import BaseCommand
from online_site.models import Profile, ContestResult
from online_site.documents import ProfileDocument, ContestResultDocument
from elasticsearch_dsl import Document, Integer, Text, Object
import glob
import pandas as pd
import os
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch


def get_file_name(file_path):
    cur_file = os.path.basename(file_path)
    username = os.path.splitext(cur_file)[0]
    return username


def add_profiles(all_files):
    index_name = 'list_substring_v2_faster_add'
    es = Elasticsearch(
        ['https://daa681.es.us-east-1.aws.found.io'],  # thay đổi địa chỉ URL kết nối đến Elasticsearch
        http_auth=('elastic', 'xhBqmy8XqOYQSZYjspBVsnPK'),  # thêm thông tin đăng nhập
        scheme="https",
    )
    es.indices.create(index=index_name, ignore=400)
    mp = {}
    for file_path in all_files:
        name = get_file_name(file_path)
        s = name.lower()
        n = len(s)

        for length in range(1, n + 1):
            vt = []
            for i in range(n - length + 1):
                if s[i:i + length].isalnum():
                    vt.append(s[i:i + length])
            vt = sorted(list(set(vt)))
            for keyname in vt:
                if keyname not in mp:
                    mp[keyname] = []
                mp[keyname].append(name)
    print(len(mp))
    for key,value in mp.items():
        new_doc = {
            "keyname": key,
            "list_name": value
        }
        response = es.index(index=index_name, document=new_doc)
        if response['result'] == 'created':
            print(f"Created new document have of {key}")
        else:
            print("Failed to create document.")
# 10h40 -> ?
# {
# "keyname" : something,
# "list_name": [something,something1,...,somethingn]
# }
# ngoài ra có 1 dạng truy vấn như sau
# truy vấn có dạng 2 string keyname và name

class Command(BaseCommand):
    help = 'Load csv files into models'

    def add_arguments(self, parser):
        parser.add_argument('csv_dir', help="Directory containing CSV files")

    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        all_files = glob.glob(csv_dir + '/*.csv')
        add_profiles(all_files)
