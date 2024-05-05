import pytest
from django.urls import reverse
from django.test import TestCase, Client
from unittest.mock import patch, Mock


class TestNewsView(TestCase):
    def setUp(self):
        # Client setup to make requests to your Django server
        self.client = Client()
        # Reverse the URL name to get the URL string (adjust 'news:index' to the actual URL name in your urls.py)
        self.url = reverse('news:index')

    @patch('news.views.requests.get')
    def test_news_view_status_code(self, mock_get):
        """
        Test that the news view returns a 200 status code and uses the correct template.
        We mock the 'requests.get' to control the external API responses.
        """
        # Mocking the API responses to ensure our view handles the data correctly
        mock_get.return_value.json.side_effect = [
            {
                "date": "2023-04-27",
                "exchangeRate": [
                    {"currency": "USD", "saleRate": 27.5, "purchaseRate": 27.0},
                    {"currency": "EUR", "saleRate": 29.5, "purchaseRate": 29.0}
                ]
            },
            {
                "data": {
                    "day": 400,
                    "stats": {"personnel_units": 10000, "tanks": 100},
                    "increase": {"personnel_units": 50, "tanks": 1}
                }
            },
            {
                "articles": [
                    {"source": {"name": "BBC"}, "author": "John Doe", "title": "News Title",
                     "description": "News description",
                     "url": "http://example.com", "publishedAt": "2023-04-27"}
                ]
            }
        ]

        # Making a GET request to the news view
        response = self.client.get(self.url)
        # Check for HTTP 200 response
        assert response.status_code == 200
        # Ensure the context contains the expected title
        assert 'page_title' in response.context
        assert response.context['page_title'] == 'News and Statistics'
        # Check for presence of 'data' in context used by the template
        assert 'data' in response.context

    @patch('news.views.requests.get')
    def test_news_view_content(self, mock_get):
        """
        Test the content of the response to ensure specific data is being passed to the template.
        """
        mock_get.return_value.json.side_effect = [
            # Include the same mock responses as above
        ]

        # Making a GET request to the news view
        response = self.client.get(self.url)
        # Check if the response content contains expected text
        content = response.content.decode()
        assert 'News and Statistics' in content
        assert 'Exchange rate data' in content
