from rest_framework.generics import ListAPIView
from licenses.serializers import DistrictSerializer
from licenses.models import District


class DistrictList(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
