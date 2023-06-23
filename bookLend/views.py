from django.shortcuts import render, redirect, HttpResponse
from dateutil.relativedelta import relativedelta
from django.utils.datetime_safe import datetime

from bookLend.models import *


def index(request):
    error_msg = ""
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'bookLend/index.html', {'books': books, 'error_msg': error_msg})

    if request.method == 'POST':
        if request.POST.get('delete'):
            print("------")
            ISBN = request.POST.get('ISBN')
            book = Book.objects.get(ISBN=ISBN)
            if book.available_num < book.book_num:
                print("node")
                error_msg = "有书籍借阅中，无法删除"
                return HttpResponse(data=error_msg)
            else:
                book.delete()
                print("delete")
                error_msg = "删除成功"
                return HttpResponse(data=error_msg)

        if request.POST.get('search'):
            print("-------")
            ISBN_key = request.POST.get('ISBN')
            name_key = request.POST.get('name')
            press_key = request.POST.get('press')
            author_key = request.POST.get('author')
            abstract_key = request.POST.get('abstract')

            year = request.POST.get('year')
            month = request.POST.get('month')
            day = request.POST.get('day')

            if year == '' and month == '' and day != '':
                date_key = '-' + day
            elif year == '' and day == '' and month != '':
                date_key = '-' + month + '-'
            elif month == '' and day == '' and year != '':
                date_key = year + '-'
            else:
                date_key = ''

            books = Book.objects.filter(ISBN__icontains=ISBN_key,
                                        name__icontains=name_key,
                                        press__icontains=press_key,
                                        author__icontains=author_key,
                                        abstract__icontains=abstract_key,
                                        publishDate__icontains=date_key
                                        )
            print(books)
            return render(request, 'bookLend/index.html', {'books': books, 'error_msg': error_msg})

        return HttpResponse(status=500)


def readers(request):
    error_msg = ""
    if request.method == 'GET':
        readers_obj = Reader.objects.all()
        return render(request, 'bookLend/readers.html', {'readers': readers_obj, 'error_msg': error_msg})

    if request.method == 'POST':
        if request.POST.get('delete'):
            print("------")
            ID = request.POST.get('ID')
            reader_obj = Reader.objects.get(ID=ID)

            if reader_obj.is_lend:
                print("node")
                error_msg = "有书籍借阅中，无法删除"
                return HttpResponse(status=200)
            else:
                reader_obj.delete()
                print("delete")
                error_msg = "删除成功"
                return HttpResponse(status=200)

        if request.POST.get('search'):
            ID_key = request.POST.get('ID')
            name_key = request.POST.get('name')

            sex_key = request.POST.get('sex')
            if sex_key == 'true':
                sex_key = True
            elif sex_key == 'false':
                sex_key = False
            else:
                sex_key = 'any'

            department_key = request.POST.get('department')

            grade_key = request.POST.get('grade')

            readers_obj = Reader.objects.filter(ID__icontains=ID_key,
                                                name__icontains=name_key,
                                                department__icontains=department_key,
                                                )
            if sex_key != 'any':
                readers_obj = readers_obj.filter(sex=sex_key)
            if grade_key != 'any':
                readers_obj = readers_obj.filter(grade=int(grade_key))

            print(readers_obj)
            return render(request, 'bookLend/readers.html', {'readers': readers_obj, 'error_msg': error_msg})

        return HttpResponse(status=500)


def addBook(request):
    error_msg = ""
    if request.method == 'GET':
        return render(request, 'bookLend/addBook.html', {'error_msg': error_msg})

    if request.method == 'POST':
        if request.POST.get('addBook'):
            ISBN = request.POST.get('ISBN')
            name = request.POST.get('name')
            press = request.POST.get('press')
            author = request.POST.get('author')
            abstract = request.POST.get('abstract')
            year = request.POST.get('year')
            month = request.POST.get('month')
            day = request.POST.get('day')
            book_num = request.POST.get('book_num')
            available_num = book_num

            if Book.objects.filter(ISBN=ISBN).exists():
                error_msg = "该书已经注册"
                return render(request, 'bookLend/addBook.html', {'error_msg': error_msg})

            if ISBN == "":
                error_msg = "ISBN不能为空"
                return render(request, 'bookLend/addBook.html', {'error_msg': error_msg})

            if book_num == "":
                error_msg = "书的数量不能为空"
                return render(request, 'bookLend/addBook.html', {'error_msg': error_msg})

            info = {
                'ISBN': ISBN,
                'name': name,
                'press': press,
                'author': author,
                'abstract': abstract,
                'publishDate': str(year) + "-" + str(month) + "-" + str(day),
                'book_num': book_num,
                'available_num': available_num
            }

            Book.objects.create(**info)
            error_msg = "书籍创建成功"

            return render(request, 'bookLend/addBook.html', {'error_msg': error_msg})

        return HttpResponse(status=500)


