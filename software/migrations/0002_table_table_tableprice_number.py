# Generated by Django 4.1.2 on 2022-11-17 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("software", "0001_initial"),
    ]

    operations = [
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
                        to="software.canteen",
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
    ]
