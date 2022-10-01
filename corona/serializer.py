from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from django_countries.serializer_fields import CountryField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "country", "password")


class CountryDateSerializer(serializers.Serializer):
    country = CountryField(required=False)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

    def validate(self, attrs):
        attrs = super(CountryDateSerializer, self).validate(attrs)
        if attrs.get("from_date", None) and attrs.get("to_date"):
            if attrs["from_date"] > attrs["to_date"]:
                raise ValidationError("to_date should be greated than from_date")
        return attrs