def addReader(request):
    error_msg = ""
    if request.method == 'GET':
        return render(request, 'bookLend/addReader.html', {'error_msg': error_msg})

    if request.method == 'POST':
        if request.POST.get('addReader'):
            print("--------")
            ID = request.POST.get('ID')
            name = request.POST.get('name')

            sex = request.POST.get('sex')
            if sex == 'true':
                sex = True
            elif sex == 'false':
                sex = False

            department = request.POST.get('department')
            grade = request.POST.get('grade')

            if Reader.objects.filter(ID=ID).exists():
                error_msg = "该生已经注册"
                return render(request, 'bookLend/addReader.html', {'error_msg': error_msg})

            if ID == "":
                error_msg = "ID不能为空"
                return render(request, 'bookLend/addReader.html', {'error_msg': error_msg})

            if name == "":
                error_msg = "姓名不能为空"
                return render(request, 'bookLend/addReader.html', {'error_msg': error_msg})

            info = {
                'ID': ID,
                'name': name,
                'sex': sex,
                'department': department,
                'grade': grade,
                'is_lend': False,
                'lend_permission': True,
            }

            Reader.objects.create(**info)
            error_msg = "读者创建成功"

            return render(request, 'bookLend/addReader.html', {'error_msg': error_msg})

        return HttpResponse(status=500)


def addLend(request):
    error_msg = ""
    if request.method == 'GET':
        return render(request, 'bookLend/addLend.html', {'error_msg': error_msg})

    if request.method == 'POST':
        ID = request.POST.get('ID')
        ISBN_list = request.POST.getlist('ISBN')
        lend_num_list = request.POST.getlist('lend_num')

        reader_obj = Reader.objects.get(ID=ID)

        if not Reader.objects.filter(ID=ID).exists():
            error_msg = "没有找到读者"
            return render(request, 'bookLend/addLend.html', {'error_msg': error_msg})

        for lend_record in Lend.objects.filter(reader_id=ID):
            if lend_record.return_last() < 0:
                # 有不良记录
                reader_obj.lend_permission = False
                reader_obj.save()

        if not reader_obj.lend_permission:
            error_msg = "该读者有未按期归还记录，无法借出"
            return render(request, 'bookLend/addLend.html', {'error_msg': error_msg})

        reader_obj.is_lend = True
        reader_obj.save()

        Lend_obj = 0

        try:
            Lend_obj = Lend.objects.create(reader_id=ID, return_date=datetime.now() + relativedelta(days=+30))
        except Exception as ex:
            print("lend", ex)

        try:
            print(ISBN_list, lend_num_list)
            for ISBN, lend_num in zip(ISBN_list, lend_num_list):
                book = Book.objects.get(ISBN=ISBN)

                if book.available_num < int(lend_num):
                    error_msg = str(book.name) + "没有剩余量，无法借出"
                    return render(request, 'bookLend/addLend.html', {'error_msg': error_msg})

                book.available_num -= int(lend_num)
                book.save()

                LendBookList.objects.create(book=book, num=lend_num, Lend=Lend_obj)

            error_msg = "添加借阅信息成功"

        except Exception as ex:
            print("lend-list", ex)

        return render(request, 'bookLend/addLend.html', {'error_msg': error_msg})


def readerLendS(request, keyword=''):
    error_msg = ""
    if request.method == 'GET':
        reader = Reader.objects.get(ID=keyword)

        if Lend.objects.filter(reader_id=keyword).exists():
            lend_books = LendBookList.objects.filter(Lend__reader=reader)
            date_now = datetime.now()

            return render(request, 'bookLend/readerLendS.html', {'error_msg': error_msg,
                                                                 'lend_books': lend_books,
                                                                 'reader': reader,
                                                                 'date_now': date_now})

        error_msg = "没有借阅记录"
        return render(request, 'bookLend/readerLendS.html', {'error_msg': error_msg,
                                                             'reader': reader,})


