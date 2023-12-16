from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView
from django.db.models import Sum, F
from datetime import date, timedelta
from food.models import *
from rooms.models import *
# -------------------------------------------------------------------------------------------------------------------------------
class FoodSalesReportAPIView(APIView):
    def get(self, request):
        today = date.today()
        one_year_ago = today - timedelta(days=365)
        one_month_ago = today - timedelta(days=30)
        one_day_ago = today - timedelta(days=0)

        sales_queryset = FoodReservation.objects.filter(paid=True)

        # last month
        monthly_sales = sales_queryset.filter(created__gte=one_month_ago)
        total_monthly_sales = monthly_sales.aggregate(total_sales=Sum('food__price'))['total_sales'] or 0
        total_monthly_count = monthly_sales.aggregate(total_count=Sum('food__reserved'))['total_count'] or 0

        # last year
        yearly_sales = sales_queryset.filter(created__gte=one_year_ago)
        total_yearly_sales = yearly_sales.aggregate(total_sales=Sum('food__price'))['total_sales'] or 0
        total_yearly_count = yearly_sales.aggregate(total_count=Sum('food__reserved'))['total_count'] or 0
        

        # last day
        daily_sales = sales_queryset.filter(created__date=one_day_ago)
        total_daily_sales = daily_sales.aggregate(total_sales=Sum('food__price'))['total_sales'] or 0
        total_daily_count = daily_sales.aggregate(total_count=Sum('food__reserved'))['total_count'] or 0

        report_data = {
            'monthly_sales': total_monthly_sales,
            'monthly_count' : total_monthly_count,
            'yearly_sales': total_yearly_sales,
            'yearly_count' : total_yearly_count,
            'daily_sales': total_daily_sales,
            'daily_count' : total_daily_count,
        }

        return Response(report_data)
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
