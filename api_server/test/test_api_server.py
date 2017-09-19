import unittest

from api_server import api_server
from webtest import TestApp
from mock import Mock


class ApiServerTestCase(unittest.TestCase):
    def setUp(self):
        self.mocked_es = Mock()
        self.mocked_es.search.return_value = {'hits': {'hits': []}}

    def test_empty_results_from_es(self):
        api_server.es = self.mocked_es
        self.app = TestApp(api_server.app)

        res = self.app.get('/ask?q=lala', expect_errors=True)
        assert res.status_int == 200

    def test_no_query_param_provided(self):
        api_server.es = self.mocked_es
        self.app = TestApp(api_server.app)

        res = self.app.get('/ask', expect_errors=True)
        assert res.status_int == 400

    def test_json_response(self):
        self.mocked_es.search.return_value = {'hits': {'hits': [
            {
                "_score": 1.0,
                "_source": {
                    "title": "page title",
                    "url": "page url",
                    "main_content": "page content"
                }
            }
        ]}}

        api_server.es = self.mocked_es
        self.app = TestApp(api_server.app)
        res = self.app.get('/ask?q=page', expect_errors=True)
        self.assertEqual(1, len(res.json))
        self.assertTrue(res.status_int == 200)
