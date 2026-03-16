import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist_project.settings')
django.setup()

from services.models import Country, Destination, Guide, TourPackage, Customer, Booking, Review

Country.objects.all().delete()
countries_data = [
    {'name': 'Greece', 'code': 'GRC', 'continent': 'Europe', 'description': 'Mediterranean country known for history and islands.'},
    {'name': 'Japan', 'code': 'JPN', 'continent': 'Asia', 'description': 'Island nation known for technology and tradition.'},
    {'name': 'Peru', 'code': 'PER', 'continent': 'South America', 'description': 'Home of the Inca civilization.'},
    {'name': 'Tanzania', 'code': 'TZA', 'continent': 'Africa', 'description': 'Famous for Serengeti and Kilimanjaro.'},
    {'name': 'Maldives', 'code': 'MDV', 'continent': 'Asia', 'description': 'Tropical island paradise in the Indian Ocean.'},
    {'name': 'Switzerland', 'code': 'CHE', 'continent': 'Europe', 'description': 'Known for Alps, watches and chocolate.'},
    {'name': 'United States', 'code': 'USA', 'continent': 'North America', 'description': 'Diverse country with iconic landmarks.'},
    {'name': 'France', 'code': 'FRA', 'continent': 'Europe', 'description': 'Known for culture, cuisine and fashion.'},
]
country_objs = {}
for c in countries_data:
    obj = Country.objects.create(**c)
    country_objs[c['name']] = obj
print(f"Created {Country.objects.count()} countries")

Guide.objects.all().delete()
guides_data = [
    {
        'full_name': 'Alexandra Papadopoulos',
        'photo_url': 'https://randomuser.me/api/portraits/women/44.jpg',
        'bio': 'Born and raised in Athens, Alexandra has been leading tours across Greece for over 12 years. She holds a degree in Archaeology.',
        'languages': 'English, Greek, French, Spanish',
        'years_experience': 12,
        'specialization': 'Greek History & Culture',
        'rating': 4.9,
        'is_available': True,
    },
    {
        'full_name': 'Carlos Mendoza',
        'photo_url': 'https://randomuser.me/api/portraits/men/32.jpg',
        'bio': 'Carlos is a certified mountain guide with extensive knowledge of South American trails and indigenous cultures.',
        'languages': 'English, Spanish, Portuguese, Quechua',
        'years_experience': 15,
        'specialization': 'Adventure & Mountain Trekking',
        'rating': 4.8,
        'is_available': True,
    },
    {
        'full_name': 'Yuki Tanaka',
        'photo_url': 'https://randomuser.me/api/portraits/women/68.jpg',
        'bio': 'Yuki is a passionate cultural ambassador from Kyoto with deep knowledge of Japanese traditions, art, and cuisine.',
        'languages': 'English, Japanese, Mandarin, Korean',
        'years_experience': 8,
        'specialization': 'Japanese Culture & Traditions',
        'rating': 4.9,
        'is_available': True,
    },
    {
        'full_name': 'David Kimani',
        'photo_url': 'https://randomuser.me/api/portraits/men/75.jpg',
        'bio': 'David grew up near the Serengeti and has an unparalleled knowledge of African wildlife and ecosystems.',
        'languages': 'English, Swahili, French',
        'years_experience': 18,
        'specialization': 'African Wildlife & Safari',
        'rating': 4.9,
        'is_available': True,
    },
    {
        'full_name': 'Sophie Laurent',
        'photo_url': 'https://randomuser.me/api/portraits/women/23.jpg',
        'bio': 'Sophie is a certified ski instructor and mountain guide from Chamonix.',
        'languages': 'English, French, German, Italian',
        'years_experience': 10,
        'specialization': 'Alpine Sports & Mountain Tours',
        'rating': 4.7,
        'is_available': True,
    },
    {
        'full_name': 'Ahmed Hassan',
        'photo_url': 'https://randomuser.me/api/portraits/men/46.jpg',
        'bio': 'Ahmed specializes in cultural and historical tours across the Middle East and North Africa.',
        'languages': 'English, Arabic, French, Turkish',
        'years_experience': 11,
        'specialization': 'Middle Eastern History & Culture',
        'rating': 4.8,
        'is_available': True,
    },
]
guide_objs = []
for g in guides_data:
    obj = Guide.objects.create(**g)
    guide_objs.append(obj)
