from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as csv_r

from mspray.apps.main.models import Location
from mspray.apps.main.models import SprayPoint
from mspray.apps.main.models.spray_day import DATA_ID_FIELD
from mspray.apps.main.models.spray_day import DATE_FIELD
from mspray.apps.main.models.spray_day import SprayDay
from mspray.apps.main.serializers.sprayday import SubmissionSerializer
from mspray.apps.main.serializers.sprayday import SprayDayGeoSerializer
from mspray.apps.main.serializers.sprayday import SprayDayNamibiaSerializer
from mspray.apps.main.serializers.sprayday import SprayDayShapeSerializer
from mspray.apps.main.utils import add_spray_data
from mspray.apps.main.utils import delete_cached_target_area_keys


class SprayDayViewSet(viewsets.ModelViewSet):
    """
    List of households that have been sprayed.

    Query Parameters:
    - `day` - filter list of sprayed points for a specific day
    - `target_area` - filter spray points for a specific target
    - `ordering` - you can order by day field e.g `ordering=day` or \
    `ordering=-day`
    """
    queryset = SprayDay.objects.filter()
    serializer_class = SprayDayGeoSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('spray_date',)
    ordering_fields = ('spray_date',)
    ordering = ('spray_date',)
    renderer_classes = \
        [csv_r.CSVStreamingRenderer] + api_settings.DEFAULT_RENDERER_CLASSES

    def get_serializer_class(self):
        fmt = self.request.accepted_renderer.format
        if fmt == 'csv':
            return SubmissionSerializer

        if settings.OSM_SUBMISSIONS:
            return SprayDayShapeSerializer

        if settings.SITE_NAME == 'namibia':
            return SprayDayNamibiaSerializer

        return super(SprayDayViewSet, self).get_serializer_class()

    def filter_queryset(self, queryset):
        targetid = self.request.query_params.get('target_area')

        if targetid:
            target = get_object_or_404(Location, pk=targetid)
            if False:  # settings.MSPRAY_SPATIAL_QUERIES:
                queryset = queryset.filter(geom__coveredby=target.geom)
            else:
                if target.parent is None:
                    queryset = queryset.filter(location__parent=target)
                else:
                    queryset = queryset.filter(location=target)

        if getattr(settings, 'MSPRAY_UNIQUE_FIELD', None):
            queryset = queryset.filter(
                pk__in=SprayPoint.objects.values('sprayday')
            )

        return super(SprayDayViewSet, self).filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        has_id = request.data.get(DATA_ID_FIELD)
        spray_date = request.data.get(DATE_FIELD)

        if not has_id or not spray_date:
            data = {
                "error": _("Not a valid submission: _id - %s, date - %s"
                           % (has_id, spray_date))
            }
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            try:
                sprayday = add_spray_data(request.data)
            except ValidationError as e:
                data = {"error": "%s" % e}
                status_code = status.HTTP_400_BAD_REQUEST
            except IntegrityError as e:
                data = {"error": "%s" % e}
                status_code = status.HTTP_400_BAD_REQUEST
            else:
                data = {"success": _("Successfully imported submission with"
                                     " submission id %(submission_id)s."
                                     % {'submission_id': has_id})}
                status_code = status.HTTP_201_CREATED
                delete_cached_target_area_keys(sprayday)

        return Response(data, status=status_code)

    def list(self, request, *args, **kwargs):
        if request.query_params.get('dates_only') == 'true':
            self.object_list = self.filter_queryset(self.get_queryset())
            data = self.object_list\
                .values_list('spray_date', flat=True).distinct()

            return Response(data)

        return super(SprayDayViewSet, self).list(request, *args, **kwargs)
