from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView, UpdateView
from djgeojson.views import GeoJSONLayerView

from .models import Device
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='devices_home'),
    url(r'^data.geojson/(?P<pk>\d+)$', views.DeviceGeomonitorView.as_view(model=Device, properties=('model_name, notes, id, config')), name='data'),

    url(r'^device/(?P<pk>\d+)/update$', views.DeviceUpdate.as_view(), name='device_update'),
    url(r'^device/(?P<pk>\d+)/delete$', views.DeviceDelete.as_view(), name='device_delete'),
    url(r'^device/register', views.DeviceRegister.as_view(), name='device_register'),
    url(r'^device/search', views.DeviceSearch.as_view(), name='device_search'),
    url(r'^device/select_templates', views.TemplateList.as_view(), name='devices_apply_template'),

    url(r'^device/(?P<device_id>\d+)/(?P<graph_type>[a-z]+)$', views.graph_view, name='device_graphs'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
