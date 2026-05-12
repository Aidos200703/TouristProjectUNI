from rest_framework import serializers
from .models import Country, Destination, Guide, TourPackage, Customer, Booking, Review


class CountrySerializer(serializers.ModelSerializer):
    destinations_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'continent', 'description', 'destinations_count']

    def get_destinations_count(self, obj):
        return obj.destinations.count()


class CountryReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'continent']
        read_only_fields = ['id', 'name', 'code', 'continent']


class DestinationSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    country_code = serializers.CharField(source='country.code', read_only=True)
    tours_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'country', 'country_name', 'country_code',
            'description', 'image_url', 'rating', 'price_per_day',
            'is_featured', 'tours_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_tours_count(self, obj):
        return obj.packages.filter(is_available=True).count()

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

    def validate_price_per_day(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class DestinationListSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Destination
        fields = ['id', 'name', 'country_name', 'rating', 'price_per_day', 'image_url', 'is_featured']
        read_only_fields = ['id', 'name', 'country_name', 'rating', 'price_per_day', 'image_url', 'is_featured']


class GuideSerializer(serializers.ModelSerializer):
    tours_count = serializers.SerializerMethodField(read_only=True)
    bookings_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Guide
        fields = [
            'id', 'full_name', 'photo_url', 'bio', 'languages',
            'years_experience', 'specialization', 'rating',
            'is_available', 'tours_count', 'bookings_count'
        ]
        read_only_fields = ['id']

    def get_tours_count(self, obj):
        return obj.tours.count()

    def get_bookings_count(self, obj):
        return obj.bookings.count()


class GuidePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ['id', 'full_name', 'photo_url', 'specialization', 'rating', 'languages', 'is_available']
        read_only_fields = ['id', 'full_name', 'photo_url', 'specialization', 'rating', 'languages', 'is_available']


class TourPackageSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_country = serializers.CharField(source='destination.country.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    reviews_count = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TourPackage
        fields = [
            'id', 'title', 'destination', 'destination_name', 'destination_country',
            'category', 'category_display', 'description', 'duration_days',
            'price', 'max_group_size', 'includes_hotel', 'includes_flight',
            'includes_meals', 'is_available', 'reviews_count', 'average_rating', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return None

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class TourPackageListSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TourPackage
        fields = ['id', 'title', 'destination_name', 'category_display', 'price', 'duration_days', 'is_available']
        read_only_fields = ['id', 'title', 'destination_name', 'category_display', 'price', 'duration_days', 'is_available']


class CustomerSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    bookings_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'country', 'country_name', 'bookings_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_bookings_count(self, obj):
        return obj.bookings.count()

    def validate_email(self, value):
        import re
        if not re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField(read_only=True)
    tour_title = serializers.CharField(source='tour_package.title', read_only=True)
    guide_name = serializers.CharField(source='guide.full_name', read_only=True)
    booking_ref = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_ref', 'customer', 'customer_name',
            'tour_package', 'tour_title', 'guide', 'guide_name',
            'travel_date', 'number_of_people', 'special_requests',
            'status', 'total_price', 'created_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at']

    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    def get_booking_ref(self, obj):
        return f"TSB{obj.id:04d}"

    def validate_travel_date(self, value):
        import datetime
        if value < datetime.date.today():
            raise serializers.ValidationError("Travel date cannot be in the past.")
        return value

    def validate_number_of_people(self, value):
        if value < 1:
            raise serializers.ValidationError("At least 1 person required.")
        if value > 50:
            raise serializers.ValidationError("Maximum 50 people per booking.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField(read_only=True)
    tour_title = serializers.CharField(source='tour_package.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'tour_package', 'tour_title', 'customer', 'customer_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_comment(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters.")
        return value