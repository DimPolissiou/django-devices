from django.forms import Form, ModelForm, CharField, UUIDField, Textarea
from django.db import models
#from leaflet.admin import LeafletGeoAdminMixin
from leaflet.forms.fields import PointField
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.forms.widgets import NullBooleanSelect
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from leaflet.forms.widgets import LeafletWidget

from django_netjsonconfig.models import Config

from .models import Device

class CustomizedLeafletWidget(LeafletWidget):
	geom_type = 'POINT'
	map_template = 'leaflet/admin/widget.html'
	map_width = '100%'
	map_height = '400px'
	display_raw = False
	include_media = True
	settings_overrides = {}

class DeviceUpdateForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(DeviceUpdateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
		self.helper.add_input(Button('delete', 'Delete', css_class='btn btn-danger', onclick='window.location.href="{}"'.format('delete')))

	class Meta:
		model = Device
		exclude = ['config', 'owner']
		widgets = {'geom' : CustomizedLeafletWidget(), 'notes' : Textarea(attrs={'rows': 2, 'cols': 40})}

class DeviceRegisterForm(DeviceUpdateForm):
	config_uuid = UUIDField()
	field_order = ['config_uuid']

	def clean_config_uuid(self):
		config_uuid = self.cleaned_data['config_uuid']
		if Config.objects.filter(id=config_uuid).exists() == False:
			raise ValidationError('UUID does not correspond to a valid device configuration')
		return config_uuid

	def __init__(self, *args, **kwargs):
		super(DeviceRegisterForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

class DeviceSearchForm(ModelForm):

	class Meta:
		model = Device
		exclude = ['config', 'notes', 'is_indoor', 'geom', 'owner']
