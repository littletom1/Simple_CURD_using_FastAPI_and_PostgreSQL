# base_setting = {
#     'analysis': {
#         "tokenizer": {
#             "ngram_tokenizer": {
#                 "type": "nGram",
#                 "min_gram": "2",
#                 "max_gram": "3",
#                 "token_chars": ["letter", "digit"]
#             }
#         },
#         'analyzer': {
#             'whitespace_lowercase': {
#                 'tokenizer': 'whitespace',
#                 'filter': ['lowercase']
#             },
#             'ngram_analyzer': {
#                 'tokenizer': 'ngram_tokenizer',
#                 "char_filter": ["html_strip"],
#                 'filter': ['icu_folding', 'icu_normalizer', 'lowercase']
#             },
#             'my_standard': {
#                 'tokenizer': 'icu_tokenizer',
#                 "char_filter": ["html_strip"],
#                 'filter': ['icu_folding', 'icu_normalizer', 'lowercase']
#             }
#         }
#     },
#     'index': {
#         "number_of_shards": 1,
#         "number_of_replicas": 1,
#         "max_ngram_diff": 10
#     }
# }

# def get_setting_to_create_index(mapping, setting = None):
#     index_setting = {
#         'settings': setting if setting else base_setting,
#         'mappings': mapping
#     }
#     print(index_setting)
#     return index_setting