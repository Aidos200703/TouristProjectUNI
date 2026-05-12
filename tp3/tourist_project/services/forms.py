from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Destination, TourPackage, Guide, Booking, Review, Customer, Country
import re
import datetime


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers and underscores.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError('First name can only contain letters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError('Last name can only contain letters.')
        return last_name


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


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
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise ValidationError('Destination name must be at least 2 characters.')
        if len(name) > 200:
            raise ValidationError('Destination name is too long (max 200 characters).')
        return name

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0 or rating > 5:
                raise ValidationError('Rating must be between 0 and 5.')
        return rating

    def clean_price_per_day(self):
        price = self.cleaned_data.get('price_per_day')
        if price is not None:
            if price <= 0:
                raise ValidationError('Price must be greater than 0.')
            if price > 100000:
                raise ValidationError('Price seems too high. Please enter a valid amount.')
        return price

    def clean_image_url(self):
        url = self.cleaned_data.get('image_url')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            raise ValidationError('Image URL must start with http:// or https://')
        return url


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
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'max_group_size': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
            'includes_hotel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'includes_flight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'includes_meals': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError('Tour title must be at least 5 characters.')
        return title

    def clean_duration_days(self):
        days = self.cleaned_data.get('duration_days')
        if days is not None:
            if days < 1:
                raise ValidationError('Duration must be at least 1 day.')
            if days > 365:
                raise ValidationError('Duration cannot exceed 365 days.')
        return days

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None:
            if price <= 0:
                raise ValidationError('Price must be greater than 0.')
        return price

    def clean_max_group_size(self):
        size = self.cleaned_data.get('max_group_size')
        if size is not None:
            if size < 1:
                raise ValidationError('Group size must be at least 1.')
            if size > 100:
                raise ValidationError('Group size cannot exceed 100.')
        return size


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['full_name', 'photo_url', 'bio', 'languages',
                  'years_experience', 'specialization', 'rating', 'is_available']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English, French...'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '60'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if len(name) < 3:
            raise ValidationError('Full name must be at least 3 characters.')
        return name

    def clean_years_experience(self):
        years = self.cleaned_data.get('years_experience')
        if years is not None:
            if years < 0:
                raise ValidationError('Years of experience cannot be negative.')
            if years > 60:
                raise ValidationError('Years of experience seems too high.')
        return years

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0 or rating > 5:
                raise ValidationError('Rating must be between 0 and 5.')
        return rating


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1-555-000-0000'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not cleaned.isdigit():
            raise ValidationError('Phone number can only contain digits, spaces, dashes and parentheses.')
        if len(cleaned) < 7 or len(cleaned) > 15:
            raise ValidationError('Phone number must be between 7 and 15 digits.')
        return phone

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if len(name) < 2:
            raise ValidationError('First name must be at least 2 characters.')
        return name


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'tour_package', 'guide', 'travel_date',
                  'number_of_people', 'special_requests', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'tour_package': forms.Select(attrs={'class': 'form-select'}),
            'guide': forms.Select(attrs={'class': 'form-select'}),
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_travel_date(self):
        date = self.cleaned_data.get('travel_date')
        if date and date < datetime.date.today():
            raise ValidationError('Travel date cannot be in the past.')
        return date

    def clean_number_of_people(self):
        num = self.cleaned_data.get('number_of_people')
        if num is not None:
            if num < 1:
                raise ValidationError('At least 1 person is required.')
            if num > 50:
                raise ValidationError('Maximum 50 people per booking.')
        return num


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

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 1 or rating > 5:
                raise ValidationError('Rating must be between 1 and 5.')
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise ValidationError('Comment must be at least 10 characters long.')
        if len(comment) > 2000:
            raise ValidationError('Comment is too long (max 2000 characters).')
        return comment


class PublicBookingForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1-555-000-0000'})
    )
    tour_package = forms.ModelChoiceField(
        queryset=TourPackage.objects.filter(is_available=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    guide = forms.ModelChoiceField(
        queryset=Guide.objects.filter(is_available=True),
        required=False,
        empty_label='No preference',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    travel_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    number_of_people = forms.IntegerField(
        min_value=1, max_value=20,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    def clean_travel_date(self):
        date = self.cleaned_data.get('travel_date')
        if date and date < datetime.date.today():
            raise ValidationError('Travel date cannot be in the past.')
        if date and date > datetime.date.today().replace(year=datetime.date.today().year + 2):
            raise ValidationError('Travel date cannot be more than 2 years in the future.')
        return date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not cleaned.isdigit():
            raise ValidationError('Phone number is not valid.')
        if len(cleaned) < 7 or len(cleaned) > 15:
            raise ValidationError('Phone must be 7-15 digits.')
        return phone

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if len(name) < 2:
            raise ValidationError('First name must be at least 2 characters.')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Please enter a valid email address.')
        return email
