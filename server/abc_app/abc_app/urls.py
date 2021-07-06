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
    path('api/v1/actions', action.ActionList.as_view()),

    # API DISTRICTS
    path('api/v1/districts', district.DistrictList.as_view()),

    # API DISTRICTS
    path('api/v1/statuses', status.StatusList.as_view()),

    # API RECIPIENTS
    path('api/v1/recipients', recipient.RecipientList.as_view()),

    # API REPORTS
    path('api/v1/reports', report.ReportList.as_view()),

    # API ADMINS
    path('api/v1/admins', admins.AdminList.as_view()),
]