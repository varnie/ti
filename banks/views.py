from rest_framework import mixins, serializers, viewsets

from banks import models
from programs import models as pmodel
import pycountry


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ["id", "name", "countries"]


class BankViewSet(viewsets.ModelViewSet):
    queryset = models.Bank.objects.all()
    serializer_class = BankSerializer


class TransactionSerializer(serializers.Serializer):
    is_eligible = serializers.BooleanField(default=True)
    bank_name =  serializers.CharField()
    program_name = serializers.CharField()
    country_name = serializers.CharField()

    def create(self, validated_data):
        country = pycountry.countries.get(name='Pakistan')
        currency = pycountry.currencies.get(numeric=country.numeric)
        pname = pmodel.Program.objects.get(name = program_name)
        print(pname) 

        pass

    def update(self, instance, validated_data):
        pass


class TransactionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        print(serializer_class.pname)
        
        pass

