from django.test import TestCase
from django.urls import reverse,resolve
from online_site.views import ProfileList, getDetailProfile

class TestViews(TestCase):

    def test_project(self):
        url = reverse('main_site')
        self.assertEqual(resolve(url).func.view_class, ProfileList)
    def test_detail_profile_url(self):
        url = reverse('detail_profile',args=[''])
        self.assertEqual(resolve(url).func,getDetailProfile)
