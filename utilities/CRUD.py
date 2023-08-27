from utilities.elastic_config import *
from utilities.date_conversion import convert_date


def delete_index(index_name):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        es.indices.delete(index=index_name)
        return {'status': True, 'msg': f'Index - {index_name} deleted successfully'}
    return {'status': False, 'msg': f'Index - {index_name} already deleted or does not exists'}


def update_by_id(index_name, id, doc):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        try:
            # doc.update({'updated_at':convert_date()})
            # del doc['_id']
            return es.update(index=index_name, id=id, body={"doc": doc})
        except ModuleNotFoundError:
            return {'status': False, 'msg': f'id = {id} does not exists'}
    else:
        return {'status': False, 'msg': f'Index = {index_name} does not exists'}


def delete(index_name, id):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        es.delete(index=index_name, id=id)
        return {'status': True, 'msg': f'Index = {index_name} bearing _id = {id} deleted successfully'}
    return {'status': False, 'msg': f'Index - {index_name} already deleted or does not exists'}


def get_by_id(index_name, id):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        try:
            response = es.get(index=index_name, id=id)
            return response['_source']
        except ModuleNotFoundError:
            return {'status': False, 'msg': f'id = {id} does not exists'}
    else:
        return {'status': False, 'msg': f'Index = {index_name} does not exists'}

def get_by_query_agg(index_name, query):
    result = es.search(index=index_name, body=query)
    return result

def get_by_query(index_name, query):
    result = es.search(index=index_name, body=query)
    result = result['hits']['hits']
    final_list = []
    for res in result:
        res['_source'].update({'_id':res['_id']})
        final_list.append(res['_source'])
    return final_list


def get_all(index_name,size=None):
    result = es.search(index=index_name, body={"size":size,"query": {"match_all": {}}})
    result = result['hits']['hits']
    count =len(result)
    final_list = []
    for res in result:
        res['_source'].update({'_id':res['_id']})
        final_list.append(res['_source'])
        
    return dict(data=final_list,count=count)


def create(index_name, mapping:dict):
    index_exists = es.indices.exists(index=index_name)
    if not index_exists:
        es.indices.create(index=index_name)
    mapping.update({'created_at':convert_date(),'updated_at':convert_date()})
    response = es.index(index=index_name, body=mapping)
    response_get_by_id =   get_by_id(index_name=index_name, id=response['_id'])
    try:
        response_get_by_id.update({'id': response['_id']})
        response_update =   update_by_id(index_name=index_name, id=response['_id'], doc=response_get_by_id)
        return   get_by_id(index_name=index_name, id=response_update['_id'])
    except Exception as e:
        return e

def get_all_scroll(index_name, batch_size):
    # Initialize the scroll API
    scroll = '2m' # Keep the search context alive for 2 minutes
    search_body = {"query": {"match_all": {}}}
    search_result = es.search(index=index_name, body=search_body, scroll=scroll, size=batch_size)

    # Get the total number of hits and initialize the results list
    total_hits = search_result['hits']['total']['value']
    results = []

    # Keep scrolling until all documents have been retrieved
    while len(search_result['hits']['hits']) > 0:
        # Append the current batch of results to the final list
        results += [hit['_source'] for hit in search_result['hits']['hits']]

        # Use the scroll ID to retrieve the next batch of results
        scroll_id = search_result['_scroll_id']
        search_result = es.scroll(scroll_id=scroll_id, scroll=scroll)

    # Return the final list of results
    return results
