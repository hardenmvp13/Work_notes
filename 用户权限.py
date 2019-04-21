'''
方法一:

utils/auth.py

```python
class MyAuthtication(object):
    """
    登陆认证
    """
    def authenticate(self, request):
        # _request获取最原始的request
        token = request._request.GET.get('token') # 获取URL上的token
        # 获取请求头的token信息
        token = request.META.get('HTTP_AUTHORIZATION', '')

        token_obj = UserInfo.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在restframwork内部会将整个两个字段赋值给request,以供后续使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass
```

users/model.py

```python
class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP用户'),
        (3, 'SVIP用户'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=64, default=uuid.uuid4())
```

utils/permission.py

```python
# http://127.0.0.1:8000/order/?token=f5769d727d6f28e613bd9f4bf49fde97
class VIPPermission(object):
    message = "必须是VIP才可以访问"

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True


class MyPermission(object):
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True

```

view.py

```python
class OrderView(APIView):
    """
    相关业务
    """
    authentication_classes = []   # 不需认证
    # 认证用户登陆,才可以进行访问
    # 局部认证类
    # authentication_classes = [MyAuthtication, ]
    # 局部权限
    # permission_classes = [VIPPermission,]
    # 访问频率
    # throttle_classes = [VisitThrottle,]
    def get(self, request, *args, **kwargs):
        # request.user
        # request.auth
        ret = {}
        try:
            ret["code"] = 0
            ret["msg"] = "successful"
            ret["data"] = ORDER_DICT
        except Exception as e:
            ret["code"] = 1
            ret["msg"] = str(e)
        return Response(ret)

```

settings.py

```python
REST_FRAMEWORK = {
  # 全局使用的认证类
   "DEFAULT_AUTHENTICATION_CLASSES": ['apps.utils.auth.MyAuthtication', ],
}
```





方法二：

model.py

```python

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=64, verbose_name="权限名称")
    url = models.CharField(null=True, blank=True, max_length=60)
    parent_id = models.IntegerField(null=True, blank=True, verbose_name="菜单ID")

    class Meta:
        db_table = "yangji_permission"
        verbose_name_plural = "权限表"
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, verbose_name="角色名称")
    remark = models.TextField(verbose_name="备注")
    permission = models.ManyToManyField(Permission, related_name='roles', verbose_name="角色拥有的权限",
                                        error_messages={'blank': '权限不能为空', 'null': '权限不能为空'})

    class Meta:
        db_table = "yangji_role"
        verbose_name_plural = "角色表"
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    用户表
    """
    index = models.IntegerField(null=True, blank=True, verbose_name="序号")
    username = models.CharField(max_length=32, unique=True, error_messages={'unique': '用户已经存在'}, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    token = models.CharField(max_length=64, null=True, blank=True, verbose_name="token")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, related_name='user',
                             verbose_name="角色",)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "yangji_users"
        ordering = ["index", ]
        verbose_name_plural = "用户表"
        verbose_name = verbose_name_plural
```

views.py

```python


# 创建角色及角色权限
class CreateRole(APIView):
    def post(self, request):
        ret = {}
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            user = UserInfo.objects.filter(token=token).first()
            if user:
                name = request._request.POST.get('name')
                remark = request._request.POST.get('remark')
                per_list = request._request.POST.get('per_list')
                per_list = json.loads(per_list)
                parent_list = Permission.objects.filter(parent_id=0).values_list('id', flat=True)
                per_list = list(set(per_list).difference(set(parent_list)))
                Role.objects.update_or_create(name=name, remark=remark)
                role = Role.objects.get(name=name)
                role.permission.set(per_list)
                RoleHistory.objects.create(role_id=role.id, role=role.name, modified_name=user.username).save()
                ret["code"] = 0
                ret["msg"] = "创建角色权限成功"
            else:
                ret["code"] = 0
                ret["msg"] = "请重新登陆"
                return Response(ret, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            ret["code"] = 1
            ret["msg"] = "创建角色及角色权限：%s" % str(e)
        return JsonResponse(ret)


# 查看某个角色权限
class PermissionDetail(APIView):

    def get_object(self, role_id):
        try:
            return Role.objects.filter(id=role_id).first()
        except:
            pass

    def get(self, request, role_id):
        ret = {}
        try:
            role = self.get_object(role_id)
            # parent_list = role.permission.exclude(parent_id=0).values_list('parent_id', 'id')     # [(1, 9), (1, 10)]
            # parent_list = [j for i in parent_list for j in i]          # [1, 9, 1, 10]
            #
            # per_list = list(set(parent_list))               # [1, 10, 9]
            per_list = role.permission.exclude(parent_id=0).values_list('id', flat=True)
            data_dict = {}
            data_dict["name"] = role.name
            data_dict["remark"] = role.remark
            data_dict["per_list"] = per_list
            ret["code"] = 0
            ret["data"] = data_dict
        except Exception as e:
            ret["code"] = 1
            ret["msg"] = "查看某个角色权限：%s" % str(e)
        return Response(ret)


# 修改角色权限
class PermissionUpdate(APIView):
    def get_object(self, role_id):
        try:
            return Role.objects.get(id=role_id)
        except:
            pass

    def put(self, request, role_id):
        ret = {}
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            user = UserInfo.objects.filter(token=token).first()
            if user:
                role = self.get_object(role_id)
                data = request.data
                remark = data.get('remark')
                per_str = data.get('per_list')
                role.remark = remark
                role.save()
                data_list = json.loads(per_str)
                parent_list = Permission.objects.filter(parent_id=0).values_list('id', flat=True)
                per_list = list(set(data_list).difference(set(parent_list)))
                role.permission.set(per_list)
                RoleHistory.objects.filter(role_id=role_id).update(modified_name=user.username)
                ret["code"] = 0
                ret["msg"] = "修改成功"
            else:
                ret["code"] = 1
                ret["msg"] = "请重新登陆"
                return Response(ret, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            ret["code"] = 1
            ret["msg"] = "修改角色权限：%s" % str(e)
        return Response(ret)

    def delete(self, request, role_id):
        ret = {}
        try:
            role = self.get_object(role_id)
            role.permission.clear()
            Role.objects.filter(id=role_id).delete()
            RoleHistory.objects.filter(role_id=role_id).delete()
            ret["code"] = 0
            ret["msg"] = "成功"
        except Exception as e:
            ret["code"] = 1
            ret["msg"] = "删除角色权限：%s" % str(e)
        return JsonResponse(ret)


```








'''