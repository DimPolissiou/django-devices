from django.db import models
from django_netjsonconfig.models import Config
#from django.contrib.gis.db import models as gismodels
from djgeojson.fields import PointField, PolygonField
from django.utils.translation import ugettext as _
from collectd_rest.models import  GraphGroup
from .signals import *

class Device(models.Model):
	config = models.ForeignKey(Config,
				on_delete=models.PROTECT)
				#unique=True,
				#editable=False)
	manufacturer = models.CharField(_("Manufacturer"), max_length=256, blank=True)
	model_name = models.CharField(_("Model name"), max_length=256, blank=True)
	activation_date = models.DateField(auto_now_add=True)
	is_indoor = models.NullBooleanField()

	notes =  models.TextField(_("Administration notes"), blank=True)

	country = models.CharField(_("Country"), max_length=50, blank=True)
	city = models.CharField(_("City"), max_length=50, blank=True)
	street = models.CharField(_("Street"), max_length=100, blank=True)
	zip_code = models.CharField(_("ZIP/Postal Code"), max_length=12, blank=True)

	geom = PointField(help_text=" ")

	def __unicode__(self):
		return self.model_name

class GraphManager(models.Model):
	device = models.OneToOneField(Device,
				on_delete=models.CASCADE,
				primary_key=True)
	cpugraphs = models.OneToOneField(GraphGroup, on_delete=models.CASCADE, related_name="cpu_graphmanager")
	memorygraphs = models.OneToOneField(GraphGroup, on_delete=models.CASCADE, related_name="memory_graphmanager")
	interfacegraphs = models.OneToOneField(GraphGroup, on_delete=models.CASCADE, related_name="interface_graphmanager")
	loadgraphs = models.OneToOneField(GraphGroup, on_delete=models.CASCADE, related_name="load_graphmanager")
