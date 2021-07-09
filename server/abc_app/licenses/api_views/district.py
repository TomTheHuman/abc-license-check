from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from licenses.serializers import DistrictSerializer
from licenses.models import District


# PAGINATION

class DistrictPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


class DistrictList(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    # PAGINATION
    pagination_class = DistrictPagination


class DistrictCreate(CreateAPIView):
    serializer_class = DistrictSerializer

    def create(self, request, *args, **kargs):
        try:
            code = request.data.get('code')
            descripton = request.data.get('description')
            errors = {}

            if len(code) < 1:
                errors['code'] = 'Code cannot be blank!'
            if len(descripton) < 1:
                errors['description'] = 'Description cannot be blank!'
            if len(errors) > 0:
                raise ValidationError(errors)

        except ValueError:
            raise ValidationError(
                {'code': 'A valid code is required.', 'description': 'A valid description is required.'})

        return super().create(request, *args, **kargs)
