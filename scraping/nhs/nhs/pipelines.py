# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch

INDEX_MAPPING = {
    "properties": {
        "title": {"type": "text", "index": True},
        "url": {"type": "keyword", "index": False},
        "main-content": {"type": "text", "index": True}
    }
}


class ElasticsearchPipeline(object):

    def __init__(self):
        self.es = Elasticsearch(['localhost'],
                                http_auth=('elastic', 'changeme'), )

        if not self.es.indices.exists(index="nhs"):
            self.es.create(index="nhs", id=1, doc_type="condition_page",
                           body=INDEX_MAPPING)

    def process_item(self, item, spider):
        res = self.es.index(index="nhs", doc_type='condition_page', body=item)
        return item
