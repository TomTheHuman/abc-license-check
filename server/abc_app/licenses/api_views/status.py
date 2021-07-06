from rest_framework.generics import ListAPIView
from licenses.serializers import StatusSerializer
from licenses.models import Status


class StatusList(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
