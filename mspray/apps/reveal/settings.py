"""settings for reveal app"""
from django.conf import settings

REVEAL_DATA_ID_FIELD = getattr(settings, "REVEAL_DATA_ID_FIELD", "id")
REVEAL_DATE_FIELD = getattr(settings, "REVEAL_DATE_FIELD", "date")
REVEAL_GPS_FIELD = getattr(settings, "REVEAL_GPS_FIELD", "location")
