from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from licenses.serializers import ReportSerializer
from licenses.models import Report

# TODO Only retrieve reports that match districts in territory
# PAGINATION


class ReportPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


class ReportList(ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportByTypeList(ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


    def get_queryset(self):
        type = self.kwargs['type']
        return Report.objects.filter(report_type=type)


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


class ReportRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    lookup_field = 'id'
    serializer_class = ReportSerializer

    def delete(self, request, *args, **kargs):
        report_id = request.data.get("id")
        response = super().delete(request, *args, **kargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('report_data_{}'.format(report_id))
        return response

    def update(self, request, *args, **kargs):
        response = super().update(request, *args, **kargs)
        if response.status_code == 200:
            from django.core.cache import cache
            report = response.data
            cache.set('report_data_{}'.format(report['id']), {
                'created': report['created'],
                'report_type': report['report_type'],
                'lic_num': report['lic_num'],
                'status_from': report['status_from'],
                'status_to': report['status_to'],
                'status': report['status'],
                'lic_type': report['lic_type'],
                'lic_dup': report['lic_dup'],
                'issue_date': report['issue_date'],
                'exp_date': report['exp_date'],
                'acct_name': report['acct_name'],
                'acct_own': report['acct_own'],
                'acct_street': report['acct_street'],
                'acct_city': report['acct_city'],
                'acct_state': report['acct_state'],
                'acct_zip': report['acct_zip'],
                'mail_street': report['mail_street'],
                'mail_city': report['mail_city'],
                'mail_state': report['mail_state'],
                'mail_zip': report['mail_zip'],
                'conditions': report['conditions'],
                'escrow_addr': report['escrow_addr'],
                'district': report['district'],
                'trans_from': report['trans_from'],
                'trans_to': report['trans_to'],
                'geocode': report['geocode']
            })
        return response
