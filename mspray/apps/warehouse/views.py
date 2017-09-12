from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from mspray.apps.main.mixins import SiteNameMixin
from mspray.apps.main.models import Location
from mspray.apps.warehouse.druid import get_druid_data, process_location_data,\
    calculate_target_area_totals
from mspray.apps.main.definitions import DEFINITIONS


class Home(SiteNameMixin, TemplateView):
    template_name = 'warehouse/home.html'

    def get_queryset(self):
        return Location.objects.filter(level='district', parent=None).values(
            'id', 'name', 'structures')

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context.update(DEFINITIONS['district'])
        data, totals = get_druid_data(dimensions=[
            'target_area_id', 'target_area_name', 'target_area_structures',
            'rhc_name', 'district_name', 'district_id']
        )
        object_list = Location.objects.filter(
            level='district', parent=None).values(
            'id', 'name', 'structures', 'level')
        for district in object_list:
            district_data = [x for x in data if x['district_id'] ==
                             str(district['id'])]
            result = process_location_data(district, district_data)
            district.update(result)
        context['object_list'] = object_list
        return context


class DistrictView(SiteNameMixin, DetailView):
    template_name = 'warehouse/district.html'
    slug_field = 'pk'
    model = Location

    def get_queryset(self):
        return Location.objects.filter(level='district')

    def get_context_data(self, **kwargs):
        context = super(DistrictView, self).get_context_data(**kwargs)
        context.update(DEFINITIONS['RHC'])
        data, totals = get_druid_data(dimensions=[
            'target_area_id', 'target_area_name', 'target_area_structures',
            'rhc_name', 'district_name', 'rhc_id']
        )
        object_list = Location.objects.filter(
            level='RHC', parent=self.object).values(
            'id', 'name', 'structures', 'level')
        for rhc in object_list:
            rhc_data = [x for x in data if x['rhc_id'] == str(rhc['id'])]
            result = process_location_data(rhc, rhc_data)
            rhc.update(result)
        context['object_list'] = object_list
        return context


class RHCView(SiteNameMixin, DetailView):
    template_name = 'warehouse/rhc.html'
    slug_field = 'pk'
    model = Location

    def get_queryset(self):
        return Location.objects.filter(level='RHC')

    def get_context_data(self, **kwargs):
        context = super(RHCView, self).get_context_data(**kwargs)
        data, totals = get_druid_data(rhc_pk=self.object.pk)
        context['data'] = data
        context.update(DEFINITIONS['ta'])
        # update data with numbers of any missing target areas
        ids_present = []
        for x in data:
            try:
                ids_present.append(int(x['target_area_id']))
            except TypeError:
                pass
        missing = self.object.get_children().exclude(
            id__in=ids_present).values('name', 'structures')
        if missing:
            for m in missing:
                totals['structures'] += m['structures']
            context['missing_target_areas'] = missing
        context['totals'] = calculate_target_area_totals(totals)
        return context


class TargetAreas(SiteNameMixin, TemplateView):
    template_name = 'warehouse/spray-areas.html'

    def get_context_data(self, **kwargs):
        context = super(TargetAreas, self).get_context_data(**kwargs)
        data, totals = get_druid_data(pk=None, dimensions=[
            'target_area_id', 'target_area_name', 'target_area_structures',
            'rhc_name', 'district_name']
        )
        context['data'] = data
        context.update(DEFINITIONS['ta'])
        # update data with numbers of any missing target areas
        ids_present = []
        for x in data:
            try:
                ids_present.append(int(x['target_area_id']))
            except TypeError:
                pass
        missing = Location.objects.select_related(
            'parent').filter(level='ta').exclude(id__in=ids_present).values(
            'name', 'parent__name', 'parent__parent__name', 'structures')
        if missing:
            for m in missing:
                totals['structures'] += m['structures']
            context['missing_target_areas'] = missing
        context['totals'] = calculate_target_area_totals(totals)
        return context
