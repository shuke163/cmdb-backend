from django.db import models


# Create your models here.


class common(models.Model):
    """
    common model
    """
    create_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Inventory(common):
    """
    ansible inventory table
    """
    id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=120, blank=True, null=True, verbose_name="host alias")
    ansible_host = models.CharField(max_length=120, blank=True, null=True, verbose_name="ansible_host")
    ansible_password = models.CharField(max_length=120, blank=True, null=True, verbose_name="ansible_password")
    ansible_user = models.CharField(max_length=120, blank=True, null=True, verbose_name="ansible_user")
    ansible_ssh_private_key_file = models.CharField(max_length=120, blank=True, null=True,
                                                    verbose_name="ansible_ssh_private_key_file")
    group = models.CharField(max_length=120, blank=True, null=False, default="ungrouped", verbose_name="group name")
    children = models.CharField(max_length=120, blank=True, null=False, verbose_name="children name")

    class Meta:
        ordering = ["alias"]
        verbose_name_plural = "ansible inventory"
        db_table = "ansible_inventory"


class Group(common):
    """
    ansible group table
    """
    group = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="a_group",
                              verbose_name="ansible_group_name")

    class Meta:
        db_table = "ansible_group"


class Hosts(common):
    """
    hosts table
    """
    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=120, blank=True, null=True, verbose_name="Hostname")
    ansible_all_ipv4_addresses = models.GenericIPAddressField(blank=True, null=True, verbose_name="ipv4_addresses")
    macaddress = models.CharField(max_length=120, blank=True, null=True, verbose_name="macaddress")
    ansible_architecture = models.CharField(max_length=12, blank=True, null=True, verbose_name="architecture")
    ansible_distribution = models.CharField(max_length=12, blank=True, null=True, verbose_name="distribution")
    ansible_distribution_major_version = models.CharField(max_length=12, blank=True, null=True,
                                                          verbose_name="major_version")
    ansible_distribution_version = models.CharField(max_length=12, blank=True, null=True,
                                                    verbose_name="distribution_version")
    ansible_hostname = models.CharField(max_length=12, blank=True, null=True, verbose_name="hostname_alias")
    ansible_kernel_version = models.CharField(max_length=12, blank=True, null=True, verbose_name="kernel_version")
    ansible_machine = models.CharField(max_length=12, blank=True, null=True, verbose_name="machine")
    ansible_memfree_mb = models.CharField(max_length=12, blank=True, null=True, verbose_name="memfree_mb")
    ansible_memtotal_mb = models.CharField(max_length=12, blank=True, null=True, verbose_name="memtotal_mb")
    ansible_nodename = models.CharField(max_length=12, blank=True, null=True, verbose_name="nodename")
    ansible_os_family = models.CharField(max_length=12, blank=True, null=True, verbose_name="os_family")
    ansible_processor = models.CharField(max_length=12, blank=True, null=True, verbose_name="processor")
    ansible_processor_cores = models.CharField(max_length=12, blank=True, null=True, verbose_name="processor_cores")
    ansible_processor_vcpus = models.CharField(max_length=12, blank=True, null=True, verbose_name="processor_vcpus")
    ansible_python_version = models.CharField(max_length=12, blank=True, null=True, verbose_name="python_version")
    ansible_service_mgr = models.CharField(max_length=12, blank=True, null=True, verbose_name="service_mgr")
    ansible_product_name = models.CharField(max_length=32, blank=True, null=True, verbose_name="product_name")
    ansible_system = models.CharField(max_length=12, blank=True, null=True, verbose_name="system")
    raw_data = models.JSONField(blank=True, verbose_name="raw_data")

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "hosts"
        db_table = "cmdb"

    # def __str__(self):
    #     return self.data
