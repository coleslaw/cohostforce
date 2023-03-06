import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from .models import Profile
from django import forms
# Create your views here.

def detail_data(request):
    my_data = {'name': 'John', 'age': 30}
    return JsonResponse(my_data)

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100)

class ProfileList(ListView):
    model = Profile
    template_name = "index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword',None)
        if keyword:
            queryset = Profile.objects.filter(name__icontains=keyword).order_by('name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword')
        return context
    
    def post(self, request , *args, **kwargs):
        pass

class DetailProfile(DetailView):
    model = Profile
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contest_results'] = list(self.object.contests.all().values('name', 'rating_change', 'new_rating', 'title_change'))
        return context

    

