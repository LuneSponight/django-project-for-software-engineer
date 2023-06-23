from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# 1)	能够通过书籍基本信息（包括：书号、书名、出版社、出版日期、作者、内容摘要）单个或以AND方式组合多个条件查询书籍信息；0
# 2)	对于每一种书籍，除可查看其基本信息之外还可查看其总数以及目前在馆数量 0
# 3)	可增添新的书籍 0
# 4)	可删除已有书籍（如有读者借了该书籍尚未归还，则不允许删除）0
# 5)	可修改书籍的基本信息 0
# 6)	能够通过读者基本信息（包括：证号、姓名、性别、系名、年级）单个或以AND方式组合多个条件查询读者信息 0
# 7)	对于每位读者除可查看其基本信息之外，还可查看其已借的书籍列表、数量、借还日期 0
# 8)	可增添新的读者 0
# 9)	可删除已有读者（如该读者有尚未归还的借书，则不允许删除）0
# 10)	可修改读者的基本信息 0
# 11)	可完成借还书籍的手续 0
# 12)	还书时如超期，应该显示超期天数 X
# 13)	借书时如果有超期的书没有还，则不允许借书 0
# 14)	可查询有哪些读者有超期的书没有还，列出这些读者的基本信息 0

from django.db import models


class Book(models.Model):
    ISBN = models.CharField(max_length=30, primary_key=True, unique=True)
    name = models.CharField(max_length=50, default="no name")
    press = models.CharField(max_length=50, default="no press")
    publishDate = models.CharField(max_length=20, default="no date")
    author = models.CharField(max_length=50, default="no author")
    abstract = models.TextField(max_length=200, null=True, blank=True)
    book_num = models.IntegerField()
    available_num = models.IntegerField()


class Reader(models.Model):
    ID = models.CharField(max_length=30, primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    sex = models.BooleanField(default=True)  # True 是男孩
    department = models.CharField(max_length=20)
    grade = models.IntegerField()
    is_lend = models.BooleanField(default=False)
    lend_permission = models.BooleanField(default=True)


class Lend(models.Model):
    ID = models.AutoField(primary_key=True)
    lend_date = models.DateField(auto_now=True)
    return_date = models.DateField()
    reader = models.ForeignKey('Reader', on_delete=models.CASCADE)

    def return_last(self):
        a = self.return_date - datetime.date(datetime.now())
        return a.days


class LendBookList(models.Model):
    ID = models.AutoField(primary_key=True)
    Lend = models.ForeignKey('Lend', on_delete=models.CASCADE, default=0)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    num = models.IntegerField()
