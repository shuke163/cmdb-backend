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
