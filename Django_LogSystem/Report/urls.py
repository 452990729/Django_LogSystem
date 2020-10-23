from django.urls import path,re_path
from . import views

urlpatterns = [
    path('new/', views.CreateNew, name="CreateNew"),
    path('loginfor/', views.Index, name="Index"),
    path('sub/', views.SubAlin, name="SubAlin"),
    path('sub/subsingledetail/<str:project>/', views.SubSingleDetail, name='SubSingleDetail'),
    path('sub/comment/<str:project>/', views.SubComment, name='SubComment'),
    path('subdetail/<str:number>', views.SubDetail, name="SubDetail"),
    path('<str:project>/', views.Detail, name='Detail'),
    path('<str:project>/del/', views.Del, name='Del'),
    path('', views.Index, name="Index"),
]
