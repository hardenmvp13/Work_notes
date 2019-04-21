'''
pagination.py

```python
"""
分页器
"""
from django.utils.safestring import mark_safe


class Pagination:

    def __init__(self, request, all_count, per_num=10, max_show=11):
        try:
            self.current_page = int(request.GET.get('page', 1))
            if self.current_page <= 0:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1
        # 最多显示的页码数
        self.max_show = 11
        half_show = max_show // 2
        # 每页显示的数据条数
        self.per_num = 10
        # 总数量
        self.all_count = all_count
        # 总页码数
        self.total_num, more = divmod(all_count, per_num)
        if more:
            self.total_num += 1
        # 总页码数小于最大显示数： 显示总页码数
        if self.total_num <= max_show:
            self.page_start = 1
            self.page_end = self.total_num
        else:
            if self.current_page <= half_show:
                self.page_start = 1
                self.page_end = max_show
            elif self.current_page + half_show >= self.total_num:
                self.page_end = self.total_num
                self.page_start = self.total_num - max_show + 1
            else:
                self.page_start = self.current_page -half_show
                self.page_end = self.current_page + half_show
    @property
    def start(self):
        return (self.current_page - 1) * self.per_num
    @property
    def end(self):
        return self.current_page * self.per_num
    @property
    def show_li(self):
        # 存放li标签的列表
        html_list = []
        first_li = '<li><a href="/user_list/?page=1">首页</a><li>'
        html_list.append(first_li)

        if self.current_page == 1:
            per_li = '<li class="disable"><a><<</a></li>'
        else:
            per_li = '<li><a href="/user_list/?page={0}"><<</a></li>'.format(self.current_page - 1)
        html_list.append(per_li)

        for num in range(self.page_start, self.page_end + 1):
            if  self.current_page == num:
                li_html = '<li class="active"><a href="/user_list/?page={0}">{0}</a></li>'.format(num)
            else:
                li_html = '<li><a gref="/user_list/?page={0}">{0}</a></li>'.format(num)
            html_list.append(li_html)
        if self.current_page == self.total_num:
            next_li = '<li class="disabled"><a>>></a></li>'
        else:
            next_li = '<li><a href="/user_list/?page={0}">>></a></li>'.format(self.current_page + 1)
            html_list.append(next_li)
            last_li = '<li><a href="/user_list/?page={}">尾页</a></li>'.format(self.total_num)
            html_list.append(last_li)
            return mark_safe(''.join(html_list))
```

view.py

```python
def user_list(request):
    users = UserInfo.objects.all()
    page = Pagination(request, len(users))
    return render(request, 'user_list.html', {"data": users[page.start:page.end], 'html_str': page.show_li})
```





实战：

pagination.py

```python
class SlotPagination(object):

    def __init__(self, request, all_count, current_page, per_num):
        self.current_page = current_page
        # 每页显示的数据条数
        self.per_num = per_num
        # 总数量
        self.all_count = all_count

    @property
    def start(self):
        return (self.current_page - 1) * self.per_num
    @property
    def end(self):
        return self.current_page * self.per_num
    @property
    def total_num(self):
        # 总页码数
        total_num, more = divmod(self.all_count, self.per_num)
        if more:
            total_num += 1
        return total_num

```



view.py

```python
def get_slot(request):
    """
    获取槽位信息
    """
    ret = {}
    if request.method == 'POST':
        slots = slot1([1, 2, 3, 91, 92, 93])
        current_page = int(request.POST.get('page', 1))
        page_size = int(request.POST.get('size', 9))
        page = SlotPagination(request, len(slots), current_page, page_size)
        ret["code"] = 0
        ret["data"] = slots[page.start:page.end]
        ret["current_page"] = current_page
        ret["total_page"] = page.total_num
        ret["size"] = page_size
    else:
        ret["code"] = 1
        ret["msg"] = "请求方式不正确"

    return JsonResponse(ret)

def slot1(ignore=()):
  ......
```




'''