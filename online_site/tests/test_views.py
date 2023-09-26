from django.test import TestCase, Client
from django.urls import reverse, resolve
from online_site.views import ProfileList, getDetailProfile

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_site_url = reverse('main_site')
        self.list_detail_profile_url = [reverse('detail_profile', args=['iloveioi']),
                                   reverse('detail_profile', args=['HelloimTuan']),
                                   reverse('detail_profile', args=['-14'])]
        self.error_list_detail_profile_url = [reverse('detail_profile', args=['att']),
                                        reverse('detail_profile', args=['alo']),
                                        reverse('detail_profile', args=['-'])]
    def test_project_list_get(self):
        response = self.client.get(self.main_site_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    def test_detail_profile_get(self):
        for url in self.list_detail_profile_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'PrintProfileWithElasticsearch.html')
        for url in self.error_list_detail_profile_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, 'PrintProfileWithElasticsearch.html')
