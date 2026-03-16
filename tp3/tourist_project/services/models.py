from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    continent = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'


class Destination(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='destinations')
    description = models.TextField()
    image_url = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.country.name}"

    class Meta:
        ordering = ['-rating']


class Guide(models.Model):
    full_name = models.CharField(max_length=200)
    photo_url = models.URLField(blank=True)
    bio = models.TextField()
    languages = models.CharField(max_length=200)
    years_experience = models.PositiveIntegerField()
    specialization = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-rating']


class TourPackage(models.Model):
    CATEGORY_CHOICES = [
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('beach', 'Beach & Resort'),
        ('mountain', 'Mountain'),
        ('city', 'City Tour'),
        ('safari', 'Safari'),
    ]

    title = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    guides = models.ManyToManyField(Guide, related_name='tours', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_group_size = models.PositiveIntegerField(default=15)
    includes_hotel = models.BooleanField(default=True)
    includes_flight = models.BooleanField(default=False)
    includes_meals = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['price']


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    travel_date = models.DateField()
    number_of_people = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.tour_package.price * self.number_of_people
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer} - {self.tour_package.title}"

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.tour_package.title}"

    class Meta:
        ordering = ['-created_at']
