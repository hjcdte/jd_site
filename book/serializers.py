from rest_framework import serializers


class RoomTypeSerializer(serializers.Serializer):
    room_type = serializers.CharField()
    price = serializers.IntegerField()
    id = serializers.IntegerField()


class RoomSerializer(serializers.Serializer):
    room_type__room_type = serializers.CharField()
    room_type__price = serializers.IntegerField()
    room_num = serializers.CharField()
    id = serializers.IntegerField()


class RoomNoneSerializer(serializers.Serializer):
    max_day = serializers.CharField()
    room_num = serializers.CharField()
    room_type = serializers.CharField()
    status = serializers.CharField()
    price = serializers.IntegerField()


class BookNoneSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    room__id = serializers.IntegerField()
    room__room_num = serializers.CharField()
    room__room_type__room_type = serializers.CharField()
    name = serializers.CharField()
    tel = serializers.CharField()
    book_day = serializers.IntegerField()
    crash = serializers.IntegerField()
    max_day = serializers.CharField()


class LiveNoneSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    room__id = serializers.IntegerField()
    room__room_num = serializers.CharField()
    room__room_type__room_type = serializers.CharField()
    book_date = serializers.DateField()
    cancel_date = serializers.DateField()
    name = serializers.CharField()
    tel = serializers.CharField()
    deposit = serializers.IntegerField()
    max_day = serializers.CharField()


class CancelNoneSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    room__id = serializers.IntegerField()
    room__room_num = serializers.CharField()
    room__room_type__room_type = serializers.CharField()
    name = serializers.CharField()
    tel = serializers.CharField()
    deposit = serializers.IntegerField()
    max_day = serializers.CharField()

class BookRecordSerializer(serializers.Serializer):
    customer__name = serializers.CharField()
    room__room_num = serializers.IntegerField()
    book_date = serializers.DateField()
    cancel_date = serializers.DateField()
    room_registrant = serializers.CharField()

class MoneyTableSerializer(serializers.Serializer):
    room__room_num = serializers.IntegerField()
    crash = serializers.IntegerField()
    book_date = serializers.DateField()
    cancel_date = serializers.DateField()