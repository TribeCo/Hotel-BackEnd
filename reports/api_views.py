from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView
from django.db.models import Sum, F
from datetime import date, timedelta,datetime
from food.models import *
from rooms.models import *
from persiantools.jdatetime import JalaliDate
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
class YearChartAPIView(APIView):
    """
    GET room reservation and food sales information for chart.
    urls: domain.com/..../charts/year/
    """
    def get(self, request):
        today = JalaliDate.today()
        current_year = today.year
        jalali_start_year = current_year - 4
        jalali_end_year = current_year + 1

        reservation_queryset = RoomReservation.objects.filter(paid=True)

        sales_queryset = FoodReservation.objects.filter(paid=True)

        yearly_room_revenue = []
        yearly_food_revenue = []

        for year in range(jalali_start_year, jalali_end_year):
            jalali_start_date = JalaliDate(year, 1, 1)
            jalali_end_date = JalaliDate(year, 12, 29)

            start_date = jalali_start_date.to_gregorian()
            end_date = jalali_end_date.to_gregorian() + timedelta(days=1)

            yearly_reservation = reservation_queryset.filter(check_in__range=(start_date, end_date))
            total_yearly_room_revenue = yearly_reservation.aggregate(total_revenue=Sum(F('night_count') * F('room__type__price_one_night')))['total_revenue'] or 0

            yearly_food_reservation = sales_queryset.filter(created__range=(start_date, end_date))
            total_yearly_food_revenue = yearly_food_reservation.aggregate(total_count=Sum('food__price'))['total_count'] or 0

            yearly_room_revenue.append((year, total_yearly_room_revenue))
            yearly_food_revenue.append((year, total_yearly_food_revenue))

        report_data = {}
        room_data = {}
        food_data = {}

        for year, revenue in yearly_room_revenue:
            persian_date = f"{year}"
            room_data[persian_date] = revenue

        for year, revenue in yearly_food_revenue:
            persian_date = f"{year}"
            food_data[persian_date] = revenue   

        report_data["room"] = room_data
        report_data["food"] = food_data

        return Response(report_data)
#-----------------------------------------------------------
class MonthChartAPIView(APIView):
    """
    GET room reservation and food sales information for chart.
    urls: domain.com/..../charts/year/
    """
    def get(self, request):
        today = JalaliDate.today()
        current_year = today.year

        reservation_queryset = RoomReservation.objects.filter(paid=True)
        sales_queryset = FoodReservation.objects.filter(paid=True)

        month_room_revenue = []
        month_food_revenue = []

        for month in range(1, 13):
            jalali_start_date = JalaliDate(current_year, month, 1)
            

            start_date = jalali_start_date.to_gregorian()
            end_date = jalali_start_date.to_gregorian() + timedelta(days=29)

            yearly_reservation = reservation_queryset.filter(check_in__range=(start_date, end_date))
            total_yearly_room_revenue = yearly_reservation.aggregate(total_revenue=Sum(F('night_count') * F('room__type__price_one_night')))['total_revenue'] or 0

            yearly_food_reservation = sales_queryset.filter(created__range=(start_date, end_date))
            total_yearly_food_revenue = yearly_food_reservation.aggregate(total_count=Sum('food__price'))['total_count'] or 0

            month_room_revenue.append((self.map_month_to_jalali(month), total_yearly_room_revenue))
            month_food_revenue.append((self.map_month_to_jalali(month), total_yearly_food_revenue))

        report_data = {}
        room_data = {}
        food_data = {}

        for month, revenue in month_room_revenue:
            persian_date = f"{month}"
            room_data[persian_date] = revenue

        for month, revenue in month_food_revenue:
            persian_date = f"{month}"
            food_data[persian_date] = revenue   

        report_data["room"] = room_data
        report_data["food"] = food_data

        return Response(report_data)

    def map_month_to_jalali(self, month):
        mapping = {
            1: 'فروردین',
            2: 'اردیبهشت',
            3: 'خرداد',
            4: 'تیر',
            5: 'مرداد',
            6: 'شهریور',
            7: 'مهر',
            8: 'آبان',
            9: 'آذر',
            10: 'دی',
            11: 'بهمن',
            12: 'اسفند',
        }
        return mapping.get(month, '')

