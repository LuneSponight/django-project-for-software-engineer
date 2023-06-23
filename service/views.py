import ast
import json

from django.shortcuts import render, redirect, HttpResponse

from service.models import *


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'error_msg': request.session.get('error_msg')})

    if request.method == 'POST':
        name = request.POST.get('account-name')
        password = request.POST.get('password')
        role = request.POST.get('role')

    try:
        if role == 'consumer':
            user = CustomerInfo.objects.get(nickName=name)

            if int(password) == user.password:
                request.session['login'] = True
                request.session['userName'] = user.nickName
                request.session['userID'] = user.userID
                return redirect("../index")
            else:
                return render(request, 'login.html', {
                    'error_msg': 'No such user.',
                    'Name': name})

        elif role == 'canteen':
            user = Canteen.objects.get(canteenName=name)
            if int(password) == user.password:
                request.session['login'] = True
                request.session['canteenName'] = user.canteenName
                request.session['canteenID'] = user.canteenID
                return redirect("../index_canteen")
            else:
                return render(request, 'login.html', {'error_msg': 'No such canteen.'})
    except Exception as ex:
        print(ex)
        return render(request, 'login.html', {'error_msg': 'An exception occurred.'})


def index(request, keyword=''):
    if request.method == 'GET':
        try:
            print(keyword)
            if keyword != "":
                canteen_list = Canteen.objects.filter(canteenName__icontains=keyword)

                if not canteen_list.exists():
                    canteen_list = [{'error_msg': '没有匹配项.'}]

                return render(request, 'index.html',
                              {'canteen_list': list(canteen_list), 'Name': request.session['userName']})

            else:
                error_msg = "请输入内容"
                return render(request, 'index.html', {'Name': request.session['userName'], 'error_msg': error_msg})

        except Exception as ex:
            print(ex)
            return render(request, 'index.html', {'error_msg': 'An exception occurred, '
                                                               'Maybe the database received incorrect data'})


def canteenMainPage(request, ID=0):
    if request.method == 'GET':
        try:
            canteen = Canteen.objects.get(canteenID=ID)
            dishes = Dish.objects.filter(canteenID=canteen.canteenID)
            tables = Table.objects.filter(canteenID=canteen.canteenID)

            return render(request, 'canteenMainPage.html', {"canteen": canteen, "dishes": dishes, "tables": tables})
        except Exception as ex:
            print(ex)
            return redirect('../index')

    if request.method == 'POST':

        dictionary = ""
        try:
            dictionary = request.POST.get('content')
        except Exception as e:
            print(e)

        canteen = Canteen.objects.get(canteenName=request.POST.get('canteenID'))
        dishes = json.loads(dictionary)
        totalPrice = request.POST.get('totalPrice')
        customer = CustomerInfo.objects.get(userID=request.session['userID'])
        table = Table.objects.get(tableID=request.POST.get('tableID'))
        time = request.POST.get('time')

        dish_list = "{"

        for dish in dishes.values():
            dish_list = dish_list + '"' + str(dish['dishName']) + '": ' + str(dish['dishNum']) + ', '

        dish_list = dish_list + "}"
        dish_list = ast.literal_eval(dish_list)

        dish_list = json.dumps(dish_list)

        info = {'customerID_id': customer.userID,
                'canteenID_id': canteen.canteenID,
                'dishList': dish_list,
                'totalPrice': totalPrice,
                'state': 0,
                'time': time,
                'tableID_id': table.tableID}

        try:
            order_obj = Order.objects.create(**info)
            order_obj.save()

            return HttpResponse(status=200)

        except Exception as e:
            print(e)
            return HttpResponse(status=500)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    info = {}

    role = request.POST.get('role')

    print(role)

    if role == 'consumer':
        info['nickName'] = request.POST.get('userName')

        if CustomerInfo.objects.filter(nickName=info['nickName']):
            request.session['error_msg'] = '该用户名已被注册，请重新输入'
            return render(request, 'register.html')

        info['password'] = request.POST.get('password')
        info['descript'] = "there's no description"
        try:
            CustomerInfo.objects.create(**info)
        except Exception as e:
            print(e)

    elif role == 'canteen':
        info['canteenName'] = request.POST.get('userName')

        if Canteen.objects.filter(canteenName=info['canteenName']):
            error_message = '该餐厅名已被注册，请重新输入'
            return render(request, 'register.html', {'error_msg': error_message})

        info['password'] = request.POST.get('password')
        info['descript'] = "there's no description"
        info['address'] = "haven't set address"
        info['logoURL'] = "NULL"
        try:
            Canteen.objects.create(**info)
        except Exception as e:
            print(e)

    else:
        print("an error occurred in role choosing")

    request.session['message'] = '注册成功，请重新登入'
    return redirect('../login')


