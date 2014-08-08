import gc

from django.db import connection
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.contrib.gis.utils import LayerMapping

from mspray.apps.main.models.target_area import TargetArea, targetarea_mapping
from mspray.apps.main.models.household import Household, household_mapping
from mspray.apps.main.models.spray_day import SprayDay, sprayday_mapping
from mspray.apps.main.models.households_buffer import HouseholdsBuffer


def queryset_iterator(queryset, chunksize=100):
    '''''
    Iterate over a Django Queryset.

    This method loads a maximum of chunksize (default: 100) rows in
    its memory at the same time while django normally would load all
    rows in its memory. Using the iterator() method only causes it to
    not preload all the classes.
    '''
    start = 0
    end = chunksize
    while start < queryset.count():
        for row in queryset[start:end]:
            yield row
        start += chunksize
        end += chunksize
        gc.collect()


def load_layer_mapping(model, shp_file, mapping, verbose=False, unique=None):
    lm = LayerMapping(model, shp_file, mapping, transform=False, unique=unique)
    lm.save(strict=True, verbose=verbose)


def load_area_layer_mapping(shp_file, verbose=False):
    unique = ('ranks', 'targetid')
    load_layer_mapping(TargetArea, shp_file, targetarea_mapping, verbose,
                       unique)


def load_household_layer_mapping(shp_file, verbose=False):
    unique = 'orig_fid'
    load_layer_mapping(Household, shp_file, household_mapping, verbose, unique)


def load_sprayday_layer_mapping(shp_file, verbose=False):
    load_layer_mapping(SprayDay, shp_file, sprayday_mapping, verbose)


def set_household_buffer(distance=15):
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE main_household SET bgeom = ST_GeomFromText(ST_AsText("
        "ST_Buffer(geography(geom), %s)), 4326);" % distance)


def create_households_buffer(distance=15, recreate=False):
    set_household_buffer(distance)

    if recreate:
        HouseholdsBuffer.objects.all().delete()

    for ta in queryset_iterator(TargetArea.objects.all(), 10):
        hh_buffers = Household.objects.filter(geom__coveredby=ta.geom)\
            .values_list('bgeom', flat=True)
        bf = MultiPolygon([hhb for hhb in hh_buffers])

        for b in bf.cascaded_union.simplify():
            if not isinstance(b, Polygon):
                continue
            obj, created = \
                HouseholdsBuffer.objects.get_or_create(geom=b, target_area=ta)
            obj.num_households = \
                Household.objects.filter(geom__coveredby=b).count()
            obj.save()
