from django.urls import path, include

from . import views

app_name = "worldometers"

urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path("get_table/", views.getTable, name="getTable"),
    path("get_sorted_table/", views.sortTable, name="getSortedTable"),
    path("country/<str:countryName>/", views.countryInfo.as_view(), name="showCountryNew"),
    path("get_countries_name/", views.getCounteriesName, name="get_countries_name"),
    path("top_news/<int:pageNum>", views.News, name="news"),
]
