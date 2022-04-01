import pycountry
from rest_framework import mixins, serializers, viewsets
from rest_framework.exceptions import ValidationError as DRFValidationError

from associations import models as association_models
from banks import models as bank_models
from transaction import models as transaction_models


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = bank_models.Bank
        fields = ["id", "name", "countries"]


class BankViewSet(viewsets.ModelViewSet):
    queryset = bank_models.Bank.objects.all()
    serializer_class = BankSerializer


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transaction_models.Transaction
        fields = ["id", "program_name", "country_name", "bank_name", "currency", "is_eligible"]
        extra_kwargs = {
            'is_eligible': {'read_only': True}
        }

    def create(self, validated_data):
        is_eligible = False

        country_name = validated_data.get("country_name")

        country = pycountry.countries.get(name=country_name)
        if country_name is None or country is None:
            raise DRFValidationError(
                detail="Invalid country_name supplied"
            )

        currency = pycountry.currencies.get(alpha_3=validated_data.get("currency"))
        if currency is None:
            raise DRFValidationError(
                detail="Invalid currency supplied"
            )

        #TODO: add better currency validation check depending on country
        country_currency_check = pycountry.currencies.get(numeric=country.numeric)
        if country_currency_check is not None:
            if currency != country_currency_check:
                is_eligible = False
        else:
            # looks like there's no country-specific currency
            raise DRFValidationError(
                detail="Cannot validate currency, please fix me"
            )

        print(country_name)
        if association_models.Association.objects.filter(
                program__name=validated_data.get("program_name"),
                program__currency=validated_data.get("currency"),
                bank__name=validated_data.get("bank_name"),
                country=country_name,
                bank__countries__contains=[country_name]).exists():
            is_eligible = True

        validated_data["is_eligible"] = is_eligible
        return super().create(validated_data=validated_data)


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    model = transaction_models.Transaction
    queryset = transaction_models.Transaction.objects.all()
    serializer_class = TransactionSerializer

