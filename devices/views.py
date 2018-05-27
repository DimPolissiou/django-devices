from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .forms import DeviceUpdateForm, DeviceRegisterForm, DeviceSearchForm
from .models import Device, GraphManager
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from leaflet.forms.widgets import LeafletWidget
from django_netjsonconfig.models import Config, Template
from rules.contrib.views import LoginRequiredMixin, PermissionRequiredMixin
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionListMixin
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth.models import User
from search_listview.list import SearchableListView
from django_actions.views import ActionViewMixin
from .actions import select_devices_action, apply_template_action, rebuild_graphs_action
from collectd_rest.models import Graph, GraphGroup
from .graphs import make_graphs

class IndexView(LoginRequiredMixin, TemplateView):
	template_name = 'devices/index.html'

class DeviceGeomonitorView(PermissionListMixin, GeoJSONLayerView):
	permission_required = 'devices.change_device'

	def dispatch(self, request, *args, **kwargs):
		request.user = User.objects.get(pk=kwargs['pk'])
		return super(DeviceGeomonitorView, self).dispatch(request, args, kwargs)

class DeviceRegister(LoginRequiredMixin, CreateView):
	model = Device
	form_class = DeviceRegisterForm
	template_name_suffix = '_register'

	def form_valid(self, form):
		form.instance.config = Config.objects.get(id=form.cleaned_data['config_uuid'])
		user_group = self.request.user.groups.first()
		form.instance.owner = user_group
		assign_perm('django_netjsonconfig.change_config', user_group, form.instance.config)
		assign_perm('django_netjsonconfig.delete_config', user_group, form.instance.config)
		return super(DeviceRegister, self).form_valid(form)

	def get_success_url(self, *args, **kwargs):
                return reverse("devices_home")

class DeviceUpdate(PermissionRequiredMixin, UpdateView):
	model = Device
	form_class = DeviceUpdateForm
	template_name_suffix = '_update_form'
	permission_required = 'devices.change_device'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self, *args, **kwargs):
		return reverse("devices_home")

class DeviceDelete(PermissionRequiredMixin, UpdateView):
	model = Device
	fields = []
	template_name_suffix = '_delete_form'
	permission_required = 'devices.delete_device'

	def get_success_url(self, *args, **kwargs):
		return reverse("devices_home")

class DeviceSearch(ActionViewMixin, PermissionListMixin, SearchableListView):
	permission_required = 'devices.change_device'
	actions = [select_devices_action, rebuild_graphs_action]
	model = Device
	paginate_by = 10
	template_name = "devices/device_search.html"
	searchable_fields = ["manufacturer", "model_name", "country", "city", "street", "zip_code"]
	specifications = {
		"manufacturer": "__icontains",
		"model_name": "__icontains",
	}

	def get_search_form(self):
		forms = []
		form = DeviceSearchForm
		form.prefix = Device.__name__

		initial = list(self.request.GET.lists())
		initial_tmp = {}
		for k, vals in initial:
			tmp_list = k.split(Device.__name__ + "-")
			if len(tmp_list) == 2:
				list_val_tmp = vals[0] if len(vals) == 1 else [val for val in vals if val != '']
				initial_tmp[tmp_list[-1]] = list_val_tmp

		form.initial = initial_tmp

		forms.append(form)
		return forms

class TemplateList(ActionViewMixin, PermissionListMixin, ListView):
	permission_required = 'django_netjsonconfig.change_template'
	actions = [apply_template_action]
	model = Template
	template_name = "devices/template_list.html"

def graph_view(request, device_id, graph_type):
	device = get_object_or_404(Device, pk=device_id)
	try:
		graph_manager = GraphManager.objects.get(pk=device_id)
	except GraphManager.DoesNotExist:
		make_graphs(device)
		graph_manager = get_object_or_404(GraphManager, pk=device_id)
	if (graph_type == "cpu"):
		graph_group = graph_manager.cpugraphs
	elif (graph_type == "memory"):
		graph_group = graph_manager.memorygraphs
	elif (graph_type == "interface"):
		graph_group = graph_manager.interfacegraphs
	elif (graph_type == "load"):
		graph_group = graph_manager.loadgraphs
	else:
		raise Http404
	return render(request, 'devices/device_graphs.html',
		{'device' : device, 'group' : graph_group})
