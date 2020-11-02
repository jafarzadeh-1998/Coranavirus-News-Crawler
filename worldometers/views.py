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

def exctractTable(table):
    thead = []
    for col in table.find("thead").find_all("th"):
        thead.append(col.get_text(separator=" ").strip())
    tbody = []
    for row in table.find("tbody").find_all("tr"):
        rowData = {"columns" :[], "countryName": ""}
        for rc in row.find_all("td"):
            if rc.find("a", class_="mt_a") is not None:
                rowData["countryName"] = rc.find("a").get("href")
                rowData["columns"].append(rc.find("a").get_text().strip())
            else:
                rowData["columns"].append(rc.get_text())
        tbody.append(rowData)
    return {"head": thead,"body": tbody}

def getTable(request):
    url = "https://www.worldometers.info/coronavirus/"
    bsContainer = bs((requests.get(url=url).content), "html.parser")
    return JsonResponse(data=exctractTable(bsContainer.find("table")))

def str_to_bool(s):
    if s.lower() == 'true':
         return True
    elif s.lower() == 'false':
         return False
    else:
         raise ValueError

def sortTable(request):
    sort_by = request.GET['sort_by']
    is_dec = str_to_bool(request.GET['is_dec'])
    
    url = "https://www.worldometers.info/coronavirus/"
    bsContainer = bs((requests.get(url=url).content), "html.parser")
    table = exctractTable(bsContainer.find("table"))
    colIndex = 0
    for i in range(len(table['head'])):
        if table['head'][i] == sort_by:
            colIndex = i
            break
    if colIndex != 1:
        table['body'] = sorted(table['body'],
                            key=lambda t:\
                            int(''.join(filter(str.isdigit, t['columns'][colIndex].replace(",", "") )))
                            if t['columns'][colIndex] != "" else 0,
                            reverse=is_dec)
    else:
        table['body'] = sorted(table['body'], key=lambda t:\
            t['columns'][colIndex].replace("\n", ""),
            reverse=is_dec)
    return JsonResponse(data=table)

def showCountry(request, countryName):
    pass


PAGINATION = 5

def News(request):
    url = "https://www.worldometers.info/coronavirus/"
    bsContainer = bs((requests.get(url=url).content), "html.parser")
    allNews = bsContainer.find_all('div', class_="news_post")
    for index in range(len(allNews)):
        if index == PAGINATION:
            break
        liTag = allNews[index].find('li')
        print(liTag)
        print(liTag.get_text())