#-----------------------------------------------------------
class DayChartAPIView(APIView):
    """
    GET room reservation and food sales information for chart.
    urls: domain.com/..../charts/year/
    """
    def get(self, request):
        today = JalaliDate.today()
        year = today.year
        month = today.month

        reservation_queryset = RoomReservation.objects.filter(paid=True)
        sales_queryset = FoodReservation.objects.filter(paid=True)

        day_room_revenue = []
        day_food_revenue = []

        for day in range(1, 31):
            jalali_start_date = JalaliDate(year, month, day)
            
            start_date = jalali_start_date.to_gregorian()
            end_date = jalali_start_date.to_gregorian() + timedelta(days=1)

            day_reservation = reservation_queryset.filter(check_in__range=(start_date, end_date))
            total_day_room_revenue = day_reservation.aggregate(total_revenue=Sum(F('night_count') * F('room__type__price_one_night')))['total_revenue'] or 0

            day_food_reservation = sales_queryset.filter(created__range=(start_date, end_date))
            total_day_food_revenue = day_food_reservation.aggregate(total_count=Sum('food__price'))['total_count'] or 0

            day_room_revenue.append((day, total_day_room_revenue))
            day_food_revenue.append((day, total_day_food_revenue))

        report_data = {}
        room_data = {}
        food_data = {}

        for day, revenue in day_room_revenue:
            persian_date = f"{day}"
            room_data[persian_date] = revenue

        for day, revenue in day_food_revenue:
            persian_date = f"{day}"
            food_data[persian_date] = revenue   

        report_data["room"] = room_data
        report_data["food"] = food_data

        return Response(report_data)
#-----------------------------------------------------------
from django.db.models import Count

class FoodSalesChartAPIView(APIView):
    """
    GET food sales information in year, month, and day.
    urls: domain.com/..../reports/food/
    """

    def get(self, request):
        today = JalaliDate.today()
        tyear = today.year
        tmonth = today.month
        tday = today.day



        sales_queryset = FoodReservation.objects.filter(paid=True)

        # Top 4 best-selling foods for each year
        jalali_start_date = JalaliDate(tyear, 1, 1)
        jalali_end_date = JalaliDate(tyear, 12, 29)

        start_date = jalali_start_date.to_gregorian()
        end_date = jalali_end_date.to_gregorian() + timedelta(days=1)

        yearly_reservation = sales_queryset.filter(created__range=(start_date, end_date))
        top_selling_foods = yearly_reservation.values('food__name').annotate(sales_count=Count('food')).order_by('-sales_count')[:4]

        top_selling_foods_by_year = {}
        top_selling_foods_by_year[tyear] = list(top_selling_foods)

        # Top 4 best-selling foods for each year and month
        jalali_start_date = JalaliDate(tyear, tmonth, 1)
        jalali_end_date = JalaliDate(tyear, tmonth, 29)

        start_date = jalali_start_date.to_gregorian()
        end_date = jalali_end_date.to_gregorian() + timedelta(days=1)

        month_sales_queryset = sales_queryset.filter(created__range=(start_date, end_date))
        top_selling_foods = month_sales_queryset.values('food__name').annotate(sales_count=Count('food')).order_by('-sales_count')[:4]

        top_selling_foods_by_year_month = {}
        top_selling_foods_by_year_month[tmonth] = list(top_selling_foods)
        

        # Top 4 best-selling foods for each year, month, and day
        jalali_start_date = JalaliDate(tyear, tmonth, tday)
        jalali_end_date = JalaliDate(tyear, tmonth, tday + 1)

        start_date = jalali_start_date.to_gregorian()
        end_date = jalali_end_date.to_gregorian() + timedelta(days=1)

        day_sales_queryset = sales_queryset.filter(created__range=(start_date, end_date))
        top_selling_foods = day_sales_queryset.values('food__name').annotate(sales_count=Count('food')).order_by('-sales_count')[:4]

        top_selling_foods_by_year_month_day = {}
        top_selling_foods_by_year_month_day[tday] = list(top_selling_foods)


        report_data = {
            'top_selling_foods_by_year': top_selling_foods_by_year,
            'top_selling_foods_by_year_month': top_selling_foods_by_year_month,
            'top_selling_foods_by_year_month_day': top_selling_foods_by_year_month_day,
        }

        return Response(report_data)
#-----------------------------------------------------------