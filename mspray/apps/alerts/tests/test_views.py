# -*- coding: utf-8 -*-
"""Test alerts.views module."""
from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse
from django.utils.timezone import now

from mspray.apps.alerts.views import (daily_spray_effectiveness,
                                      start_health_facility_catchment,
                                      start_send_weekly_update_email,
                                      start_so_daily_form_completion)
from mspray.apps.main.models import Location, TeamLeader
from mspray.apps.main.tests.test_base import TestBase
from mspray.celery import app


@override_settings(RAPIDPRO_DAILY_SPRAY_SUCCESS_FLOW_ID="abcdef")
class TestViews(TestBase):
    """Test alerts.views module."""

    def setUp(self):
        TestBase.setUp(self)
        app.conf.update(CELERY_ALWAYS_EAGER=True)

    @patch("mspray.apps.alerts.views.health_facility_catchment_hook")
    def test_start_health_facility_catchment(self, mock):
        """
        We are testing that the start_health_facility_catchment view is working
        and that it calls the health_facility_catchment_hook task
        """
        request = self.factory.get(reverse("alerts:health_facility_catchment"))
        response = start_health_facility_catchment(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock.delay.called)

    @patch("mspray.apps.alerts.views.task_send_weekly_update_email")
    def test_start_send_weekly_update_email(self, mock):
        """
        We are testing that the start_send_weekly_update_email view is working
        and that it calls the task_send_weekly_update_email task
        """
        request = self.factory.get(reverse("alerts:send_weekly_update_email"))
        response = start_send_weekly_update_email(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock.delay.called)

    @patch("mspray.apps.alerts.views.so_daily_form_completion")
    def test_start_so_daily_form_completion(self, mock):
        """
        We want to test that the view "start_so_daily_form_completion":
            - gives a 200 reponse when POSted to
            - calles the 'so_daily_form_completion' taks with the right args
        """
        self._load_fixtures()
        district = Location.objects.filter(level="district").first()
        tla = TeamLeader.objects.first()
        post_data = {
            "district": district.code,
            "SO_name": tla.code,
            "confirmdecisionform": "No",
        }
        request = self.factory.post(
            reverse("alerts:so_daily_form_completion"), data=post_data
        )
        response = start_so_daily_form_completion(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock.delay.called)
        args, kwargs = mock.delay.call_args_list[0]
        self.assertEqual(args[0], str(district.code))
        self.assertEqual(args[1], str(tla.code))
        self.assertEqual(args[2], "No")

    @patch("mspray.apps.alerts.views.daily_spray_effectiveness_task")
    def test_daily_spray_effectiveness(self, mock_task):
        """Test trigger daily spray area spray effectiveness notifications."""
        request = self.factory.get("/daily-spray-effectiveness")
        response = daily_spray_effectiveness(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_task.delay.called)
        args, _ = mock_task.delay.call_args_list[0]
        self.assertEqual(args[0], "abcdef")
        self.assertEqual(args[1], now().date())

        request = self.factory.get(
            "/daily-spray-effectiveness", {"spray_date": "2018-11-01"}
        )
        response = daily_spray_effectiveness(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_task.delay.called)
        args, _ = mock_task.delay.call_args_list[1]
        self.assertEqual(args[0], "abcdef")
        self.assertEqual(args[1], "2018-11-01")

        self.assertEqual(
            reverse("alerts:daily_spray_effectiveness"),
            "/api/alerts/daily-spray-effectiveness",
        )
