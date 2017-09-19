## User Guide

### How to run

* Start elasticsearch in a docker container `make start_elasticsearch` (elasticsearch will become available under localhost:9200)
* Scrape conditions using scrapy as follows `make scrape` (this is expected to generate around 3000 docs in elasticsearch)
* Start the api-server `make start_api_server` 

The api can be used as follows 

`curl 'http://localhost:5000/ask?q=heart%20attack%20complications'`

The `relevance_score` indicates how relevant a result is to the question asked.

## Dev Guide:

### Testing

There are two types of tests:
* Scrapy spider contracts that verify scraping functionality
  * Run them using `make scrapy_test`
* Unit tests for the api server
  * Run them using `make unit_test`

Run them all at once with `make test`
