import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from .models import Profile, ContestResult
from django import forms
from elasticsearch import Elasticsearch
from .documents import ContestResultDocument, ProfileDocument
# Create your views here.
from elasticsearch_dsl.connections import connections

connections.create_connection()


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100)


def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


# class ProfileList(ListView):
#     model = Profile
#     template_name = "index.html"
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         keyword = self.request.GET.get('keyword',None)
#         if keyword:
#             queryset = Profile.objects.filter(name__icontains=keyword).order_by('name')
#         print(queryset)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['keyword'] = self.request.GET.get('keyword')
#         return context
#
#     def post(self, request , *args, **kwargs):
#         pass



# class DetailProfile(DetailView):
#     model = Profile
#     template_name = 'profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['contest_results'] = list(self.object.contests.all().values('name',
#                                                                             'rating_change', 'new_rating',
#                                                                             'title_change'))
#         print(context)
#         return context


def getDetailProfile(request, name):
    es = Elasticsearch()
    query_dict ={
        "size": 10000,
        "query":
            {
                "match":
                    {
                        "user.name": name
                    }
            }
    }
    result = es.search(index="contest_results", body=query_dict)
    results = result["hits"]["hits"]
    context = {"contest_results":[]}

    for result in results:
        old_key_result = result.pop("_source")
        result["source"] = old_key_result
        context["contest_results"].append(result["source"])
    query_dict = {
        "size": 10000,
        "query": {
            "match": {
                "name": name
            }
        }
    }
    result = es.search(index="profiles", body=query_dict)
    results = result["hits"]["hits"]
    context["data"] = results[0]["_source"]
    print(context)
    return render(request, 'PrintProfileWithElasticsearch.html', context)


class ProfileList(ListView):
    model = Profile
    template_name = "index.html"
    def get_queryset(self):
        queryset = []
        keyword = self.request.GET.get('keyword', "")
        es = Elasticsearch()
        keyword = keyword.replace("-",r"\-")
        query_dict = query_dict = {
            "size": 10000,
            "query": {
                "query_string": {
                    "query": "*" + keyword + "*",
                    "fields": ["name"]
                }
            }
        }
        result = es.search(index="profiles", body=query_dict)
        results = result["hits"]["hits"]
        for result in results:
            old_key_result = result.pop("_id")
            result["id"] = old_key_result
            old_key_result = result.pop("_source")
            result["source"] = old_key_result
        queryset = results
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword')
        return context

    def post(self, request, *args, **kwargs):
        pass
