from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from licenses.serializers import AdminSerializer
from licenses.models import Admin


# PAGINATION

class AdminPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


class AdminList(ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    # PAGINATION
    pagination_class = AdminPagination


class AdminCreate(CreateAPIView):
    serializer_class = AdminSerializer

    def create(self, request, *args, **kargs):
        try:
            email_address = request.data.get('email_address')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            errors = {}

            if len(email_address) < 1:
                errors['email_address'] = 'Email address cannot be blank!'
            if len(first_name) < 1:
                errors['first_name'] = 'First name cannot be blank!'
            if len(last_name) < 1:
                errors['last_name'] = 'Last name cannot be blank!'
            if len(errors) > 0:
                raise ValidationError(errors)

        except ValueError:
            raise ValidationError({'email_address': 'A valid email address is required.',
                                  'first_name': 'A valid first name is required.',
                                   'last_name': 'A valid last name is required.'})

        return super().create(request, *args, **kargs)

class AdminRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.all()
    lookup_field = 'id'
    serializer_class = AdminSerializer

    def delete(self, request, *args, **kargs):
        admin_id = request.data.get("id")
        response = super().delete(request, *args, **kargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('admin_data_{}'.format(admin_id))
        return response

    def update(self, request, *args, **kargs):
        response = super().update(request, *args, **kargs)
        if response.status_code == 200:
            from django.core.cache import cache
            admin = response.data
            cache.set('admin_data_{}'.format(admin['id']), {
                'email_address': admin['email_address'],
                'first_name': admin['first_name'],
                'last_name': admin['last_name'],
            })
        return response
