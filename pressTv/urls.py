from django.urls import path, include

from . import views

app_name = "pressTv"

urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path("change_news_page/<str:pageNum>", views.changePage, name="change_news_page"),
]