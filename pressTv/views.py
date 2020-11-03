from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

import requests, urllib, datetime
from bs4 import BeautifulSoup as bs

class index(TemplateView):
    template_name = "pressTv/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baseUrl = 'https://www.presstv.com/default/search?q={keyword}&from={from_}&to={to}&section=1&page=1'
        url = baseUrl.format(keyword="COVID-19",
                             to=str(datetime.date.today()),
                             from_=str(datetime.date.today() - datetime.timedelta(days=30)))
        bsContainer = bs((requests.get(url=url).content), "html.parser")
        newsLink = set()
        newsList = []
        for news in bsContainer.find_all("a", class_="result-item-link"):
            link = "https://www.presstv.com" + news.get("href")
            newsLink.add(link)
            title = news.find("div", class_="result-item-title").get_text()
            summary = news.find("div", class_="result-item-summery").get_text()
            pubdate = news.find("span", class_="result-item-puddate").get_text()
            datetime_pubdate = "".join(pubdate.split(",")[1:])
            datetime_pubdate = datetime.datetime.strptime(datetime_pubdate, " %B %d %Y ")
            newsList.append({"link":link,
                             "pubdate":pubdate,
                             "title":title,
                             "summary":summary,
                             "date": datetime_pubdate})

        url = baseUrl.format(keyword="coronavirus",
                             to=str(datetime.date.today()),
                             from_=str(datetime.date.today() - datetime.timedelta(days=30)))
        coronaContainer = bs((requests.get(url=url).content), "html.parser")

        for news in coronaContainer.find_all("a", class_="result-item-link"):
            link = "https://www.presstv.com" + news.get("href")
            if link in newsLink:
                continue
            title = news.find("div", class_="result-item-title").get_text()
            summary = news.find("div", class_="result-item-summery").get_text()
            pubdate = news.find("span", class_="result-item-puddate").get_text()
            datetime_pubdate = "".join(pubdate.split(",")[1:])
            datetime_pubdate = datetime.datetime.strptime(datetime_pubdate, " %B %d %Y ")
            newsList.append({"link":link,
                             "pubdate":pubdate,
                             "title":title,
                             "summary":summary,
                             "date": datetime_pubdate})

        newsList = sorted(newsList, key=lambda n:n["date"], reverse=True)
        context["newsList"] = newsList
        return context
    

def changePage(request, pageNum):
    baseUrl = 'https://www.presstv.com/default/search?q={keyword}&from={from_}&to={to}&section=1&page='+pageNum
    url = baseUrl.format(keyword="COVID-19",
                        to=str(datetime.date.today()),
                        from_=str(datetime.date.today() - datetime.timedelta(days=30)))
    bsContainer = bs((requests.get(url=url).content), "html.parser")
    newsLink = set()
    newsList = []
    for news in bsContainer.find_all("a", class_="result-item-link"):
        link = "https://www.presstv.com" + news.get("href")
        newsLink.add(link)
        title = news.find("div", class_="result-item-title").get_text()
        summary = news.find("div", class_="result-item-summery").get_text()
        pubdate = news.find("span", class_="result-item-puddate").get_text()
        datetime_pubdate = "".join(pubdate.split(",")[1:])
        datetime_pubdate = datetime.datetime.strptime(datetime_pubdate, " %B %d %Y ")
        newsList.append({"link":link,
                        "pubdate":pubdate,
                        "title":title,
                        "summary":summary,
                        "date": datetime_pubdate})

    url = baseUrl.format(keyword="coronavirus",
                        to=str(datetime.date.today()),
                        from_=str(datetime.date.today() - datetime.timedelta(days=30)))
    coronaContainer = bs((requests.get(url=url).content), "html.parser")

    for news in coronaContainer.find_all("a", class_="result-item-link"):
        link = "https://www.presstv.com" + news.get("href")
        if link in newsLink:
            continue
        title = news.find("div", class_="result-item-title").get_text()
        summary = news.find("div", class_="result-item-summery").get_text()
        pubdate = news.find("span", class_="result-item-puddate").get_text()
        datetime_pubdate = "".join(pubdate.split(",")[1:])
        datetime_pubdate = datetime.datetime.strptime(datetime_pubdate, " %B %d %Y ")
        newsList.append({"link":link,
                        "pubdate":pubdate,
                        "title":title,
                        "summary":summary,
                        "date": datetime_pubdate})

    newsList = sorted(newsList, key=lambda n:n["date"], reverse=True)
    return JsonResponse(data={"newsList": newsList})
