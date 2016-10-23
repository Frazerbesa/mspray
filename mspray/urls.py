from mspray.apps.main.views import (
    target_area, household, household_buffer, sprayday, indicators, districts,
    spray_operator_daily, directly_observed_spraying_form
)
from mspray.apps.main.views import home
from mspray.apps.main.views import performance

from django.conf import settings
from django.conf.urls import include, url, static
from rest_framework import routers
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'buffers', household_buffer.HouseholdBufferViewSet)
router.register(r'districts', districts.DistrictViewSet, 'district')
router.register(r'households', household.HouseholdViewSet)
router.register(r'spraydays', sprayday.SprayDayViewSet)
router.register(r'targetareas', target_area.TargetAreaViewSet)

performance_urls = [
    url(r'^$', performance.DistrictPerfomanceView.as_view(),
        name="districts"),
    url(r'^team-leaders/(?P<slug>[^/]+)',
        performance.TeamLeadersPerformanceView.as_view(),
        name="team-leaders"),
    url(r'^spray-operators/(?P<slug>[^/]+)/(?P<team_leader>[^/]+)/summary',
        performance.SprayOperatorSummaryView.as_view(),
        name="spray-operator-summary"),
    url(r'^spray-operators/(?P<slug>[^/]+)/(?P<team_leader>[^/]+)/(?P<spray_operator>[^/]+)/daily',  # noqa
        performance.SprayOperatorDailyView.as_view(),
        name="spray-operator-daily"),
    url(r'^definitions-and-conditions$',
        performance.DefinitionAndConditionView.as_view(),
        name='definitions-and-conditions'),
]

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', home.DistrictView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)$', home.DistrictView.as_view(),
        name='district'),
    url(r'^(?P<district_pk>\d+)/(?P<slug>\d+)$',
        home.TargetAreaView.as_view(),
        name='target_area'),
    url(r'^sprayareas$', home.SprayAreaView.as_view()),
    url(r'indicators/number_of_households',
        indicators.NumberOfHouseholdsIndicatorView.as_view(),
        name='number_of_housesholds'),
    url(r'^performance/', include(performance_urls, namespace='performance')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^spray-operator-daily',
        spray_operator_daily.SprayOperatorDailyViewSet.as_view(
            {'post': 'create'}
        ),
        name='spray-operator-daily'),
    url(r'^directly-observed-spraying-form',
        directly_observed_spraying_form.DirectlyObservedSprayingFormViewSet.as_view(  # noqa
            {'post': 'create'}
        ),
        name='directly-observed-spraying-form'),
    url(r'^directly-observed-spraying',
        directly_observed_spraying_form.DirectlyObservedSprayingView.as_view(),
        name='directly-observed-spraying'),
    url(r'^directly-observed-spraying/(?P<district>[^/]+)',
        directly_observed_spraying_form.DirectlyObservedSprayingView.as_view(),
        name="dos-district"),
    url(r'^directly-observed-spraying/(?P<district>[^/]+)/(?P<team_leader>[^/]+)',  # noqa
        directly_observed_spraying_form.DirectlyObservedSprayingView.as_view(),
        name="dos-team-leader"),
    url(r'^directly-observed-spraying/(?P<district>[^/]+)/(?P<team_leader>[^/]+)/(?P<spray_operator>[^/]+)',  # noqa
        directly_observed_spraying_form.DirectlyObservedSprayingView.as_view(),
        name="dos-spray-operator"),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
