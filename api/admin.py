from django.contrib import admin
from .models import Inventory, Hosts

# Register your models here.
admin.site.site_header = "CMDB"
admin.site.index_title = "CMDB后台"


class HostsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'hostname', 'ansible_all_ipv4_addresses', 'macaddress', 'ansible_architecture', 'ansible_distribution',
        'ansible_hostname', 'ansible_machine', 'ansible_memfree_mb', 'ansible_memtotal_mb', 'ansible_nodename',
        'ansible_os_family', 'ansible_processor', 'ansible_processor_cores', 'ansible_processor_vcpus',
        'ansible_python_version', 'ansible_service_mgr', 'ansible_product_name', 'ansible_system')
    list_display_links = ("hostname", "ansible_all_ipv4_addresses")
    search_fields = ('hostname', 'ansible_all_ipv4_addresses',)
    list_per_page = 100


class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "alias", "ansible_host", "ansible_password", "ansible_user", "ansible_ssh_private_key_file", "group",
        "children")
    list_display_links = ("alias", "ansible_host")
    search_fields = ('ansible_host', 'alias',)
    list_per_page = 100


admin.site.register(Hosts, HostsAdmin)
admin.site.register(Inventory, InventoryAdmin)
