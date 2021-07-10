"""abc_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import licenses.views
from licenses.api_views import action, district, status, recipient, report, admins

urlpatterns = [
    path('admin/', admin.site.urls),

    # API ACTIONS
    path('api/v1/actions/', action.ActionList.as_view()),
    path('api/v1/actions/new/', action.ActionCreate.as_view()),
    path('api/v1/actions/<str:code>/', action.ActionRetrieveUpdateDestroy.as_view()),

    # API ADMINS
    path('api/v1/admins/', admins.AdminList.as_view()),
    path('api/v1/admins/new/', admins.AdminCreate.as_view()),
    path('api/v1/admins/<int:id>/', admins.AdminRetrieveUpdateDestroy.as_view()),

    # API DISTRICTS
    path('api/v1/districts/', district.DistrictList.as_view()),
    path('api/v1/districts/new/', district.DistrictCreate.as_view()),
    path('api/v1/districts/<str:code>/', district.DistrictRetrieveUpdateDestroy.as_view()),

    # API RECIPIENTS
    path('api/v1/recipients/', recipient.RecipientList.as_view()),
    path('api/v1/recipients/new/', recipient.RecipientCreate.as_view()),
    path('api/v1/recipients/<int:id>/', recipient.RecipientRetrieveUpdateDestroy.as_view()),

    # API REPORTS
    path('api/v1/reports/', report.ReportList.as_view()),
    path('api/v1/reports/new/', report.ReportCreate.as_view()),
    path('api/v1/reports/<int:id>/', report.ReportRetrieveUpdateDestroy.as_view()),
    path('api/v1/reports/<str:type>/', report.ReportByTypeList.as_view()),

    # API STATUSES
    path('api/v1/statuses/', status.StatusList.as_view()),
    path('api/v1/statuses/new/', status.StatusCreate.as_view()),
    path('api/v1/statuses/<str:code>/', status.StatusRetrieveUpdateDestroy.as_view()),
]
