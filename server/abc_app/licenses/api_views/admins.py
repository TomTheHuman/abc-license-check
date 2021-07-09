from rest_framework.generics import ListAPIView, CreateAPIView
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
