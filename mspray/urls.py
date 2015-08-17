from mspray.apps.main.views import (
    target_area, household, household_buffer, sprayday, indicators, districts
)

from django.conf import settings
from django.conf.urls import patterns, include, url, static
from rest_framework import routers
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'buffers', household_buffer.HouseholdBufferViewSet)
router.register(r'districts', districts.DistrictViewSet, 'district')
router.register(r'households', household.HouseholdViewSet)
router.register(r'spraydays', sprayday.SprayDayViewSet)
router.register(r'targetareas', target_area.TargetAreaViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mspray.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'indicators/number_of_households',
        indicators.NumberOfHouseholdsIndicatorView.as_view(),
        name='number_of_housesholds'),
    url(r'^madagascar/', include('mspray.apps.madagascar.urls',
                                 namespace='madagascar')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^performance/district',
        'mspray.apps.main.views.performance.district'),
    url(r'^performance/team-leader',
        'mspray.apps.main.views.performance.team_leader'),
    url(r'^definitions-and-conditions',
        'mspray.apps.main.views.performance.definitions_and_conditions'),
) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
