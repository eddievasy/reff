from django.test import TestCase
from django.shortcuts import reverse # We use reverse so we don't have to hard-code URLs in our code; we can just reference their 'alias'

# First test -- just trying things out
class LandingPageTest(TestCase):
    # each method within the class represents a test

    def test_get(self):
        # self.client is an alternative to the requests package -- request.get(""), request.post() etc;
        # these methods are used to create HTTP requests;
        # we save the HTTP response to our request in 'response';
        response = self.client.get(reverse("landing-page"))
        # test that the response is 'OK' (i.e code 200)
        self.assertEqual(response.status_code, 200)
        # test that the template used in the response is the correct one
        self.assertTemplateUsed(response, "landing.html")


