# Generated by Django 4.1.3 on 2023-06-23 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Canteen",
            fields=[
                ("canteenID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "password",
                    models.DecimalField(
                        blank=True, decimal_places=0, max_digits=6, null=True
                    ),
                ),
                ("canteenName", models.CharField(max_length=15)),
                ("address", models.TextField(blank=True, null=True)),
                ("descript", models.TextField(blank=True, null=True)),
                (
                    "logoURL",
                    models.FileField(
                        blank=True, null=True, upload_to="static/canteen/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CustomerInfo",
            fields=[
                ("userID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "password",
                    models.DecimalField(
                        blank=True, decimal_places=0, max_digits=6, null=True
                    ),
                ),
                (
                    "nickName",
                    models.CharField(
                        default=models.AutoField(primary_key=True, serialize=False),
                        max_length=10,
                    ),
                ),
                ("descript", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Table",
            fields=[
                ("tableID", models.AutoField(primary_key=True, serialize=False)),
                ("tablePrice", models.DecimalField(decimal_places=0, max_digits=3)),
                ("tableLocation", models.TextField(blank=True, null=True)),
                ("capacity", models.DecimalField(decimal_places=0, max_digits=2)),
                (
                    "canteenID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.canteen",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.CharField(default="", max_length=50)),
                ("dishList", models.CharField(default="", max_length=500)),
                ("totalPrice", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "state",
                    models.DecimalField(
                        choices=[(1, "Complete"), (0, "not-Complete")],
                        decimal_places=0,
                        default=0,
                        max_digits=1,
                    ),
                ),
                (
                    "canteenID",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.canteen",
                    ),
                ),
                (
                    "customerID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.customerinfo",
                    ),
                ),
                (
                    "tableID",
                    models.ForeignKey(
                        default=30,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.table",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dish",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dishName", models.CharField(max_length=15)),
                ("dishPrice", models.DecimalField(decimal_places=2, max_digits=6)),
                ("picName", models.CharField(default="no_name", max_length=64)),
                (
                    "picURL",
                    models.ImageField(
                        default="photos/pic-none-replace.png", upload_to="photos"
                    ),
                ),
                (
                    "canteenID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.canteen",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="table",
            constraint=models.CheckConstraint(
                check=models.Q(("tablePrice__gte", 0), ("tablePrice__lte", 999)),
                name="tablePrice_number",
            ),
        ),
        migrations.AddConstraint(
            model_name="order",
            constraint=models.CheckConstraint(
                check=models.Q(("totalPrice__gte", 0), ("totalPrice__lte", 50000)),
                name="Order_number",
            ),
        ),
        migrations.AddConstraint(
            model_name="dish",
            constraint=models.CheckConstraint(
                check=models.Q(("dishPrice__gte", 0), ("dishPrice__lte", 5000)),
                name="dishPrice_number",
            ),
        ),
    ]