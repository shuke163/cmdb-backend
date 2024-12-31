from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Hosts
import ansible_runner
import json
from pathlib import Path
from loguru import logger


# Create your views here.

class CmdbView(APIView):
    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        try:
            hosts = request.data.get('hosts')
            logger.info(f"hosts: {hosts}")

            if isinstance(hosts, list) and hosts is not None:
                for host in hosts:
                    r = ansible_runner.run(private_data_dir=Path.cwd(), host_pattern=str(host).strip(),
                                           limit=",".join(hosts), module='setup')

                    if r.status == "successful" and r.rc == 0:
                        setup_dict = {}
                        data = r.get_fact_cache(host)
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
                        obj, created = Hosts.objects.update_or_create(hostname=str(host).strip(), defaults=setup_dict)
                        logger.info(f"The {obj.hostname} update successfully")

            return Response(data={"msg": True}, status=status.HTTP_200_OK)
        except Exception as e:
            pass

        return Response(data={"msg": False}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        # Handle PUT request to update a resource
        data = {'message': f'Resource {pk} updated successfully'}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Handle DELETE request to delete a resource
        data = {'message': f'Resource {pk} deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
