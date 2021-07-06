from rest_framework.generics import ListAPIView
from licenses.serializers import RecipientSerializer
from licenses.models import Recipient


class RecipientList(ListAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
