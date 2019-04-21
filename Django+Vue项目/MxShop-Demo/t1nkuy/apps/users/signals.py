# -*- coding: utf-8 -*-
__author__ = 'bobby'
# 在创建新用户完成时，截获signals，把保存的明文密码修改为密文

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# sender 接收User的model ----对数据库操作的信号；post_save是在model的save()之后，pre_save是在model的save()之前
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 新建的时候才修改用户
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()

# 要在apps.py 进行配置
#     from django.apps import AppConfig
#
#     class UsersConfig(AppConfig):
#         name = 'users'
#         verbose_name = "用户管理"
#
#         def ready(self):
#             import users.signals
