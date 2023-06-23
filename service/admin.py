from django.contrib import admin

# Register your models here.
from django.contrib import admin
from service.models import CustomerInfo, Canteen, Dish, Table, Order
from bookLend.models import Book, Reader, Lend, LendBookList

admin.site.register([CustomerInfo, Canteen, Dish, Table, Order])
admin.site.register([Book, Reader, Lend, LendBookList])
