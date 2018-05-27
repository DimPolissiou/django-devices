from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from . import models as device_models

from django_netjsonconfig.admin import ConfigAdmin, TemplateAdmin
from django_netjsonconfig.models import Config, Template
from guardian.admin import GuardedModelAdminMixin
from guardian.shortcuts import get_objects_for_user
from rules.contrib.admin import ObjectPermissionsModelAdminMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class DeviceAdmin(LeafletGeoAdmin):
	list_display = [field.name for field in device_models.Device._meta.fields if field.name != "id" and field.name != "geom"]

class GuardedConfigAdmin(GuardedModelAdminMixin, ObjectPermissionsModelAdminMixin, ConfigAdmin):

	def response_add(self, request, obj, post_url_continue="../%s/"):
		if not '_continue' in request.POST:
			return HttpResponseRedirect(reverse('devices_home'))
		else:
			return super(GuardedConfigAdmin, self).response_add(request, obj, post_url_continue)

	def response_change(self, request, obj):
		if not '_continue' in request.POST:
			return HttpResponseRedirect(reverse('devices_home'))
		else:
			return super(GuardedConfigAdmin, self).response_change(request, obj)

class GuardedTemplateAdmin(GuardedModelAdminMixin, ObjectPermissionsModelAdminMixin, TemplateAdmin):
	list_display = ('name', 'type', 'backend', 'created', 'modified')
	list_filter = ('backend', 'type', 'created',)
	fields = ['name',
              	'type',
              	'backend',
              	'vpn',
              	'auto_cert',
              	'config',
              	'created',
		'modified']

	def save_model(self, request, obj, form, change):
		user_group = request.user.groups.all().first()
		assign_perm('django_netjsonconfig.change_template', user_group, obj)
		assign_perm('django_netjsonconfig.delete_template', user_group, obj)
		return super(GuardedTemplateAdmin, self).save_model(request, obj, form, change)

admin.site.unregister(Config)
admin.site.register(Config, GuardedConfigAdmin)

admin.site.unregister(Template)
admin.site.register(Template, GuardedTemplateAdmin)

admin.site.register(device_models.Device, DeviceAdmin)
