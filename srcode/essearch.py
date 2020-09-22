from flask import current_app
from config import Config
import re, requests, json

bonsai_search_url = Config.ELASTIC_SEARCH_URL
def connect_to_bonsai_search():
     """Connects to bonsai Search service and establishes a connection with the cluster.
     """     
     # Parse the auth and host from env:
     auth = re.search('https\:\/\/(.*)\@', bonsai_search_url).group(1).split(':')
     host = bonsai_search_url.replace('https://%s:%s@' % (auth[0], auth[1]), '')

     # optional port
     match = re.search('(:\d+)', host)
     if match:
          p = match.group(0)
          host = host.replace(p, '')
          port = int(p.split(':')[1])
     else:
          port=443

     # Connect to cluster over SSL using auth for best security:
     es_header = [{
     'host': host,
     'port': port,
     'use_ssl': True,
     'http_auth': (auth[0],auth[1])
     }]
     return es_header

def add_to_index(index, model):
     '''Adds an an arbitrary data model to an elastic search index. Helpful to maintain cross platform and interopability'''
     if not current_app.elasticsearch:
          return
     payload = {}
     for field in model.__searchable__:
          payload[field] = field[0]
     payload_json = json.dumps(payload)
     requests.post(f'{bonsai_search_url}/{index}/{model.id}/ -H Content-Type:application/json -d @{payload_json}')
     #current_app.elasticsearch.index(index = index, id = model.id, body = payload)

def remove_from_index(index, model):
     '''Used to remove an element from an elastic doc. Helpful when one need to delete the model eg a user or a post'''
     if not current_app.elasticsearch:
          return
     requests.delete(bonsai_search_url/index/model.id)
     #current_app.elasticsearch.delete(index=index, id = model.id)

def query_index(index, query, page, per_page):
     '''Used to query(search) an elastic search document'''
     if not current_app.elasticsearch:
          return [], 0
     #Below is the search functionality
     search = requests.get(f'{bonsai_search_url}/{index}/_search'/
          {'query' : {'multi_match': {'query' : query, 
          'fields' : ['*']}},
          'from' :(page -1) * per_page, 
          'size' : per_page
     })
     ids = [int(hit['_id']) for hit in search['hits']]
     return ids, search['hits']['hits']['value']