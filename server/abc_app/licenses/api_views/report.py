from rest_framework.generics import ListAPIView
from licenses.serializers import ReportSerializer
from licenses.models import Report


class ReportList(ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
