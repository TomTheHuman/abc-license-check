from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from licenses.serializers import ReportSerializer
from licenses.models import Report

# TODO Add methods for listing reports by type

# PAGINATION


class ReportPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


class ReportList(ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    # PAGINATION
    pagination_class = ReportPagination


class ReportCreate(CreateAPIView):
    serializer_class = ReportSerializer

    def create(self, request, *args, **kargs):
        try:
            lic_num = request.data.get('lic_num')
            status_from = request.data.get('status_from')
            status_to = request.data.get('status_to')
            errors = {}

            if len(lic_num) < 1:
                errors['lic_num'] = 'License number cannot be blank!'

            # TODO Check if to date is after from date
            # if len(status_from) < 1:
            #     errors['status_from'] = 'Status-From cannot be blank!'
            # if len(status_to) < 1:
            #     errors['status_to'] = 'Status-To cannot be blank!'

            if len(errors) > 0:
                raise ValidationError(errors)

        except ValueError:
            raise ValidationError(
                {'lic_num': 'A valid license number is required.'})

        return super().create(request, *args, **kargs)
