from rest_framework import serializers
from django.contrib.gis.geos import Point


class LocationSerializer(serializers.Serializer):
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)

    def point(self):
        return Point(self.data['lat'], self.data['long'], srid=4326)
