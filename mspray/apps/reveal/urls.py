"""
reveal.urls module.
"""
from django.urls import path

from mspray.apps.reveal.views import add_spray_data_view

app_name = "reveal"  # pylint: disable=invalid-name

urlpatterns = [  # pylint: disable=invalid-name
    path("add-spray-data/", add_spray_data_view, name="add_spray_data")
]
