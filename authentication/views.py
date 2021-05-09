import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db.models import QuerySet
from django.urls import reverse

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema, extend_schema_view)
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import RegisterSerializer, LoginSerializer
from authentication.utils import Util


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=["Register"],
        summary="user 등록",
        examples=[
            OpenApiExample(
                request_only=True,
                summary="sample 1",
                name="sample 1",
                value={
                    "email": "user@example.com",
                    "username": "username1",
                    "password": "password1234"
                }
            ),
            OpenApiExample(
                response_only=True,
                summary="sample 1",
                name="sample 1",
                value={
                    "username": "username1",
                    "email": "user@example.com",
                }
            ),
        ]
    )
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to verify your email \n' + abs_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        # Util.send_email(data)
        print("token : ", token)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    @extend_schema(
        tags=["Register"],
        summary="user 활성화",
        parameters=[
            OpenApiParameter(
                name="token",
                type=OpenApiTypes.STR
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        token = request.query_params.get("token", "")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            User.objects.filter(id=payload.get('user_id', 0)).update(is_verified=True)
            return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError as err:
            return Response({"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as err:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Register"],
    summary="login 하자",
    examples=[
        OpenApiExample(
            request_only=True,
            name="sample1",
            value={
                "email": "user1@example.com",
                "password": "password1234"
            }
        ),
    ]
)
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
