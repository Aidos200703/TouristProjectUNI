from django import forms
from .models import Destination, TourPackage, Guide, Booking, Review, Customer, Country


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'image_url', 'rating', 'price_per_day', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination name'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['title', 'destination', 'guides', 'category', 'description',
                  'duration_days', 'price', 'max_group_size',
                  'includes_hotel', 'includes_flight', 'includes_meals', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'guides': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_group_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'includes_hotel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'includes_flight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'includes_meals': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['full_name', 'photo_url', 'bio', 'languages', 'years_experience', 'specialization', 'rating', 'is_available']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English, French...'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'tour_package', 'guide', 'travel_date', 'number_of_people', 'special_requests', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'tour_package': forms.Select(attrs={'class': 'form-select'}),
            'guide': forms.Select(attrs={'class': 'form-select'}),
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tour_package', 'customer', 'rating', 'comment']
        widgets = {
            'tour_package': forms.Select(attrs={'class': 'form-select'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PublicBookingForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tour_package = forms.ModelChoiceField(
        queryset=TourPackage.objects.filter(is_available=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    guide = forms.ModelChoiceField(
        queryset=Guide.objects.filter(is_available=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    travel_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    number_of_people = forms.IntegerField(
        min_value=1, max_value=20,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
