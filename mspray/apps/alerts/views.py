from rest_framework.decorators import api_view
from rest_framework.response import Response

from mspray.apps.alerts.tasks import health_facility_catchment_hook
from mspray.apps.alerts.tasks import so_daily_form_completion
from mspray.apps.alerts.tasks import task_send_weekly_update_email


@api_view()
def start_health_facility_catchment(request):
    health_facility_catchment_hook.delay()
    return Response({"success": True})


@api_view()
def start_send_weekly_update_email(request):
    task_send_weekly_update_email.delay()
    return Response({"success": True})


@api_view(['GET', 'POST'])
def start_so_daily_form_completion(request):
    if request.method == 'POST':
        district_code = request.data.get("district")
        tla_code = request.data.get("SO_name")
        confirmdecision = request.data.get("confirmdecisionform")
        so_daily_form_completion.delay(district_code, tla_code,
                                       confirmdecision)
    return Response({"success": True})