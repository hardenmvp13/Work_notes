'''
不存在就创建，存在就更新

```python
RoleHistory.objects.update_or_create(role_id=role.id, modified_name=user.username)
```

创建

```python
RoleHistory.objects.create(role_id=role.id, modified_name=user.username).save()
```

更新

```python
RoleHistory.objects.filter(role_id=role.id).upadate(modified_name=user.username)
```

删除

```python
RoleHistory.objects.filter(role_id=role.id).delete()
```
'''