from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import requests as http_requests

from .models import Destination, TourPackage, Guide, Booking, Review, Customer, Country
from .forms import (
    RegisterForm, LoginForm,
    DestinationForm, TourPackageForm, GuideForm,
    BookingForm, ReviewForm, CustomerForm, PublicBookingForm
)


# ============================================================
# TASK 1 — User Registration & Authorization
# ============================================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'services/auth/register.html', {'form': form, 'page_title': 'Register'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'services/auth/login.html', {'form': form, 'page_title': 'Login'})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'services/auth/profile.html', {'page_title': 'My Profile'})


# ============================================================
# TASK 3 — Pagination + TASK 4 — External API
# ============================================================

def home(request):
    featured_destinations = Destination.objects.filter(is_featured=True).select_related('country')[:3]
    if featured_destinations.count() < 3:
        featured_destinations = Destination.objects.select_related('country').all()[:3]
    featured_tours = TourPackage.objects.filter(is_available=True).select_related('destination__country')[:3]
    testimonials = Review.objects.select_related('tour_package', 'customer').order_by('-created_at')[:4]
    stats = {
        'destinations': Destination.objects.count() or 50,
        'tours': TourPackage.objects.count() or 120,
        'guides': Guide.objects.count() or 45,
        'happy_clients': Customer.objects.count() or 15000,
        'countries': Country.objects.count() or 35,
        'years_experience': 15,
    }
    context = {
        'featured_destinations': featured_destinations,
        'featured_tours': featured_tours,
        'testimonials': testimonials,
        'stats': stats,
        'page_title': 'Home',
    }
    return render(request, 'services/home.html', context)


def destinations(request):
    category_filter = request.GET.get('category', 'all')
    all_destinations = Destination.objects.select_related('country').all()
    if category_filter != 'all':
        all_destinations = all_destinations.filter(country__name__icontains=category_filter)
    countries = Country.objects.all()

    paginator = Paginator(all_destinations, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'destinations': page_obj,
        'page_obj': page_obj,
        'categories': countries,
        'selected_category': category_filter,
        'page_title': 'Destinations',
    }
    return render(request, 'services/destinations.html', context)


def tours(request):
    sort_by = request.GET.get('sort', 'price')
    category_filter = request.GET.get('category', 'all')
    all_tours = TourPackage.objects.filter(is_available=True).select_related('destination__country')
    if category_filter != 'all':
        all_tours = all_tours.filter(category=category_filter)
    if sort_by == 'price':
        all_tours = all_tours.order_by('price')
    elif sort_by == 'rating':
        all_tours = all_tours.order_by('-destination__rating')
    elif sort_by == 'duration':
        all_tours = all_tours.order_by('duration_days')
    categories = TourPackage.objects.values_list('category', flat=True).distinct()

    paginator = Paginator(all_tours, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tours': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_filter,
        'sort_by': sort_by,
        'page_title': 'Tour Packages',
    }
    return render(request, 'services/tours.html', context)


def guides(request):
    all_guides = Guide.objects.filter(is_available=True)

    paginator = Paginator(all_guides, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'guides': page_obj,
        'page_obj': page_obj,
        'page_title': 'Our Guides',
    }
    return render(request, 'services/guides.html', context)


def booking(request):
    success = False
    booking_data = None
    if request.method == 'POST':
        form = PublicBookingForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            tour_obj = form.cleaned_data['tour_package']
            guide_obj = form.cleaned_data.get('guide')
            travel_date = form.cleaned_data['travel_date']
            people = form.cleaned_data['number_of_people']
            requests_text = form.cleaned_data.get('special_requests', '')

            customer, _ = Customer.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'last_name': last_name, 'phone': phone}
            )
            total = tour_obj.price * people
            new_booking = Booking.objects.create(
                customer=customer,
                tour_package=tour_obj,
                guide=guide_obj,
                travel_date=travel_date,
                number_of_people=people,
                special_requests=requests_text,
                total_price=total,
                status='pending',
            )
            booking_data = {
                'full_name': f"{first_name} {last_name}",
                'email': email,
                'phone': phone,
                'tour': tour_obj.title,
                'destination': str(tour_obj.destination),
                'travel_date': travel_date,
                'people': people,
                'total_price': total,
                'booking_ref': f"TSB{new_booking.id:04d}",
            }
            success = True
        else:
            messages.error(request, 'Please fix the errors in the form.')
    else:
        form = PublicBookingForm()

    context = {
        'form': form,
        'tours': TourPackage.objects.filter(is_available=True).select_related('destination'),
        'guides': Guide.objects.filter(is_available=True),
        'success': success,
        'booking_data': booking_data,
        'page_title': 'Book a Tour',
    }
    return render(request, 'services/booking.html', context)


