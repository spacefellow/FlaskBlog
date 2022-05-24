from views import app


class TestViews:
    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_posts(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def teardown(self):
        pass
