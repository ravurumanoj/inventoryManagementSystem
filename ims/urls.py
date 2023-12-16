"""
URL configuration for ims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from sopeonow import views

urlpatterns = [
    path('',views.home,name='home'),
    path('itemList/', views.itemList, name='itemList'),
    path('allOrders/', views.allOrders, name='allOrders'),
    path('allTransactions/', views.allTransactions, name='allTransactions'),
    path('sellItem/<int:item_id>/', views.sellItem, name='sellItem'),
    path('createItem/', views.createItem, name='createItem'),
    path('itemDetails/<int:item_id>/', views.itemDetails, name='itemDetails'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),  
    path('item/<int:item_id>/orders/placed/', views.orders_placed, name='orders_placed'),
    path('item/<int:item_id>/orders/received/', views.orders_received, name='orders_received'),
    path('item/<int:item_id>/orders/canceled/', views.orders_canceled, name='orders_canceled'),
    path('item/<int:item_id>/transactions/', views.item_transactions, name='item_transactions'),
    path('order/<int:order_id>/<int:new_quantity>/confirm_received/', views.confirm_received, name='confirm_received'),  
    path('order/<int:order_id>/confirm_canceled/', views.confirm_canceled, name='confirm_canceled'),
    # path('admin/', admin.site.urls),
]
