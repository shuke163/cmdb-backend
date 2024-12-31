from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import CMDB
import ansible_runner
import json
from loguru import logger


# Create your views here.

class CmdbView(APIView):
    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        # Handle POST data and perform actions
        hosts = request.data.get('hosts')
        logger.info(f"hosts: {hosts}")
        hosts = "localhost" if hosts is None else hosts
        r = ansible_runner.run(private_data_dir='/Users/apple/work/cmdb', host_pattern=hosts, module='setup')

        if r.status == "successful" and r.rc == 0:
            data = json.dumps(r.get_fact_cache(hosts), indent=4)
            logger.debug(f"{hosts}: setup api response: {r.status}")

        CMDB.objects.create(data=data)
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Handle PUT request to update a resource
        data = {'message': f'Resource {pk} updated successfully'}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Handle DELETE request to delete a resource
        data = {'message': f'Resource {pk} deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
