# forms.py
'''
python
from django import forms
from .models import CraneManage


class CraneForm(forms.ModelForm):
    class Meta:
        model = CraneManage
        fields = "__all__"
'''

# view.py

'''
python
def crane_list(request):
    ret = {}
    all_crane = CraneManage.objects.all()
    ret["code"] = 0
    ret["data"] = list(all_crane.values('crane_num', 'work_range', 'change_slot'))
    return JsonResponse(ret)


def crane_manage(request, edit_id=None):
    ret = {}
    obj = CraneManage.objects.filter(id=edit_id).first()
    form_obj = CraneForm(instance=obj)
    if request.method == "POST":
        form_obj = CraneForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            ret["code"] = 0
            ret["msg"] = "成功"
            return JsonResponse(ret)
    ret["code"] = 0
    ret["data"] = form_obj
    return JsonResponse(ret)


def del_crane(request, del_id):
    ret = {}
    CraneManage.objects.filter(id=del_id).delete()
    ret["code"] = 0
    ret["msg"] = "成功"
    return JsonResponse(ret)
'''

# url.py

'''
python
    url(r'^crane_list/$', crane_list),
    url(r'^crane_add/$', crane_manage),
    url(r'^crane_edit/(\d+)$', crane_manage),
    url(r'^del_crane/', del_crane),

'''
