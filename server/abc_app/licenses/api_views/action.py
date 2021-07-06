from rest_framework.generics import ListAPIView
from licenses.serializers import ActionSerializer
from licenses.models import Action


class ActionList(ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