# ============================================================
# TASK 4 — External Open API (OpenWeatherMap + RestCountries)
# ============================================================

def weather_view(request):
    city = request.GET.get('city', 'Paris')
    weather_data = None
    country_data = None
    error_msg = None

    try:
        API_KEY = 'demo'
        weather_url = f'https://wttr.in/{city}?format=j1'
        weather_resp = http_requests.get(weather_url, timeout=5)
        if weather_resp.status_code == 200:
            data = weather_resp.json()
            current = data['current_condition'][0]
            weather_data = {
                'city': city,
                'temp_c': current['temp_C'],
                'temp_f': current['temp_F'],
                'description': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'feels_like': current['FeelsLikeC'],
                'uv_index': current['uvIndex'],
            }
    except Exception as e:
        error_msg = f'Could not fetch weather data: {str(e)}'

    try:
        country_url = f'https://restcountries.com/v3.1/name/{city}?fields=name,capital,population,currencies,languages,flags,region'
        country_resp = http_requests.get(country_url, timeout=5)
        if country_resp.status_code == 200:
            countries = country_resp.json()
            if countries:
                c = countries[0]
                currencies = list(c.get('currencies', {}).keys())
                languages = list(c.get('languages', {}).values())
                country_data = {
                    'name': c['name']['common'],
                    'capital': c.get('capital', ['N/A'])[0] if c.get('capital') else 'N/A',
                    'population': f"{c.get('population', 0):,}",
                    'currency': currencies[0] if currencies else 'N/A',
                    'language': languages[0] if languages else 'N/A',
                    'flag': c.get('flags', {}).get('png', ''),
                    'region': c.get('region', 'N/A'),
                }
    except Exception:
        pass

    popular_cities = ['Paris', 'Tokyo', 'Maldives', 'Santorini', 'Bali', 'Dubai', 'Zurich', 'Lima']

    context = {
        'city': city,
        'weather_data': weather_data,
        'country_data': country_data,
        'error_msg': error_msg,
        'popular_cities': popular_cities,
        'page_title': 'Travel Weather & Info',
    }
    return render(request, 'services/weather.html', context)


# ============================================================
# CRUD views (login_required)
# ============================================================

@login_required
def destination_list(request):
    all_items = Destination.objects.select_related('country').all()
    paginator = Paginator(all_items, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/crud/destination_list.html', {
        'items': page_obj, 'page_obj': page_obj,
        'page_title': 'Manage Destinations',
    })


@login_required
def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination created successfully!')
            return redirect('destination_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DestinationForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Destination', 'back_url': 'destination_list'
    })


@login_required
def destination_update(request, pk):
    obj = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination updated successfully!')
            return redirect('destination_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DestinationForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Destination', 'back_url': 'destination_list'
    })


@login_required
def destination_delete(request, pk):
    obj = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Destination deleted.')
        return redirect('destination_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Destination', 'back_url': 'destination_list'
    })


@login_required
def tour_list(request):
    all_items = TourPackage.objects.select_related('destination__country').all()
    paginator = Paginator(all_items, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/crud/tour_list.html', {
        'items': page_obj, 'page_obj': page_obj, 'page_title': 'Manage Tours',
    })


@login_required
def tour_create(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tour package created successfully!')
            return redirect('tour_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = TourPackageForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Tour Package', 'back_url': 'tour_list'
    })


@login_required
def tour_update(request, pk):
    obj = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tour updated successfully!')
            return redirect('tour_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = TourPackageForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Tour Package', 'back_url': 'tour_list'
    })