print(f"Created {Guide.objects.count()} guides")

Destination.objects.all().delete()
destinations_data = [
    {'name': 'Santorini', 'country': country_objs['Greece'], 'description': 'Famous for dramatic views, stunning sunsets, and white-washed houses.', 'rating': 4.9, 'price_per_day': 250, 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800'},
    {'name': 'Kyoto', 'country': country_objs['Japan'], 'description': 'Home to thousands of classical Buddhist temples and traditional wooden houses.', 'rating': 4.9, 'price_per_day': 200, 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800'},
    {'name': 'Machu Picchu', 'country': country_objs['Peru'], 'description': 'An Incan citadel set high in the Andes Mountains.', 'rating': 4.8, 'price_per_day': 180, 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=800'},
    {'name': 'Serengeti', 'country': country_objs['Tanzania'], 'description': 'Witness the Great Migration across the vast Serengeti plains.', 'rating': 4.7, 'price_per_day': 350, 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800'},
    {'name': 'Maldives', 'country': country_objs['Maldives'], 'description': 'Crystal clear lagoons, pristine beaches, and overwater bungalows.', 'rating': 4.9, 'price_per_day': 500, 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1506953823976-52e1fdc0149a?w=800'},
    {'name': 'Swiss Alps', 'country': country_objs['Switzerland'], 'description': 'Breathtaking mountain scenery with world-class skiing and hiking.', 'rating': 4.8, 'price_per_day': 300, 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800'},
]
dest_objs = {}
for d in destinations_data:
    obj = Destination.objects.create(**d)
    dest_objs[d['name']] = obj
print(f"Created {Destination.objects.count()} destinations")

TourPackage.objects.all().delete()
tours_data = [
    {'title': 'Greek Islands Adventure', 'destination': dest_objs['Santorini'], 'category': 'beach', 'description': 'Explore the stunning Greek Islands including Santorini, Mykonos, and Crete.', 'duration_days': 10, 'price': 2500, 'max_group_size': 12, 'includes_hotel': True, 'includes_flight': True, 'includes_meals': True},
    {'title': 'Japan Cultural Journey', 'destination': dest_objs['Kyoto'], 'category': 'cultural', 'description': 'Immerse yourself in Japanese culture, ancient temples, and shrines.', 'duration_days': 12, 'price': 3200, 'max_group_size': 15, 'includes_hotel': True, 'includes_flight': True, 'includes_meals': False},
    {'title': 'Inca Trail Expedition', 'destination': dest_objs['Machu Picchu'], 'category': 'adventure', 'description': 'Trek through the Andes Mountains on the legendary Inca Trail.', 'duration_days': 8, 'price': 1800, 'max_group_size': 10, 'includes_hotel': True, 'includes_flight': False, 'includes_meals': True},
    {'title': 'African Safari Experience', 'destination': dest_objs['Serengeti'], 'category': 'safari', 'description': 'Witness the spectacular Great Migration and explore the vast Serengeti.', 'duration_days': 7, 'price': 4500, 'max_group_size': 8, 'includes_hotel': True, 'includes_flight': False, 'includes_meals': True},
    {'title': 'Maldives Luxury Escape', 'destination': dest_objs['Maldives'], 'category': 'beach', 'description': 'Stay in an overwater bungalow surrounded by turquoise lagoons.', 'duration_days': 7, 'price': 5500, 'max_group_size': 4, 'includes_hotel': True, 'includes_flight': True, 'includes_meals': True},
    {'title': 'Swiss Alps Winter Tour', 'destination': dest_objs['Swiss Alps'], 'category': 'mountain', 'description': 'Experience the magic of the Swiss Alps in winter with world-class skiing.', 'duration_days': 9, 'price': 3800, 'max_group_size': 10, 'includes_hotel': True, 'includes_flight': False, 'includes_meals': True},
]
tour_objs = []
for t in tours_data:
    obj = TourPackage.objects.create(**t)
    tour_objs.append(obj)
tour_objs[0].guides.add(guide_objs[0])
tour_objs[1].guides.add(guide_objs[2])
tour_objs[2].guides.add(guide_objs[1])
tour_objs[3].guides.add(guide_objs[3])
tour_objs[4].guides.add(guide_objs[5])
tour_objs[5].guides.add(guide_objs[4])
print(f"Created {TourPackage.objects.count()} tour packages")

Customer.objects.all().delete()
customers_data = [
    {'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah@example.com', 'phone': '+1-555-0101', 'country': country_objs['United States']},
    {'first_name': 'James', 'last_name': 'Wilson', 'email': 'james@example.com', 'phone': '+44-20-0102', 'country': country_objs['France']},
    {'first_name': 'Marie', 'last_name': 'Dubois', 'email': 'marie@example.com', 'phone': '+33-1-0103', 'country': country_objs['France']},
    {'first_name': 'Michael', 'last_name': 'Chen', 'email': 'michael@example.com', 'phone': '+61-2-0104', 'country': country_objs['United States']},
    {'first_name': 'Emma', 'last_name': 'Brown', 'email': 'emma@example.com', 'phone': '+61-3-0105', 'country': country_objs['United States']},
]
customer_objs = []
for c in customers_data:
    obj = Customer.objects.create(**c)
    customer_objs.append(obj)
print(f"Created {Customer.objects.count()} customers")

Booking.objects.all().delete()
import datetime
bookings_data = [
    {'customer': customer_objs[0], 'tour_package': tour_objs[0], 'guide': guide_objs[0], 'travel_date': datetime.date(2025, 6, 15), 'number_of_people': 2, 'status': 'confirmed'},
    {'customer': customer_objs[1], 'tour_package': tour_objs[3], 'guide': guide_objs[3], 'travel_date': datetime.date(2025, 7, 20), 'number_of_people': 1, 'status': 'confirmed'},
    {'customer': customer_objs[2], 'tour_package': tour_objs[1], 'guide': guide_objs[2], 'travel_date': datetime.date(2025, 8, 10), 'number_of_people': 3, 'status': 'pending'},
    {'customer': customer_objs[3], 'tour_package': tour_objs[4], 'guide': None, 'travel_date': datetime.date(2025, 9, 5), 'number_of_people': 2, 'status': 'confirmed'},
    {'customer': customer_objs[4], 'tour_package': tour_objs[0], 'guide': guide_objs[0], 'travel_date': datetime.date(2025, 10, 1), 'number_of_people': 1, 'status': 'pending'},
]
for b in bookings_data:
    Booking.objects.create(**b)
print(f"Created {Booking.objects.count()} bookings")

Review.objects.all().delete()
reviews_data = [
    {'tour_package': tour_objs[0], 'customer': customer_objs[0], 'rating': 5, 'comment': 'Absolutely magical experience! The guide was knowledgeable and friendly. Highly recommend!'},
    {'tour_package': tour_objs[0], 'customer': customer_objs[4], 'rating': 5, 'comment': 'Santorini is breathtaking and this tour made it even more special. Will definitely book again!'},
    {'tour_package': tour_objs[2], 'customer': customer_objs[1], 'rating': 5, 'comment': 'The Inca Trail was challenging but incredibly rewarding. Views of Machu Picchu at sunrise were worth every step.'},
    {'tour_package': tour_objs[1], 'customer': customer_objs[2], 'rating': 5, 'comment': 'Japan exceeded all our expectations. Yuki was the perfect guide. We fell in love with Japanese culture!'},
    {'tour_package': tour_objs[3], 'customer': customer_objs[1], 'rating': 5, 'comment': 'David is an incredible guide. We saw the Big Five within the first two days!'},
    {'tour_package': tour_objs[4], 'customer': customer_objs[3], 'rating': 5, 'comment': 'Pure paradise! The overwater bungalow was stunning. Worth every penny!'},
]
for r in reviews_data:
    Review.objects.create(**r)
print(f"Created {Review.objects.count()} reviews")

print("\nAll data populated successfully!")
print(f"  Countries:    {Country.objects.count()}")
print(f"  Destinations: {Destination.objects.count()}")
print(f"  Guides:       {Guide.objects.count()}")
print(f"  Tours:        {TourPackage.objects.count()}")
print(f"  Customers:    {Customer.objects.count()}")
print(f"  Bookings:     {Booking.objects.count()}")
print(f"  Reviews:      {Review.objects.count()}")
