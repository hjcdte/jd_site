from rest_framework import serializers


class StaffSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    id_card = serializers.CharField()
    tel = serializers.CharField()