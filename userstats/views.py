import datetime

from django.db.models import QuerySet, Sum, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema, extend_schema_view)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.models import Expense
from income.models import Income
from userstats.serializers import ExpenseSummarySerializer, IncomeSummarySerializer


class ExpenseSummaryStats(APIView):

    @extend_schema(
        tags=["UserStats"],
        responses={200: ExpenseSummarySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        todays_date: datetime.date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30 * 12)
        queryset: QuerySet = Expense.objects \
            .filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date) \
            .values('category') \
            .annotate(amount_sum=Sum('amount')).order_by()
        serializer = ExpenseSummarySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class IncomeSummaryStats(APIView):
    @extend_schema(
        tags=["UserStats"],
        responses={200: IncomeSummarySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        todays_date: datetime.date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30 * 12)
        queryset: QuerySet = Income.objects \
            .filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date) \
            .values('source') \
            .annotate(amount_sum=Sum('amount')).order_by()
        print(queryset.explain())
        serializer = IncomeSummarySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)