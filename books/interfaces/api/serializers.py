from rest_framework import serializers

# REQUEST


class CreateBookRequest(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    published_date = serializers.DateField(required=False)
    genre = serializers.CharField(max_length=100, required=False)
    price = serializers.FloatField(required=False)


class UpdateBookRequest(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    author = serializers.CharField(max_length=255, required=False)
    published_date = serializers.DateField(required=False)
    genre = serializers.CharField(max_length=100, required=False)
    price = serializers.FloatField(required=False)


class GetAveragePriceRequest(serializers.Serializer):
    year = serializers.IntegerField(min_value=1900, max_value=2100)


# RESPONSE


class BookResponse(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    author = serializers.CharField()
    published_date = serializers.DateField()
    genre = serializers.CharField()
    price = serializers.FloatField()


class PaginatedBookResponse(serializers.Serializer):
    count = serializers.IntegerField()
    page_size = serializers.IntegerField()
    current_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = BookResponse(many=True)


class CreateBookResponse(BookResponse): ...


class UpdateBookResponse(BookResponse): ...


class GetAveragePriceResponse(serializers.Serializer):
    average_price = serializers.FloatField()


class ErrorResponse(serializers.Serializer):
    detail = serializers.CharField()
