from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page


class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)