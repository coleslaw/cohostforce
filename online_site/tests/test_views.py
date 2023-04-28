from django.test import TestCase, Client
from django.urls import reverse, resolve
from online_site.views import ProfileList, getDetailProfile

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_site_url = reverse('main_site')
        self.detail_profile_url = [reverse('detail_profile', args=['iloveioi']),
                                   reverse('detail_profile', args=['alo']),
                                   reverse('detail_profile', args=['HelloimTuan']),
                                   reverse('detail_profile', args=['iloveioi'])]
    def test_project_list_get(self):
        response = self.client.get(self.main_site_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    def test_detail_profile_get(self):
        self.assertEqual(resolve(url).func, getDetailProfile)
