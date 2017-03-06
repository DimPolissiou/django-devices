#USELESS RULES. DELETE BEFORE RELEASE
from __future__ import absolute_import
from django_netjsonconfig.models import Config, Template
import rules
import guardian

from .models import Device

@rules.predicate
def is_config_owner(user, config):
	return user.has_perm('edit_config', config)

@rules.predicate
def is_template_owner(user, template):
	return user.has_perm('edit_template', template)

@rules.predicate
def is_device_owner(user, device):
	return user.has_perm('edit_device', device)

rules.add_perm('django_netjsonconfig', rules.always_allow)
rules.add_perm('django_netjsonconfig.change_config', is_config_owner)

