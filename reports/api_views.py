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
#-----------------------------------------------------------
class FoodSalesReportAPIView(APIView):
    """
        GET food sales information in year,month and day.
        urls: domain.com/..../reports/food/
    """
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
        daily_sales = sales_queryset.filter(created__gte=one_day_ago)
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
#-----------------------------------------------------------
class RoomReservationReportAPIView(APIView):
    """
        GET room reservation information in year,month and day.
        urls: domain.com/..../reports/room/
    """
    def get(self, request):
        today = date.today()
        one_year_ago = today - timedelta(days=365)
        one_month_ago = today - timedelta(days=30)
        one_day_ago = today - timedelta(days=0)

        reservation_queryset = RoomReservation.objects.filter(paid=True)

        # last month
        monthly_reservation = reservation_queryset.filter(created__gte=one_month_ago)
        total_monthly_reservation = monthly_reservation.aggregate(total_reservation=Sum(F('night_count') * F('room__type__price_one_night')))['total_reservation'] or 0
        total_monthly_count = monthly_reservation.count()
        total_monthly_person = monthly_reservation.aggregate(total_person=Sum('room__type__bed_count'))['total_person'] or 0

        # last year
        yearly_reservation = reservation_queryset.filter(created__gte=one_year_ago)
        total_yearly_reservation = yearly_reservation.aggregate(total_reservation=Sum(F('night_count') * F('room__type__price_one_night')))['total_reservation'] or 0
        total_yearly_count = yearly_reservation.count()
        total_yearly_person = yearly_reservation.aggregate(total_person=Sum('room__type__bed_count'))['total_person'] or 0
        

        # last day
        daily_reservation = reservation_queryset.filter(created__gte=one_day_ago)
        total_daily_reservation = daily_reservation.aggregate(total_reservation=Sum(F('night_count') * F('room__type__price_one_night')))['total_reservation'] or 0
        total_daily_count = daily_reservation.count()
        total_daily_person = daily_reservation.aggregate(total_person=Sum('room__type__bed_count'))['total_person'] or 0

        report_data = {
            'monthly_reservation': total_monthly_reservation,
            'monthly_count' : total_monthly_count,
            'monthly_person' : total_monthly_person,

            'yearly_reservation': total_yearly_reservation,
            'yearly_count' : total_yearly_count,
            'yearly_person' : total_yearly_person,

            'daily_reservation': total_daily_reservation,
            'daily_count' : total_daily_count,
            'daily_person' : total_daily_person,
        }

        return Response(report_data)
#-----------------------------------------------------------
class AllReportAPIView(APIView):
    """
        GET room reservation and food sales information in year,month and day.
        urls: domain.com/..../reports/all/
    """
    def get(self, request):
        food_sales_report = FoodSalesReportAPIView()
        room_reservation_report = RoomReservationReportAPIView()

        food_sales_data = food_sales_report.get(request).data
        room_reservation_data = room_reservation_report.get(request).data


        report_data = {
            'food_sales': food_sales_data,
            'room_reservation': room_reservation_data
        }

        return Response(report_data)
#-----------------------------------------------------------
