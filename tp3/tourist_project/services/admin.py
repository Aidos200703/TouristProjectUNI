from django.contrib import admin
from django.utils.html import format_html
from .models import Country, Destination, TourPackage, Guide, Customer, Booking, Review


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'continent']
    list_filter = ['continent']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'rating', 'price_per_day', 'is_featured', 'preview_image']
    list_filter = ['country', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'price_per_day', 'rating']
    ordering = ['-rating']
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'country', 'description')}),
        ('Media', {'fields': ('image_url',)}),
        ('Pricing & Rating', {'fields': ('price_per_day', 'rating', 'is_featured')}),
    )

    def preview_image(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width:60px;height:40px;object-fit:cover;border-radius:6px;" />', obj.image_url)
        return '-'
    preview_image.short_description = 'Image'


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'category', 'duration_days', 'price', 'max_group_size', 'is_available']
    list_filter = ['category', 'is_available', 'includes_hotel', 'includes_flight', 'includes_meals']
    search_fields = ['title', 'description']
    list_editable = ['price', 'is_available']
    ordering = ['price']
    filter_horizontal = ['guides']
    fieldsets = (
        ('Tour Information', {'fields': ('title', 'destination', 'category', 'description', 'guides')}),
        ('Schedule & Group', {'fields': ('duration_days', 'max_group_size', 'is_available')}),
        ('Pricing', {'fields': ('price',)}),
        ('Inclusions', {'fields': ('includes_hotel', 'includes_flight', 'includes_meals')}),
    )


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'years_experience', 'rating', 'is_available', 'preview_photo']
    list_filter = ['is_available']
    search_fields = ['full_name', 'specialization', 'languages']
    list_editable = ['is_available', 'rating']
    ordering = ['-rating']
    fieldsets = (
        ('Personal Information', {'fields': ('full_name', 'photo_url', 'bio')}),
        ('Professional Details', {'fields': ('specialization', 'years_experience', 'languages')}),
        ('Status & Rating', {'fields': ('rating', 'is_available')}),
    )

    def preview_photo(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="width:45px;height:45px;object-fit:cover;border-radius:50%;" />', obj.photo_url)
        return '-'
    preview_photo.short_description = 'Photo'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'country', 'created_at']
    list_filter = ['country']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['last_name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_ref', 'customer', 'tour_package', 'travel_date', 'number_of_people', 'total_price', 'status']
    list_filter = ['status', 'travel_date', 'tour_package']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'total_price']
    fieldsets = (
        ('Customer', {'fields': ('customer',)}),
        ('Tour Details', {'fields': ('tour_package', 'guide', 'travel_date', 'number_of_people')}),
        ('Additional Info', {'fields': ('special_requests', 'status', 'total_price', 'created_at')}),
    )

    def booking_ref(self, obj):
        ref = f"TSB{obj.id:04d}"
        return format_html('<strong style="color:#0066cc;">{}</strong>', ref)
    booking_ref.short_description = 'Ref #'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'tour_package', 'star_rating', 'short_comment', 'created_at']
    list_filter = ['rating', 'tour_package']
    search_fields = ['customer__first_name', 'customer__last_name', 'comment']
    ordering = ['-created_at']
    fieldsets = (
        ('Reviewer', {'fields': ('customer',)}),
        ('Review', {'fields': ('tour_package', 'rating', 'comment')}),
    )

    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#ffd700;font-size:1rem;">{}</span>', stars)
    star_rating.short_description = 'Rating'

    def short_comment(self, obj):
        return obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
    short_comment.short_description = 'Comment'


admin.site.site_header = 'TravelWise Admin Panel'
admin.site.site_title = 'TravelWise'
admin.site.index_title = 'Welcome to TravelWise Administration'
