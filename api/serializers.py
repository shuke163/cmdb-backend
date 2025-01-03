# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   serializers.py    
@Contact :   shu_ke163@163.com
@Author  :   fengfeng zhao
@Desciption: 
@Modify Time      @Version
------------      --------
2025/1/3 19:21    1.0    
"""
from rest_framework import serializers
from .models import Hosts


class HostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hosts
        fields = '__all__'

    # 增加序列化字段
    # def to_representation(self, instance):
    #     ret = super(HostsSerializer, self).to_representation(instance)
    #     business = instance.business
    #     if business:
    #         ret['business'] = {'id': business.id, 'name': business.name} if business else {}
    #     # ret.update(result)
    #     return ret

    def create(self, validated_data):
        instance = Hosts.objects.create(**validated_data)
        return instance
