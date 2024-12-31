from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import CMDB
import ansible_runner
import json
from pathlib import Path
from loguru import logger

# Create your views here.


out, err = ansible_runner.get_inventory(
    action='list',
    inventories=['/Users/apple/work/cmdb/inventory/hosts', ],
    response_format='json',
    process_isolation=False,
    # container_image='network-ee'
)
logger.info("inventory: {}".format(out))


class CmdbView(APIView):
    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        # Handle POST data and perform actions
        hosts = request.data.get('hosts')
        logger.info(f"hosts: {hosts}")

        if isinstance(hosts, list) and hosts is not None:
            for host in hosts:
                r = ansible_runner.run(private_data_dir=Path.cwd(), host_pattern=str(host).strip(),
                                       limit=",".join(hosts), module='setup')

                if r.status == "successful" and r.rc == 0:
                    obj = CMDB.objects.create(hostname=str(host).strip(), data=r.get_fact_cache(host))

            return Response(data={"msg": True}, status=status.HTTP_200_OK)
        return Response(data={"msg": True}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        # Handle PUT request to update a resource
        data = {'message': f'Resource {pk} updated successfully'}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Handle DELETE request to delete a resource
        data = {'message': f'Resource {pk} deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
