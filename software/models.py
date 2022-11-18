from django.db import models


# Create your models here.
class CustomerInfo(models.Model):
    userID = models.AutoField(primary_key=True)
    password = models.DecimalField(max_digits=6, decimal_places=0)
    nickName = models.CharField(max_length=10, default=userID)
    descript = models.TextField(null=True, blank=True)


class Canteen(models.Model):
    canteenID = models.AutoField(primary_key=True)
    canteenName = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    descript = models.TextField(null=True, blank=True)
    logoURL = models.FileField(null=True, blank=True, upload_to='static/canteen/')


class Dish(models.Model):
    dishName = models.CharField(max_length=15)
    canteenID = models.ForeignKey('Canteen', on_delete=models.CASCADE)
    dishPrice = models.DecimalField(max_digits=6, decimal_places=2)
    picURL = models.FileField(null=True, blank=True, upload_to='static/dish/')

    class Meta:
        constraints = \
            [
                models.CheckConstraint(check=models.Q(dishPrice__gte=0) & models.Q(dishPrice__lte=5000),
                                       name='dishPrice_number')
            ]


class Table(models.Model):
    tableID = models.AutoField(primary_key=True)
    canteenID = models.ForeignKey('Canteen', on_delete=models.CASCADE)
    tablePrice = models.DecimalField(max_digits=3, decimal_places=0)
    tableLocation = models.TextField(null=True, blank=True)
    capacity = models.DecimalField(max_digits=2, decimal_places=0)

    class Meta:
        constraints = \
            [
                models.CheckConstraint(check=models.Q(tablePrice__gte=0) & models.Q(tablePrice__lte=999),
                                       name='tablePrice_number')
            ]


class Order(models.Model):
    customerID = models.ForeignKey('CustomerInfo', on_delete=models.CASCADE)
    canteenID = models.ForeignKey('Canteen', on_delete=models.CASCADE)
    dishList = models.ManyToManyField(to=Dish)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        constraints = \
            [
                models.CheckConstraint(check=models.Q(totalPrice__gte=0) & models.Q(totalPrice__lte=50000),
                                       name='Order_number')
            ]
