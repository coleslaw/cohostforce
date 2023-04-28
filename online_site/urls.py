from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.ProfileList.as_view() , name="main_site"),
    path('profiles/<str:name>', views.getDetailProfile, name="detail_profile"),
    # path('<str:pk>', views.DetailProfile.as_view(), name="detail_site"),

]