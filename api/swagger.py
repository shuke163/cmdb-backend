#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   swagger.py    
@Contact :   shu_ke163@163.com
@Author  :   fengfeng zhao
@Desciption: 
@Modify Time      @Version
------------      --------
2025/4/16 18:22    1.0    
"""

from drf_yasg import openapi


# 定义了 Array 和 Object 的简写
def Schema_array(schema: openapi.Schema) -> openapi.Schema:  # 这是将一个 element 转为 Array[element] 的函数
    return openapi.Schema(type=openapi.TYPE_ARRAY, items=schema)


def Schema_object(*props: dict) -> openapi.Schema:
    result_properties = {}
    for prop in props:
        result_properties = {**prop, **result_properties}  # 将两个 Dict 合为一个 Dict
    return openapi.Schema(type=openapi.TYPE_OBJECT, properties=result_properties)


Schema_None = None
Schema_id = {"id": openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, description='id')}
Schema_email = {"email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='邮箱')}
Schema_password = {"password": openapi.Schema(type=openapi.TYPE_STRING, description='密码')}

Schema_title = {"title": openapi.Schema(type=openapi.TYPE_STRING, description='沙龙标题')}
Schema_datetime = {
    "datetime": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="日期时间")}
Schema_location = {"location": openapi.Schema(type=openapi.TYPE_STRING, description='地点')}
Schema_presenter_ids = {"presenter": Schema_array(Schema_object(Schema_id))}
