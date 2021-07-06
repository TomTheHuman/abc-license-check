from rest_framework.generics import ListAPIView
from licenses.serializers import AdminSerializer
from licenses.models import Admin


class AdminList(ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
