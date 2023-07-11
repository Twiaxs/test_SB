from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.models import Deal
from api.serializers import TopClientSerializer
import csv

class DealUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.FILES.get('deals')  
        if not file_obj:
            return Response({'status': 'Error', 'desc': 'Ошибка при обработке файла.'}, status=400)

        deals = self.parse_csv(file_obj)
        if deals is None:
            return Response({'status': 'Error', 'desc': 'Ошибка обработки данных из файла.'}, status=400)

        try:
            Deal.objects.bulk_create(deals)
        except Exception as e:
            return Response({'status': 'Error', 'desc': 'Ошибка сохранения данных в базу данных.'}, status=500)

        return Response({'status': 'OK'}, status=201)

    @staticmethod
    def parse_csv(file_obj):
        """
        Обработка файла CSV с данными сделок.

        :param file_obj: объект файла
        :return: список объектов Deal или None при ошибке обработки
        """
        try:
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            deals = []

            for row in reader:
                try:
                    aware_date = timezone.make_aware(datetime.strptime(row['date'], "%Y-%m-%d %H:%M:%S.%f"), timezone.get_current_timezone())

                    deal = Deal(
                        customer=row['customer'],
                        item=row['item'],
                        total=row['total'],
                        quantity=row['quantity'],
                        date=aware_date
                    )
                    deals.append(deal)
                except ValueError as error:
                    return None

            return deals
        except Exception as e:
            return None

    @method_decorator(cache_page(60 * 5))
    def get(self, request, format=None):
        try:
            top_clients = Deal.objects.values('customer') \
                .annotate(spent_money=Sum('total')) \
                .order_by('-spent_money')[:5]

            gem_list = Deal.objects.values('item') \
                .filter(customer__in=top_clients.values('customer')) \
                .annotate(count=Count('customer')) \
                .filter(count__gte=2) \
                .values_list('item', flat=True)

            serializer = TopClientSerializer(top_clients, many=True, context={'gem_list': gem_list})
            return Response({'response': serializer.data})
        except Exception as e:
            return Response({'status': 'Error', 'desc': 'Ошибка получения данных.'}, status=500)
