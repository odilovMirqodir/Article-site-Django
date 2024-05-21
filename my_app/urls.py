from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),

    path('', index, name='index'),
    path('category/<int:pk>/', ArticleListByCategory.as_view(), name='category_list'),
    path('category/<int:pk>/', category_list, name='category_list'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article_details'),
    path('article/<int:pk>/', article_details, name='article_details'),
    path('add/', NewArticle.as_view(), name='add_article'),
    path('add/', add_article, name='add_article'),
    path('search/', SearchList.as_view(), name='search_results'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('add_comment/<int:article_id>/', add_comment, name='add_comment'),
    # path('test/', test)

]
