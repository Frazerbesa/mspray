from django.contrib.gis import admin

from mspray.apps.main.models.household import Household
from mspray.apps.main.models.spray_day import SprayDay
from mspray.apps.main.models.target_area import TargetArea

admin.site.register(Household, admin.GeoModelAdmin)
admin.site.register(SprayDay, admin.GeoModelAdmin)
admin.site.register(TargetArea, admin.GeoModelAdmin)
