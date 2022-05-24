from fixtures import *


class TestViews:
    def setup(self):
        self.client = client

    def test_posts(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def teardown(self):
        pass
