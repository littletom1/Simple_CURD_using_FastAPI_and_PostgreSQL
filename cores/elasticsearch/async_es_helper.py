# # from opensearchpy import OpenSearch
# from decouple import config
# from elasticsearch import Elasticsearch
# from elasticsearch.exceptions import NotFoundError, RequestError
# from fastapi import HTTPException, status
# import warnings
# from elasticsearch import AsyncElasticsearch
# warnings.filterwarnings('ignore')


# class ElasticSearch:
#     def __init__(self):
#         self.host = config('ELASTICSEARCH_HOST')
#         self.port = config('ELASTICSEARCH_PORT')
#         self.client = AsyncElasticsearch([f"{self.host}:{self.port}"])

#     async def search(self, index_name, query):
#         if not await self.check_index_is_exists(index_name):
#             return None
#         body = {'query': query}
#         rs = await self.client.search(
#             body=body,
#             index=index_name
#         )
#         if rs['hits']['hits']:
#             return rs['hits']['hits'][0]['_source']
#         return None


#     async def check_index_is_exists(self, index_name):
#         return await self.client.indices.exists(index_name)

#     async def get_by_query(self, index_name, query='', fields: list[str] = [], sort_by='id', order='desc'):
#         try:
#             if not await self.check_index_is_exists(index_name):
#                 raise RequestError
#             body = {}
#             if query:
#                 body['query'] = query
#             else:
#                 body['query'] = {
#                     "match_all": {}
#                 }
#             if fields:
#                 body['_source'] = fields
#             body['size'] = 2000
#             body['sort'] = [{sort_by: order}]
#             rs = await self.client.search(
#                 body=body,
#                 index=index_name,
#             )
#         except RequestError as e:  # TH field đó khổng thể sort/ mapping chưa có field đó
#             print(e)
#             return {
#                 'data': [],
#                 'metadata': {
#                     "current_page": 0,
#                     "page_size": 0,
#                     "total_items": 0,
#                     "total_page": 0
#                 }
#             }
#         data = []
#         for item in rs['hits']['hits']:
#             data.append(item['_source'])
#         # data = rs
#         total = rs['hits']['total']['value']
#         metadata = {
#             "total_items": total,
#         }
#         response = dict()
#         response['data'] = data
#         response['metadata'] = metadata
#         return response

#     async def get_all(self, index_name, sort_by='id', order='desc'):
#         try:
#             if not self.check_index_is_exists(index_name):
#                 raise RequestError
#             body = {}
#             body['query'] = {
#                 "match_all": {}
#             }
#             body['size'] = 2000
#             body['sort'] = [{sort_by: order}]
#             rs = await self.client.search(
#                 body=body,
#                 index=index_name,
#             )
#         except RequestError as e:  # TH field đó khổng thể sort/ mapping chưa có field đó
#             return {
#                 'data': [],
#                 'metadata': {
#                     "current_page": 0,
#                     "page_size": 0,
#                     "total_items": 0,
#                     "total_page": 0
#                 }
#             }
#         data = []
#         for item in rs['hits']['hits']:
#             data.append(item['_source'])
#         # data = rs
#         total = rs['hits']['total']['value']
#         metadata = {
#             "total_items": total,
#         }
#         response = dict()
#         response['data'] = data
#         response['metadata'] = metadata
#         return response

#     async def paginate(self, index_name, query, page=1, page_size=15, sort_by='id', order='desc', sorts: list[dict] = []):
#         offset = 0
#         if page != 1 and page_size != 0:
#             offset = (page - 1) * page_size
#         try:
#             if not await self.check_index_is_exists(index_name):
#                 raise RequestError
#             body = {
#                 "from": offset,
#                 "size": page_size,
#             }
#             multi_sort = []
#             if sorts:
#                 body["sort"] = sorts
#             else:
#                 body["sort"] = [{sort_by: order}]
#             if query:
#                 body['query'] = query
#             rs = await self.client.search(
#                 body=body,
#                 index=index_name,
#             )
#         except RequestError as e:  # TH field đó khổng thể sort/ mapping chưa có field đó
#             try:
#                 body = {
#                     # "query": query,
#                     "from": offset,
#                     "size": page_size,
#                     "sort": [{f'{sort_by}.keyword': order}]
#                 }
#                 if query:
#                     body["query"] = query
#                 rs = await self.client.search(
#                     body=body,
#                     index=index_name,
#                 )
#             except:
#                 return {
#                     'data': [],
#                     'metadata': {
#                         "current_page": 0,
#                         "page_size": 0,
#                         "total_items": 0,
#                         "total_page": 0
#                     }
#                 }
#         data = []
#         for item in rs['hits']['hits']:
#             data.append(item['_source'])
#         # data = rs
#         total = rs['hits']['total']['value']
#         total_page = int((total + page_size - 1) / page_size)
#         metadata = {
#             "current_page": page,
#             "page_size": page_size,
#             "total_items": total,
#             "total_page": total_page
#         }
#         response = dict()
#         response['data'] = data
#         response['metadata'] = metadata
#         return response

#     async def get_a_document(self, index_name, id):
#         if not await self.check_index_is_exists(index_name):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"Object with the id: {id} is not available")
#         return await self.client.get(index=index_name, id=id, ignore=[404])

#     async def create_index(self, index_name, index_body=None):
#         # if not settings:
#         #     settings = {
#         #         'index': {
#         #             'number_of_shards': 4
#         #         }
#         #     }
#         #
#         # index_body = {
#         #     'settings': settings
#         # }

#         response = await self.client.indices.create(index_name, body=index_body)
#         return response

#     async def delete_index(self, index_name):
#         return await self.client.indices.delete(
#             index=index_name
#         )

#     async def add_document_to_index(self, index_name, document):
#         return await self.client.index(
#             index=index_name,
#             body=document,
#             id=document['id'],
#             refresh=True
#         )

#     async def update_a_document(self, index_name, id, document):
#         return await self.client.update(
#             index=index_name,
#             body={'doc': document},
#             id=id,
#             refresh=True
#         )

#     async def delete_document(self, index_name, id):
#         return await self.client.delete(
#             index=index_name,
#             id=id
#         )
# # # Successful response!
# # # {'name': 'instance-0000000000', 'cluster_name': ...}
