def changeInfo_canteen(request):
    if request.method == 'GET':
        pass # 略去
    if request.method == 'POST':
        user = CanteenInfo.objects.get(canteenID=request.session['ID'])
        # 随便找个不影响你业务逻辑分支的地方写这段代码就行
        if request.POST.get('delete_canteen'):
            # 判断发回来的请求有没有删除餐厅
            try:
                user.delete()
                status = 200
            except Exception as ex:
                status = 500
            return HttpResponse(status=status)
        if request.POST.get('modify_password'):
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            try:
                if user.password == old_password:
                    user.password = new_password
                    user.save()
                    status = 200
                else:
                    status = 500
            except Exception as ex:
                status = 500
            return HttpResponse(status=status)