def readerLend(request):
    error_msg = ""
    if request.method == 'GET':
        if LendBookList.objects.all().exists():
            lend_records = LendBookList.objects.all()
            return render(request, 'bookLend/readerLend.html', {'error_msg': error_msg,
                                                                'lend_records': lend_records})
        else:
            error_msg = "没有记录"
            return render(request, 'bookLend/readerLend.html', {'error_msg': error_msg})

    if request.method == 'POST':
        lend_list_ID = request.POST.get('LendListID')
        lend_book_list = LendBookList.objects.get(ID=lend_list_ID)
        book = lend_book_list.book
        reader_obj = lend_book_list.Lend.reader
        lend = lend_book_list.Lend

        try:
            # 删除单类书的借阅记录
            print("删除该借阅记录")
            book.available_num += lend_book_list.num
            lend_book_list.delete()
            book.save()
        except Exception as ex:
            error_msg = "删除具体借阅记录时出错"
            print(ex)
            return render(request, 'bookLend/readerLend.html', {'error_msg': error_msg})

        # 如果一次性的借书已经没有借阅记录
        lend_flag = False
        for lend_book_list_s in LendBookList.objects.all():
            if lend_book_list_s.Lend.ID == lend.ID:
                lend_flag = True
                break

        if not lend_flag:
            # try:
            print("删除借阅项目")
            lend.delete()

        try:
            print("try")
            # 查看借阅人是否还有其他借阅记录
            if not Lend.objects.all().exists():
                print("删除借阅问题")
                reader_obj.is_lend = False
                reader_obj.lend_permission = True
                reader_obj.save()

                error_msg = "借阅记录删除操作完成"
                lend_records = LendBookList.objects.all()

                return render(request, 'bookLend/readerLend.html',
                              {'error_msg': error_msg, 'lend_records': lend_records})

            print("not null")
            reader_lend = False
            for lend in Lend.objects.all():
                print("-------")
                if lend.reader.ID == reader_obj.ID:
                    print("还有借阅记录")
                    reader_lend = True
                    break

            if not reader_lend:
                print("删除借阅问题")
                reader_obj.is_lend = False
                reader_obj.lend_permission = True
                reader_obj.save()

        except Exception as ex:
            print(ex)
            return render(request, 'bookLend/readerLend.html', {'error_msg': error_msg})

        error_msg = "借阅记录删除操作完成"
        lend_records = LendBookList.objects.all()

        return render(request, 'bookLend/readerLend.html', {'error_msg': error_msg, 'lend_records': lend_records})


def changeInfoBook(request, keyword=''):
    error_msg = ""
    if request.method == 'GET':
        book = Book.objects.get(ISBN=keyword)
        return render(request, 'bookLend/changeInfo.html', {'error_msg': error_msg, 'book': book})

    if request.method == 'POST':
        book = Book.objects.get(ISBN=request.POST.get('ISBN'))

        if request.POST.get('name') != "":
            book.name = request.POST.get('name')

        if request.POST.get('press') != "":
            book.press = request.POST.get('press')

        if request.POST.get('year') != "" or request.POST.get('month') != "" or request.POST.get('day') != "":
            date = request.POST.get('year') + "-" + request.POST.get('year') + "-" + request.POST.get('year')
            book.publishDate = date

        if request.POST.get('author') != "":
            book.author = request.POST.get('author')

        if request.POST.get('abstract') != "":
            book.abstract = request.POST.get('abstract')

        if request.POST.get('book_num') != "":
            if int(request.POST.get('book_num')) < int(book.book_num) - int(book.available_num):
                error_msg = "借出的数量比现有的数量多"
                return render(request, 'bookLend/changeInfo.html', {'error_msg': error_msg, 'book': book})

            book.book_num = request.POST.get('book_num')

        book.save()

        return render(request, 'bookLend/changeInfo.html', {'error_msg': error_msg, 'book': book})


def changeInfoReader(request, keyword=''):
    error_msg = ""
    if request.method == 'GET':
        reader = Reader.objects.get(ID=keyword)
        return render(request, 'bookLend/changeInfo_reader.html', {'error_msg': error_msg, 'reader': reader})

    if request.method == 'POST':
        reader_obj = Reader.objects.get(ID=request.POST.get('ID'))

        if request.POST.get('name') != "":
            reader_obj.name = request.POST.get('name')

        if request.POST.get('department') != "":
            reader_obj.department = request.POST.get('department')

        if request.POST.get('sex') != "":
            sex = request.POST.get('sex')
            if sex == 'true':
                sex = True
            else:
                sex = False
            reader_obj.sex = sex

        if request.POST.get('grade') != "":
            reader_obj.grade = request.POST.get('grade')

        reader_obj.save()

        return render(request, 'bookLend/changeInfo.html', {'error_msg': error_msg, 'reader': reader_obj})
