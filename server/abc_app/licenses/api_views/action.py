from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError


from licenses.serializers import ActionSerializer
from licenses.models import Action

# PAGINATION


class ActionPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


class ActionList(ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    # PAGINATION
    pagination_class = ActionPagination


class ActionCreate(CreateAPIView):
    serializer_class = ActionSerializer

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

class ActionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Action.objects.all()
    lookup_field = 'code'
    serializer_class = ActionSerializer

    def delete(self, request, *args, **kargs):
        action_code = request.data.get("code")
        response = super().delete(request, *args, **kargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(action_code))
        return response

    def update(self, request, *args, **kargs):
        print("Made it here")
        response = super().update(request, *args, **kargs)
        if response.status_code == 200:
            from django.core.cache import cache
            action = response.data
            cache.set('action_data_{}'.format(action['code']), {
                'description': action['description']
            })
        return response
