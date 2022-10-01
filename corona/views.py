import mimetypes
from datetime import timedelta
from threading import Thread
from io import BytesIO
import pandas as pd
from django.core.mail import EmailMessage
from django.shortcuts import render

# Create your views here.
from django.utils.datetime_safe import datetime, date
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import  HttpResponse
from corona.covid_api_client import ApiClient
from .serializer import *


class SignupApiView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, _ = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        return user


class FetchCovidDataApiView(GenericAPIView):
    serializer_class = CountryDateSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        country_code = serializer.validated_data.get("country", None) or self.request.user.country.code
        if country_code:
            from_date = serializer.validated_data.get("from_date", None) or date.today() - timedelta(days=15)
            to_date = serializer.validated_data.get("to_date", None) or date.today()
            client = ApiClient(country=country_code)
            data = client.get_records(from_date, to_date)
            df = pd.DataFrame(data)
            bar_plot = df.plot.bar(figsize=(10, 10), x='date', y=['active', 'confirmed', 'deaths'])
            fig = bar_plot.get_figure()
            img_bytes = BytesIO()
            fig.savefig(img_bytes, format='png')
            img_name = f"media/covid_data.png"
            fig.savefig(img_name,format='png')
            with open(img_name, "rb") as f:
                return HttpResponse(f.read(), content_type="image/png")
        return Response(data={}, status=status.HTTP_200_OK)
