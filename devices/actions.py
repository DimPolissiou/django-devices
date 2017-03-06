from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django_netjsonconfig.models import Config
from .models import Device
from .graphs import make_graphs
import pickle

def select_devices_action(view, queryset):
        view.request.session['devices_queryset'] = pickle.dumps(queryset.query)
        return HttpResponseRedirect(reverse("devices_apply_template"))

def rebuild_graphs_action(view, queryset):
	for device in queryset.iterator():
		make_graphs(device)
	return HttpResponseRedirect(reverse("devices_home"))

def apply_template_action(view, queryset):
	if 'devices_queryset' not in view.request.session:
		return HttpResponseBadRequest("Session is missing the devices_queryset key.")
	devices_queryset = Device.objects.all()[:1]
	devices_queryset.query = pickle.loads(view.request.session.get('devices_queryset'))
	templates_queryset = queryset
	for device in devices_queryset.iterator():
		config = Config.objects.get(id=device.config.id)
		for template in templates_queryset.iterator():
			config.templates.add(template)
			config.save()
	return HttpResponseRedirect(reverse("devices_home"))

select_devices_action.short_description = _('Apply templates to selected devices')
apply_template_action.short_description = _('Apply selected templates')
rebuild_graphs_action.short_description = _('Rebuild graphs (fix missing graphs)')
