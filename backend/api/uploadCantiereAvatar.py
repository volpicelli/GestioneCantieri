#
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .articoli_serializer import Articoliserializer
from home.models import Articoli,Ordine,Cantiere
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from django.db.models import Sum
from django.conf import settings

class UploadCantiereAvatar(APIView):
    def post(self, request,cantiere_id, *args, **kwargs):
        try:
            c = Cantiere.objects.get(id=cantiere_id)
            #if not user.is_authenticated:
            #    return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            avatar = request.FILES.get('avatar')
            if not avatar:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

            # Assuming you have a UserProfile model with an avatar field
            c.avatar = avatar
            c.save()
            

            
            #user.profile.avatar.save(avatar.name, avatar)
            #user.profile.save()

            return Response({"message": "Avatar uploaded successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)