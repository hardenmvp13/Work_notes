'''
python

# 登陆验证
def auth(func):
    '''
     判断是否登录装饰器
     '''

    def inner(request, *args, **kwargs):
        ck = request.session.get("username")
        '''
        如果没有登陆返回到login.html
        '''
        if not ck:
            return redirect("/login.html")
        return func(request, *args, **kwargs)

    return inner


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        pwd = md5(pwd)
        dic = {"flag": False}
        obj = User.objects.filter(username=username, pwd=pwd).first()
        if obj:
            request.session["username"] = username
            return redirect("/index.html")
        else:
            print(dic)
            return HttpResponse(json.dumps(dic))


@auth
def index(request):
    user = request.session.get("username")
    business = Business.objects.all().values("name")
    host_list = Host.objects.all().values("id", "host", "port", "business__name")
    username = User.objects.all().values("username")
    return render(request, 'index.html',
                  {'host_list': host_list, "business": business, "user": user, "username": username})


@auth
def addhost(request):
    business = Business.objects.all().values("name")
    if request.method == "POST":
        user = request.session.get("username")
        host = request.POST.get("host")
        port = request.POST.get("port")
        select_business = request.POST.get("business")
        business_id = Business.objects.filter(name=select_business).values("id")[0]
        host = Host.objects.create(host=host,
                                   port=port,
                                   business_id=business_id["id"])
        # host.business.add(*business)
        return render(request, "index.html")

    return render(request, "index.html", {"business": business})


@auth
def up_business(request):
    if request.method == "POST":
        user = request.session.get("username")
        host = request.POST.get("host")
        port = request.POST.get("port")
        business_name = request.POST.get("business")
        username = request.POST.get("username")
        print(host, port, business_name, username)
        return render(request, "保存成功")


'''