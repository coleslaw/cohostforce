from django.urls import path, include
from .views import ProfileList, DetailProfile, detail_data

urlpatterns = [
    path("", ProfileList.as_view() , name="main_site"),
    path('<int:pk>', DetailProfile.as_view(), name="detail_site"),
    path('detail_data', view=detail_data, name='detail_data'),
]