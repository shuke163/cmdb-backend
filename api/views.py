from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import HostsSerializer
from .models import Hosts
from django.db.models import Q
import ansible_runner
from pathlib import Path
from loguru import logger

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .swagger import Schema_email, Schema_password, Schema_object, Schema_None

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='User age'),
    },
    required=['name']
)


class CmdbView(APIView):
    """
    CMDB API
    """
    queryset = Hosts.objects.all().order_by('-id')
    serializer_class = HostsSerializer

    def get_queryset(self):
        """
        curl --location --request GET 'http://127.0.0.1:8000/api/v1/cmdb' \
        --header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
        --header 'Content-Type: application/json' \
        --header 'Accept: */*' \
        --header 'Host: 127.0.0.1:8000' \
        --header 'Connection: keep-alive'
        """
        queryset = self.queryset
        search = self.request.query_params.get("search", None)
        if search is not None:
            queryset = queryset.filter(Q(hostname__contains=search))
        else:
            queryset = queryset.all().order_by('-id')
        return queryset

    # @swagger_auto_schema(
    #     operation_summary='登录',
    #     operation_description='成功返回 200'
    #                           '失败（账户或密码错误）返回 401\n'
    #                           '注：一个已登录的用户 A 尝试 login 账户 B 失败后，仍具有账户 A 的凭证。',
    #     manual_parameters=[
    #         openapi.Parameter('name', openapi.IN_QUERY, description="User's name", type=openapi.TYPE_STRING),
    #         openapi.Parameter('age', openapi.IN_QUERY, description="User's age", type=openapi.TYPE_INTEGER)
    #     ],
    #     responses={200: Schema_None}
    # )
    def get(self, request):
        ser = HostsSerializer(self.get_queryset(), many=True)
        return Response({"code": status.HTTP_200_OK, "data": ser.data, "msg": "ok"})

    @swagger_auto_schema(request_body=request_schema)
    def post(self, request):
        """
        curl --location --request POST 'http://127.0.0.1:8000/api/v1/cmdb' \
        --header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
        --header 'Content-Type: application/json' \
        --header 'Accept: */*' \
        --header 'Host: 127.0.0.1:8000' \
        --header 'Connection: keep-alive' \
        --data-raw '{"hosts": ["localhost", "127.0.0.1"]}'
        """
        try:
            hosts = request.data.get('hosts')
            logger.info(f"hosts: {hosts}")

            if isinstance(hosts, list) and hosts is not None:
                for host in hosts:
                    host = str(host).strip()
                    r = ansible_runner.run(private_data_dir=Path.cwd(), host_pattern=host, limit=",".join(hosts),
                                           module='setup', quiet=True, json_mode=True)

                    data = r.get_fact_cache(host)
                    if r.status == "successful" and r.rc == 0:
                        setup_dict = {}
                        setup_dict["ansible_all_ipv4_addresses"] = data.get('ansible_default_ipv4').get("address")
                        setup_dict["macaddress"] = data.get('ansible_default_ipv4').get("macaddress")
                        setup_dict["ansible_architecture"] = data.get('ansible_architecture')
                        setup_dict["ansible_distribution"] = data.get('ansible_distribution')
                        setup_dict["ansible_distribution_major_version"] = data.get(
                            'ansible_distribution_major_version')
                        setup_dict["ansible_distribution_version"] = data.get('ansible_distribution_version')
                        setup_dict["ansible_hostname"] = data.get('ansible_hostname')
                        setup_dict["ansible_kernel_version"] = data.get('ansible_kernel_version')
                        setup_dict["ansible_machine"] = data.get('ansible_machine')
                        setup_dict["ansible_memfree_mb"] = data.get('ansible_memfree_mb')
                        setup_dict["ansible_memtotal_mb"] = data.get('ansible_memtotal_mb')
                        setup_dict["ansible_nodename"] = data.get('ansible_nodename')
                        setup_dict["ansible_os_family"] = data.get('ansible_os_family')
                        setup_dict["ansible_processor"] = data.get('ansible_processor')
                        setup_dict["ansible_processor_cores"] = data.get('ansible_processor_cores')
                        setup_dict["ansible_processor_vcpus"] = data.get('ansible_processor_vcpus')
                        setup_dict["ansible_python_version"] = data.get('ansible_python_version')
                        setup_dict["ansible_service_mgr"] = data.get('ansible_service_mgr')
                        setup_dict["ansible_product_name"] = data.get('ansible_product_name')
                        setup_dict["ansible_system"] = data.get('ansible_system')
                        setup_dict["raw_data"] = data
                        obj, created = Hosts.objects.update_or_create(hostname=host, defaults=setup_dict)

                        logger.info(f"host: {host}, data: {data}")
                        logger.info(f"The {obj.hostname} update successfully")
                    else:
                        logger.info(f"The {host} update failed")

            return Response({"code": status.HTTP_200_OK, "data": None, "msg": "ok"})
        except Exception as e:
            return Response({"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "data": None,
                             "msg": f"{e.__class__.__name__}: {str(e)}"})

    def put(self, request, pk):
        # Handle PUT request to update a resource
        # data = {'message': f'Resource {pk} updated successfully'}
        return Response(code=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Handle DELETE request to delete a resource
        data = {'message': f'Resource {pk} deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