def index_canteen(request):
    ID = request.session['canteenID']
    dishes = Dish.objects.filter(canteenID=ID)
    tables = Table.objects.filter(canteenID=ID)

    if request.method == 'GET':
        return render(request, 'index_canteen.html', {
            'tables': tables,
            'dishes': dishes,
            'canteenName': request.session.get('canteenName')})

    if request.method == 'POST':

        if request.POST.get('dishName'):

            dishName = request.POST.get('dishName')
            dishPrice = request.POST.get('dishPrice')

            if dishName == "" or dishPrice == "":
                return render(request, 'index_canteen.html', {"error_msg": "输入不能为空", 'tables': tables,
                                                              'dishes': dishes,
                                                              'canteenName': request.session.get('canteenName')})
            elif not is_number(dishPrice):
                return render(request, 'index_canteen.html', {"error_msg": "输入不是数字", 'tables': tables,
                                                              'dishes': dishes,
                                                              'canteenName': request.session.get('canteenName')})
            elif float(dishPrice) <= 0:
                return render(request, 'index_canteen.html', {"error_msg": "数字不能为负", 'tables': tables,
                                                              'dishes': dishes,
                                                              'canteenName': request.session.get('canteenName')})

            info = {
                'canteenID': Canteen.objects.get(canteenID=request.session['canteenID']),
                'dishName': request.POST.get('dishName'),
                'dishPrice': request.POST.get('dishPrice'),
                'picURL': request.FILES.get('picURL'),
                'picName': request.FILES.get('picURL').name
            }

            Dish.objects.create(**info)
            print(info)

            return HttpResponse('菜品保存成功')

        if request.POST.get('table'):
            table = json.loads(request.POST.get('table'))

            info = {'canteenID': Canteen.objects.get(canteenID=request.session['canteenID']),
                    'tablePrice': table['tablePrice'], 'tableLocation': table['tableLocation'],
                    'capacity': table['capacity']}
            try:
                Table.objects.create(**info)
            except Exception as e:
                print(e)

        if request.POST.get('deleteTable'):
            deleteTable = json.loads(request.POST.get('deleteTable'))
            print(deleteTable)
            try:
                Table.objects.filter(**deleteTable).delete()
            except Exception as ex:
                print(ex)

        if request.POST.get('deleteDish'):
            deleteDish = json.loads(request.POST.get('deleteDish'))
            print(deleteDish)
            try:
                del_dish = Dish.objects.filter(canteenID=request.session.get('canteenID'),
                                               dishName=deleteDish['dishName'],
                                               dishPrice=deleteDish['dishPrice'])
                print(del_dish)
                del_dish.delete()
            except Exception as ex:
                print(ex)

        return render(request, 'index_canteen.html')


def order(request):
    if request.method == 'GET':
        user = CustomerInfo.objects.get(userID=request.session['userID'])
        orders = Order.objects.filter(customerID=user, state=0).values('time',
                                                                       'id',
                                                                       'canteenID__canteenName',
                                                                       'canteenID__address',
                                                                       'dishList', 'tableID',
                                                                       'totalPrice')

        order_list = []
        for single_order in orders:
            try:
                print("-------")
                dishes = ""
                dishList = json.loads(single_order['dishList'])
                for dishName, dishNum in dishList.items():
                    dishes = dishes + dishName + " × " + str(dishNum) + " ,\t"
                print(dishes)
                order_dict = {'time': single_order['time'], 'orderID': single_order['id'],
                              'canteenName': single_order['canteenID__canteenName'],
                              'address': single_order['canteenID__address'],
                              'dishList': dishes, 'totalPrice': single_order['totalPrice'],
                              'tableID': single_order['tableID']}
                print("------------")
                print("orderdict", order_dict)
                order_list.append(order_dict)
            except Exception as e:
                print("error:", e)

        print(order_list)

        return render(request, 'order.html', {'error_msg': request.session.get('error_msg'),
                                              'orders': order_list,
                                              'userID': user})


def changeInfo(request):
    user = CustomerInfo.objects.get(userID=request.session['userID'])

    if request.method == 'GET':
        error_msg = None
        if request.session.get('message'):
            error_msg = request.session.get('message')
            request.session['message'] = None

        return render(request, 'changeInfo.html', {'error_msg': error_msg,
                                                   'user': user})

    if request.method == 'POST':
        if request.POST.get('QDeleteAccount'):
            user = CustomerInfo.objects.get(userID=request.session['userID'])
            try:
                user.delete()
                return HttpResponse(status=200)

            except Exception as e:
                print(e)
                return HttpResponse(status=500)

        if request.POST.get('nickName') or request.POST.get('descript'):
            nickName = request.POST.get('nickName')
            descript = request.POST.get('descript')

            if CustomerInfo.objects.filter(nickName=nickName).exists():
                error_msg = "用户名不能重复"
                return render(request, 'changeInfo.html', {'error_msg': error_msg, 'user': user})

            if nickName == "":
                error_msg = "用户名不能为空"
                return render(request, 'changeInfo.html', {'error_msg': error_msg, 'user': user})

            user.nickName = nickName
            user.descript = descript
            user.save()

            request.session['userName'] = user.nickName

            return render(request, 'changeInfo.html', {'message': request.session.get('message'), 'user': user})

        if request.POST.get('old-password'):
            old = request.POST.get('old-password')
            new = request.POST.get('new-password')
            error_msg = ""

            if int(old) == round(user.password):

                if old == new:
                    error_msg = "新旧密码不能相同"
                    return render(request, 'changeInfo.html', {'error_msg': error_msg, 'user': user})
                elif new == "":
                    error_msg = "新密码不能为空"
                    return render(request, 'changeInfo.html', {'error_msg': error_msg, 'user': user})
                else:
                    user.password = new
                    user.save()
                    error_msg = "密码更改成功"
                    return render(request, 'changeInfo.html', {'error_msg': error_msg, 'user': user})

            else:
                return render(request, 'changeInfo.html', {'error_msg': error_msg, 'user': user})


