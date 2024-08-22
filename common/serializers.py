from django.conf import settings
from rest_framework import serializers


class MediaURLSerializer(serializers.Serializer):

    def to_representation(self, instance):
        request = self.context.get('request')
        try:
            return request.build_absolute_uri(instance.file.url)
        except:
            return settings.HOST + instance.file.url
