"""autoOrderService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from service import views
from bookLend import views as bookView

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('', views.login),
                  path('login/', views.login),
                  path('index&keyword=<str:keyword>/', views.index),
                  path('index/', views.index),
                  path('canteenMainPage&id=<int:ID>/', views.canteenMainPage),
                  path('canteenMainPage/', views.canteenMainPage),
                  path('register/', views.register),
                  path('index_canteen/', views.index_canteen),
                  path('changeInfo_canteen/', views.changeInfo_canteen),
                  path('order/', views.order),
                  path('changeInfo/', views.changeInfo),
                  path('order_canteen/', views.order_canteen),
                  path('logout/', views.logout),
                  path('restaurant/', views.restaurant),

                  path('bookLend/index', bookView.index),
                  path('bookLend/readers', bookView.readers),
                  path('bookLend/addBook', bookView.addBook),
                  path('bookLend/addReader', bookView.addReader),
                  path('bookLend/addLend', bookView.addLend),
                  path('bookLend/readerLendS&ID=<str:keyword>/', bookView.readerLendS),
                  path('bookLend/readerLend', bookView.readerLend),
                  path('bookLend/changeInfo&ISBN=<str:keyword>', bookView.changeInfoBook),
                  path('bookLend/changeInfo_reader&ID=<str:keyword>', bookView.changeInfoReader),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