def changeInfo_canteen(request):
    canteenID = request.session['canteenID']
    canteen = Canteen.objects.get(canteenID=canteenID)
    canteenName = canteen.canteenName
    descript = canteen.descript
    address = canteen.address
    password = canteen.password
    error_msg = ""

    if request.method == 'GET':
        return render(request, 'changeInfo_canteen.html', {
            'message': request.session.get('message'),
            'canteenID': canteenID,
            'canteenName': canteenName,
            'descript': descript,
            'address': address,
            'password': password
        })

    if request.method == 'POST':
        if request.POST.get("old-password"):
            old_pwd = request.POST.get("old-password")
            new_pwd = request.POST.get("new-password")
            if old_pwd != canteen.password:
                error_msg = "密码错误"
            else:
                if old_pwd == new_pwd:
                    error_msg = "新旧密码不能相同"
                else:
                    print("yes")
                    canteen.password = new_pwd
                    canteen.save()

            return render(request, 'changeInfo_canteen.html', {
                'error_msg': error_msg,
                'canteenID': canteenID,
                'canteenName': canteenName,
                'descript': descript,
                'address': address,
                'password': password
            })

        elif request.POST.get('canteenName') or request.POST.get('address') or request.POST.get(
                'descript') or request.FILES.get('logoURL'):
            print("-------")

            canteenName = request.POST.get('canteenName')
            descript = request.POST.get('descript')
            address = request.POST.get('address')
            logoURL = request.FILES.get('logoURL')

            print("logo:", logoURL)

            if Canteen.objects.filter(canteenName=canteenName).exists():
                error_msg = "餐厅名不能重复"
                return render(request, 'changeInfo_canteen.html', {
                    'error_msg': error_msg,
                    'canteenID': canteenID,
                    'canteenName': canteenName,
                    'descript': descript,
                    'address': address,
                    'password': password
                })

            if canteenName != "":
                canteen.canteenName = canteenName

            if address != "":
                canteen.address = address

            if descript != "":
                canteen.descript = descript

            if logoURL:
                print("----------")
                canteen.logoURL = logoURL

            canteen.save()
            print(canteen.logoURL)

            return render(request, 'changeInfo_canteen.html', {
                'error_msg': error_msg,
                'canteenID': canteenID,
                'canteenName': canteen.canteenName,
                'descript': canteen.descript,
                'address': canteen.address,
                'password': password
            })

        elif request.POST.get('delete_canteen'):
            print("--------")
            canteen = Canteen.objects.get(canteenID=request.session['canteenID'])
            try:
                canteen.delete()
                return HttpResponse(status=200)

            except Exception as e:
                print(e)
                return HttpResponse(status=500)

        else:
            message = "NONE INPUT"

        return render(request, 'changeInfo_canteen.html', {
            'message': message,
        })


def order_canteen(request):
    if request.method == 'GET':
        canteenID = request.session['canteenID']
        Canteen.objects.get(canteenID=request.session['canteenID'])
        orders = Order.objects.filter(canteenID=canteenID, state=0).values('time',
                                                                           'id',
                                                                           'customerID__nickName',
                                                                           'dishList',
                                                                           'tableID__tableLocation',
                                                                           'totalPrice')

        order_list = []
        for single_order in orders:
            try:
                dishes = ""
                dishList = json.loads(single_order['dishList'])
                for dishName, dishNum in dishList.items():
                    dishes = dishes + dishName + " × " + str(dishNum) + " ,\t"
                order_dict = {'time': single_order['time'], 'orderID': single_order['id'],
                              'customerName': single_order['customerID__nickName'],
                              'dishList': dishes,
                              'totalPrice': single_order['totalPrice'],
                              'table': single_order['tableID__tableLocation']}
                order_list.append(order_dict)
            except Exception as e:
                print("error:", e)

        return render(request, 'order_canteen.html', {'error_msg': request.session.get('error_msg'),
                                                      'orders': order_list,
                                                      })

    if request.method == 'POST':
        print("----------")
        orderID = request.POST.get('orderID')
        order_obj = Order.objects.get(id=orderID)
        print(order_obj)
        order_obj.state = 1
        order_obj.save()

        return HttpResponse(status=200)


def logout(request):
    request.session.flush()
    request.session['message'] = '登出成功，请重新登入'
    return redirect('../login')


def restaurant(request):
    canteen_list = Canteen.objects.all()
    return render(request, 'restaurant.html', {'canteen_list': canteen_list})
