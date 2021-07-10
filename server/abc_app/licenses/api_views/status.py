from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from licenses.serializers import StatusSerializer
from licenses.models import Status


# PAGINATION

class StatusPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


class StatusList(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    # PAGINATION
    pagination_class = StatusPagination


class StatusCreate(CreateAPIView):
    serializer_class = StatusSerializer

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

class StatusRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    lookup_field = 'code'
    serializer_class = StatusSerializer

    def delete(self, request, *args, **kargs):
        status_code = request.data.get("code")
        response = super().delete(request, *args, **kargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('status_data_{}'.format(status_code))
        return response

    def update(self, request, *args, **kargs):
        response = super().update(request, *args, **kargs)
        if response.status_code == 200:
            from django.core.cache import cache
            status = response.data
            cache.set('status_data_{}'.format(status['code']), {
                'description': status['description']
            })
        return response
