from __future__ import annotations

from django.db.models import Avg, Min, Max
from django.http import HttpRequest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DataRecord
from .serializers import DataRecordSerializer


class DataRecordListView(generics.ListAPIView):
    """GET /api/records/

    Paginated list of all records (suitable for exploration).
    Supports ordering via ?ordering=year,-value etc.
    """

    queryset = DataRecord.objects.all().order_by("id")
    serializer_class = DataRecordSerializer


class DataRecordFilterView(generics.ListAPIView):
    """GET /api/records/filter/?parameter=&region=&year=&column=

    Filter by exact matches on provided fields; any combination supported.
    """

    serializer_class = DataRecordSerializer

    def get_queryset(self):  # type: ignore[override]
        qs = DataRecord.objects.all()
        p = self.request.query_params.get("parameter")
        r = self.request.query_params.get("region")
        y = self.request.query_params.get("year")
        c = self.request.query_params.get("column")
        if p:
            qs = qs.filter(parameter=p)
        if r:
            qs = qs.filter(region=r)
        if y and y.isdigit():
            qs = qs.filter(year=int(y))
        if c:
            qs = qs.filter(column_name=c)
        return qs.order_by("parameter", "region", "year", "column_name")


class StatsView(APIView):
    """GET /api/stats/?parameter=&region=

    Returns aggregate statistics (avg, min, max) across all values for parameter+region.
    """

    def get(self, request: HttpRequest) -> Response:  # type: ignore[override]
        parameter = request.query_params.get("parameter")
        region = request.query_params.get("region")
        if not parameter or not region:
            return Response(
                {
                    "detail": "Both 'parameter' and 'region' are required query params.",
                },
                status=400,
            )
        qs = DataRecord.objects.filter(parameter=parameter, region=region)
        agg = qs.aggregate(avg=Avg("value"), min=Min("value"), max=Max("value"))
        return Response({
            "parameter": parameter,
            "region": region,
            "avg": agg["avg"],
            "min": agg["min"],
            "max": agg["max"],
            "count": qs.count(),
        })
