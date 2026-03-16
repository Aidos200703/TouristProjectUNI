from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination, TourPackage, Guide, Booking, Review, Customer, Country
from .forms import (DestinationForm, TourPackageForm, GuideForm,
                    BookingForm, ReviewForm, CustomerForm, PublicBookingForm)


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
    context = {
        'destinations': all_destinations,
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
    context = {
        'tours': all_tours,
        'categories': categories,
        'selected_category': category_filter,
        'sort_by': sort_by,
        'page_title': 'Tour Packages',
    }
    return render(request, 'services/tours.html', context)


def guides(request):
    all_guides = Guide.objects.filter(is_available=True)
    context = {
        'guides': all_guides,
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

            customer, created = Customer.objects.get_or_create(
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
                'special_requests': requests_text,
                'booking_ref': f"TSB{new_booking.id:04d}",
            }
            success = True
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


# ==================== DESTINATION CRUD ====================

def destination_list(request):
    items = Destination.objects.select_related('country').all()
    context = {'items': items, 'page_title': 'Manage Destinations', 'model_name': 'Destination'}
    return render(request, 'services/crud/destination_list.html', context)


def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Destination', 'back_url': 'destination_list'
    })


def destination_update(request, pk):
    obj = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Destination', 'back_url': 'destination_list'
    })


def destination_delete(request, pk):
    obj = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('destination_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Destination', 'back_url': 'destination_list'
    })


# ==================== TOUR PACKAGE CRUD ====================

def tour_list(request):
    items = TourPackage.objects.select_related('destination__country').all()
    context = {'items': items, 'page_title': 'Manage Tours', 'model_name': 'Tour Package'}
    return render(request, 'services/crud/tour_list.html', context)


def tour_create(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourPackageForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Tour Package', 'back_url': 'tour_list'
    })


def tour_update(request, pk):
    obj = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourPackageForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Tour Package', 'back_url': 'tour_list'
    })


def tour_delete(request, pk):
    obj = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('tour_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Tour Package', 'back_url': 'tour_list'
    })


# ==================== GUIDE CRUD ====================

def guide_list(request):
    items = Guide.objects.all()
    context = {'items': items, 'page_title': 'Manage Guides', 'model_name': 'Guide'}
    return render(request, 'services/crud/guide_list.html', context)


def guide_create(request):
    if request.method == 'POST':
        form = GuideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guide_list')
    else:
        form = GuideForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Guide', 'back_url': 'guide_list'
    })


def guide_update(request, pk):
    obj = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        form = GuideForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('guide_list')
    else:
        form = GuideForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Guide', 'back_url': 'guide_list'
    })


def guide_delete(request, pk):
    obj = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('guide_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Guide', 'back_url': 'guide_list'
    })


# ==================== BOOKING CRUD ====================

def booking_list(request):
    items = Booking.objects.select_related('customer', 'tour_package', 'guide').all()
    context = {'items': items, 'page_title': 'Manage Bookings', 'model_name': 'Booking'}
    return render(request, 'services/crud/booking_list.html', context)


def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Booking', 'back_url': 'booking_list'
    })


def booking_update(request, pk):
    obj = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Booking', 'back_url': 'booking_list'
    })


def booking_delete(request, pk):
    obj = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('booking_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Booking', 'back_url': 'booking_list'
    })


# ==================== REVIEW CRUD ====================

def review_list(request):
    items = Review.objects.select_related('customer', 'tour_package').all()
    context = {'items': items, 'page_title': 'Manage Reviews', 'model_name': 'Review'}
    return render(request, 'services/crud/review_list.html', context)


def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Review', 'back_url': 'review_list'
    })


def review_update(request, pk):
    obj = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Review', 'back_url': 'review_list'
    })


def review_delete(request, pk):
    obj = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('review_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Review', 'back_url': 'review_list'
    })


# ==================== CUSTOMER CRUD ====================

def customer_list(request):
    items = Customer.objects.select_related('country').all()
    context = {'items': items, 'page_title': 'Manage Customers', 'model_name': 'Customer'}
    return render(request, 'services/crud/customer_list.html', context)


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Add Customer', 'back_url': 'customer_list'
    })


def customer_update(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=obj)
    return render(request, 'services/crud/form.html', {
        'form': form, 'title': 'Edit Customer', 'back_url': 'customer_list'
    })


def customer_delete(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('customer_list')
    return render(request, 'services/crud/confirm_delete.html', {
        'obj': obj, 'title': 'Delete Customer', 'back_url': 'customer_list'
    })
