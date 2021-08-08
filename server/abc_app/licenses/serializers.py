from rest_framework import serializers

from licenses.models import Action, District, Status, Recipient, Admin, Report


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['code', 'description']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['code', 'description']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['code', 'description']


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'email_address', 'first_name', 'last_name']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email_address', 'first_name', 'last_name']


class ReportSerializer(serializers.ModelSerializer):
    report_type = serializers.ReadOnlyField(source='report_type_d')

    class Meta:
        model = Report
        fields = ['id',
                  'created',
                  'report_type',
                  'lic_num',
                  'status_from',
                  'status_to',
                  'status',
                  'lic_type',
                  'lic_dup',
                  'issue_date',
                  'exp_date',
                  'acct_name',
                  'acct_own',
                  'acct_street',
                  'acct_city',
                  'acct_state',
                  'acct_zip',
                  'mail_street',
                  'mail_city',
                  'mail_state',
                  'mail_zip',
                  'conditions',
                  'escrow_addr',
                  'district',
                  'trans_from',
                  'trans_to',
                  'geocode']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['status'] = StatusSerializer(instance.status).data['description']
        rep['status_from'] = StatusSerializer(instance.status_from).data['description']
        rep['status_to'] = StatusSerializer(instance.status_to).data['description']
        rep['action'] = ActionSerializer(instance.action).data['description']
        rep['district'] = DistrictSerializer(instance.district).data['description']
        return rep
