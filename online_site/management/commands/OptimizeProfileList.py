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
    index_name = 'list_substring'
    es = Elasticsearch(
        ['https://daa681.es.us-east-1.aws.found.io'],  # thay đổi địa chỉ URL kết nối đến Elasticsearch
        http_auth=('elastic', 'xhBqmy8XqOYQSZYjspBVsnPK'),  # thêm thông tin đăng nhập
        scheme="https",
    )
    es.indices.create(index=index_name, ignore=400)
    cnt = 0
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
                query = {
                    "query": {
                        "term": {
                            "keyname": keyname
                        }
                    },
                    "_source": False,  # Chỉ trả về các ID, không trả về nội dung tài liệu
                    "size": 10000  # Số lượng tài liệu tối đa để trả về
                }

                # Thực hiện truy vấn
                result = es.search(index=index_name, body=query)

                # Lấy danh sách các ID từ kết quả truy vấn
                ids = [hit['_id'] for hit in result['hits']['hits']]

                if len(ids) > 0:
                    # Nếu đã tồn tại, cập nhật list_name
                    # doc_id = result['hits']['hits'][0]['_id']
                    # existing_list = result['hits']['hits'][0]['_source']['list_name']
                    # assert name not in existing_list, f"{name} đã có trong danh sách."
                    # updated_list = existing_list + [name]
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
                    # Nếu chưa tồn tại, tạo document mới
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
    index_name = 'list_substring'
    es = Elasticsearch(
        ['https://daa681.es.us-east-1.aws.found.io'],  # thay đổi địa chỉ URL kết nối đến Elasticsearch
        http_auth=('elastic', 'xhBqmy8XqOYQSZYjspBVsnPK'),  # thêm thông tin đăng nhập
        scheme="https",
    )
    es.indices.create(index=index_name, ignore=400)
    cnt = 0
    for file_path in all_files:
        name = get_file_name(file_path)
        s = name.lower()
        n = len(s)
        vt = []
        for length in range(1, n + 1):
            for i in range(n - length + 1):
                if s[i:i + length].isalnum():
                    vt.append(s[i:i + length])
        vt = sorted(list(set(vt)))
        new_doc = {
            "keyname": name,
            "list_substring": vt
        }
        response = es.index(index=index_name, document=new_doc)
        print(f"Created new document have of {name}")


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
