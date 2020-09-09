from flask import current_app


def add_to_index(index, model):
     '''Adds an an arbitrary data model to an elastic search index. Helpful to maintain cross platform and interopability'''
     if not current_app.elasticsearch:
          return
     payload = {}
     for field in model.__searchable__:
          payload[field] = field[0]
     current_app.elasticsearch.index(index = index, id = model.id, body = payload)

def remove_from_index(index, model):
     '''Used to remove an element from an elastic doc. Helpful when one need to delete the model eg a user or a post'''
     if not current_app.elasticsearch:
          return
     current_app.elasticsearch.delete(index=index, id = model.id)

def query_index(index, query, page, per_page):
     '''Used to query(search) an elastic search document'''
     if not current_app.elasticsearch:
          return [], 0
     #Below is the search functionality
     search = current_app.elasticsearch.search(
          index = index,
          body = {'query' : {'multi_match': {'query' : query, 
          'fields' : ['*']}},
          'from' :(page -1) * per_page, 
          'size' : per_page
     })
     ids = [int(hit['_id']) for hit in search['hits']['hits']]
     return ids, search['hits']['total']['value']