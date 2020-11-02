from django.urls import path, include

from . import views

app_name = "worldometers"

urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path("get_table/", views.getTable, name="getTable"),
    path("get_sorted_table/", views.sortTable, name="getSortedTable"),
    path("country/<str:countryName>", views.showCountry, name="showCountryNew"),
    path("top_news/<int:pageNum>", views.News, name="news"),
]
