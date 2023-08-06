from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleDeleteView,
    ArticleUpdateView,
    ArticleCreateView,
    )

urlpatterns=[
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("new/", ArticleCreateView.as_view(), name ="article_new"),
    path("", ArticleListView.as_view(), name="article_list"),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
