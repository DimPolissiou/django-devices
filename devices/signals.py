from django_cas_ng.signals import cas_user_authenticated
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

@receiver(cas_user_authenticated)
def cas_authentication_handler(sender, **kwargs):
	if hasattr(settings, 'AFFILIATION_FIELD'):
		affiliation_field = settings.AFFILIATION_FIELD
	else:
		affiliation_field = "affiliation"
	if (affiliation_field in kwargs["attributes"]) and kwargs["attributes"][affiliation_field]:
		affiliation = kwargs["attributes"][affiliati0on_field]
	else:
		print("********************Error in authentication signal, user has no affiliation********************")
		return
	authentication_username = kwargs["user"]
	User = get_user_model()
	try:
		user = User.objects.get(username = authentication_username)
	except User.DoesNotExist:
		print("********************Error in authentication signal, user not found in database********************")
		return
	user.is_staff=True
	user.save()
	group, created = Group.objects.get_or_create(name = affiliation)
	user.groups.clear()
	user.groups.add(group)
