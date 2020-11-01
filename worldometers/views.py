from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView

import requests, urllib
from bs4 import BeautifulSoup as bs

import requests

class index(TemplateView):
    template_name = "worldometers/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = "https://www.worldometers.info/coronavirus/"
        bsContainer = bs((requests.get(url=url).content), "html.parser")    
        maincounterDivs = list(bsContainer.find_all('div', id="maincounter-wrap"))
        context["totalNum"] = maincounterDivs[0].find("span").get_text()
        context["deathNum"] = maincounterDivs[1].find("span").get_text()
        context["recoverdNum"] = maincounterDivs[2].find("span").get_text()
        return context

def getTable(request):
    url = "https://www.worldometers.info/coronavirus/"
    bsContainer = bs((requests.get(url=url).content), "html.parser")
    table = bsContainer.find("table")
    thead = []
    for col in table.find("thead").find_all("th"):
        thead.append(col.get_text())
    tbody = []
    for row in table.find("tbody").find_all("tr"):
        rowData = {"columns" :[], "countryName": ""}
        for rc in row.find_all("td"):
            if rc.find("a", class_="mt_a") is not None:
                rowData["countryName"] = rc.find("a").get("href")
                rowData["columns"].append(rc.find("a").get_text())
            else:
                rowData["columns"].append(rc.get_text())
        tbody.append(rowData)
    return JsonResponse(data={"head": thead,"body": tbody})