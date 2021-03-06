# -*- coding: utf-8 -*-
"""
Household model.
"""
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField


class Household(models.Model):
    """
    Household model.
    """

    hh_id = models.IntegerField(unique=True)
    geom = models.PointField(srid=4326)
    bgeom = models.PolygonField(srid=4326, null=True, blank=True)
    location = models.ForeignKey(
        "Location", default=1, on_delete=models.CASCADE
    )
    rhc = models.ForeignKey(
        "Location",
        db_index=True,
        null=True,
        related_name="household_rhc_set",
        on_delete=models.CASCADE,
    )
    district = models.ForeignKey(
        "Location",
        db_index=True,
        null=True,
        related_name="houshold_district_set",
        on_delete=models.CASCADE,
    )
    data = JSONField(default=dict)
    visited = models.NullBooleanField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    sprayable = models.NullBooleanField(null=True)

    class Meta:
        app_label = "main"

    def __str__(self):
        return str(self.hh_id)

    @classmethod
    def by_osmid(cls, osmid):
        """Return a houshold object with the matching osmid for hh_id."""
        try:
            return cls.objects.get(hh_id=osmid)
        except cls.DoesNotExist:
            return None

    def _set_parent_locations(self):
        if self.location:
            if self.rhc != self.location.parent:  # pylint: disable=no-member
                self.rhc = self.location.parent  # pylint: disable=no-member
            if self.district != self.rhc.parent:  # pylint: disable=no-member
                self.district = self.rhc.parent  # pylint: disable=no-member

    # pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        self._set_parent_locations()

        return super(Household, self).save(*args, **kwargs)


# Auto-generated `LayerMapping` dictionary for Household model
household_mapping = {  # pylint: disable=C0103
    "hh_id": "OBJECTID",
    "geom": "POINT",
}
