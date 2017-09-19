venv:
	virtualenv venv
	. venv/bin/activate & pip install -r requirements.txt

start_elasticsearch:
	docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:5.6.1

start_api_server: venv
	. venv/bin/activate & python api_server/api_server/api_server.py

scrape: venv
	. venv/bin/activate & cd scraping/nhs; scrapy crawl conditions

test: unit_test scrapy_test

unit_test: venv
	. venv/bin/activate & cd api_server; nosetests -v test/*.py

scrapy_test: venv
	. venv/bin/activate & cd scraping/nhs; scrapy check conditions -v
