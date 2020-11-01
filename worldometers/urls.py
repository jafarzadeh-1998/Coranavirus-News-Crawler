from django.urls import path, include

from . import views

app_name = "worldometers"

urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path("get_table/", views.getTable, name="getTable"),
]
