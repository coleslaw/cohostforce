from django.test import SimpleTestCase
from django.urls import reverse,resolve
from online_site.views import ProfileList, getDetailProfile

class TestUrls(SimpleTestCase):

    def test_main_site_url(self):
        url = reverse('main_site')
        self.assertEqual(resolve(url).func.view_class, ProfileList)
    def test_detail_profile_url(self):
        url = reverse('detail_profile',args=[''])
        self.assertEqual(resolve(url).func,getDetailProfile)