@login_required
def tour_delete(request, pk):
    obj = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Tour deleted.')
        return redirect('tour_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Tour Package', 'back_url': 'tour_list'
    })


@login_required
def guide_list(request):
    all_items = Guide.objects.all()
    paginator = Paginator(all_items, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/crud/guide_list.html', {
        'items': page_obj, 'page_obj': page_obj, 'page_title': 'Manage Guides',
    })


@login_required
def guide_create(request):
    if request.method == 'POST':
        form = GuideForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guide created successfully!')
            return redirect('guide_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = GuideForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Guide', 'back_url': 'guide_list'
    })


@login_required
def guide_update(request, pk):
    obj = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        form = GuideForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guide updated successfully!')
            return redirect('guide_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = GuideForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Guide', 'back_url': 'guide_list'
    })


@login_required
def guide_delete(request, pk):
    obj = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Guide deleted.')
        return redirect('guide_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Guide', 'back_url': 'guide_list'
    })


@login_required
def booking_list(request):
    all_items = Booking.objects.select_related('customer', 'tour_package', 'guide').all()
    paginator = Paginator(all_items, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/crud/booking_list.html', {
        'items': page_obj, 'page_obj': page_obj, 'page_title': 'Manage Bookings',
    })


@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking created!')
            return redirect('booking_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = BookingForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Booking', 'back_url': 'booking_list'
    })


@login_required
def booking_update(request, pk):
    obj = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated!')
            return redirect('booking_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = BookingForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Booking', 'back_url': 'booking_list'
    })


@login_required
def booking_delete(request, pk):
    obj = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Booking deleted.')
        return redirect('booking_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Booking', 'back_url': 'booking_list'
    })


@login_required
def review_list(request):
    all_items = Review.objects.select_related('customer', 'tour_package').all()
    paginator = Paginator(all_items, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/crud/review_list.html', {
        'items': page_obj, 'page_obj': page_obj, 'page_title': 'Manage Reviews',
    })


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review added!')
            return redirect('review_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ReviewForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Review', 'back_url': 'review_list'
    })


@login_required
def review_update(request, pk):
    obj = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated!')
            return redirect('review_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ReviewForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Review', 'back_url': 'review_list'
    })


@login_required
def review_delete(request, pk):
    obj = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Review deleted.')
        return redirect('review_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Review', 'back_url': 'review_list'
    })


@login_required
def customer_list(request):
    all_items = Customer.objects.select_related('country').all()
    paginator = Paginator(all_items, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/crud/customer_list.html', {
        'items': page_obj, 'page_obj': page_obj, 'page_title': 'Manage Customers',
    })


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created!')
            return redirect('customer_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomerForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Customer', 'back_url': 'customer_list'
    })


@login_required
def customer_update(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated!')
            return redirect('customer_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomerForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Customer', 'back_url': 'customer_list'
    })


@login_required
def customer_delete(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Customer deleted.')
        return redirect('customer_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Customer', 'back_url': 'customer_list'
    })

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    tours = destination.packages.filter(is_available=True)
    context = {
        'destination': destination,
        'tours': tours,
        'page_title': destination.name,
    }
    return render(request, 'services/destination_detail.html', context)


def tour_detail(request, pk):
    tour = get_object_or_404(TourPackage, pk=pk)
    reviews = tour.reviews.select_related('customer').all()
    context = {
        'tour': tour,
        'reviews': reviews,
        'page_title': tour.title,
    }
    return render(request, 'services/tour_detail.html', context)


def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    context = {
        'guide': guide,
        'page_title': guide.full_name,
    }
    return render(request, 'services/guide_detail.html', context)


def search_view(request, query=None):
    from django.db.models import Q
    if not query:
        query = request.GET.get('q', '')
    tours = TourPackage.objects.filter(
        is_available=True
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(destination__name__icontains=query)
    ).select_related('destination__country')

    destinations = Destination.objects.filter(
        Q(name__icontains=query) |
        Q(country__name__icontains=query)
    ).select_related('country')

    context = {
        'tours': tours,
        'destinations': destinations,
        'query': query,
        'page_title': f'Search: {query}',
    }
    return render(request, 'services/search_results.html', context)
