import random
from datetime import datetime, timedelta # Not strictly needed with Faker for dates, but good to have
from django.core.management.base import BaseCommand
from faker import Faker
# Corrected model imports based on your models.py
from fire.models import Locations, Incident, FireStation, Firefighters, FireTruck, WeatherConditions

fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with sample data for the fire app, matching models.py'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        # Clear existing data (optional, be careful with this in production)
        self.stdout.write('Deleting existing data...')
        WeatherConditions.objects.all().delete()
        Incident.objects.all().delete()
        Firefighters.objects.all().delete()
        FireTruck.objects.all().delete()
        FireStation.objects.all().delete() # FireStation before Locations if Locations depend on it (not in this case)
        Locations.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))

        # Create Locations
        locations_list = []
        for i in range(15): # Create 15 locations
            location = Locations.objects.create(
                name=f"{fake.street_name()} Sector {i+1}",
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                address=fake.street_address(),
                city=fake.city(),
                country=fake.country()
            )
            locations_list.append(location)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(locations_list)} locations.'))

        # Create Fire Stations
        fire_stations_list = []
        for i in range(5): # Create 5 fire stations
            station = FireStation.objects.create(
                name=f"Station {fake.city_suffix()} {i+1}",
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                address=fake.street_address(),
                city=fake.city(),
                country=fake.country()
            )
            fire_stations_list.append(station)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(fire_stations_list)} fire stations.'))

        # Create Firefighters
        firefighters_list = []
        # Get choices directly from the model
        xp_choices = [choice[0] for choice in Firefighters.XP_CHOICES]
        # Ranks can be a custom list or also from choices if defined in model
        ranks_list = ['Probationary Firefighter', 'Firefighter I', 'Firefighter II', 'Captain', 'Battalion Chief']


        if fire_stations_list:
            for i in range(20): # Create 20 firefighters
                firefighter = Firefighters.objects.create(
                    name=fake.name(),
                    rank=random.choice(ranks_list), # Assuming rank is a free text or you have a predefined list
                    experience_level=random.choice(xp_choices),
                    station=random.choice(fire_stations_list)
                )
                firefighters_list.append(firefighter)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(firefighters_list)} firefighters.'))
        else:
            self.stdout.write(self.style.WARNING('No fire stations created, so no firefighters assigned to stations.'))

        # Create Fire Trucks
        truck_models_list = ['Pumper Engine', 'Ladder Truck', 'Tanker', 'Rescue Unit', 'Brush Truck']
        fire_trucks_list = []
        if fire_stations_list:
            for i in range(10): # Create 10 fire trucks
                truck = FireTruck.objects.create(
                    truck_number=f"TRK-{random.randint(100, 999)}{chr(random.randint(65, 90))}", # e.g., TRK-123A
                    model=random.choice(truck_models_list),
                    capacity=round(random.uniform(500.00, 3000.00), 2), # Capacity as Decimal
                    station=random.choice(fire_stations_list)
                )
                fire_trucks_list.append(truck)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(fire_trucks_list)} fire trucks.'))
        else:
            self.stdout.write(self.style.WARNING('No fire stations created, so no fire trucks assigned to stations.'))

        # Create Incidents and Weather Conditions
        # Get severity choices directly from the model
        severity_choices = [choice[0] for choice in Incident.SEVERITY_CHOICES]
        incidents_created_count = 0
        weather_created_count = 0

        if locations_list:
            for i in range(30): # Create 30 incidents
                incident_location = random.choice(locations_list)
                incident_datetime = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

                incident = Incident.objects.create(
                    location=incident_location,
                    date_time=incident_datetime,
                    severity_level=random.choice(severity_choices),
                    description=fake.sentence(nb_words=12)
                    # 'reported_by' is not in your Incident model
                )
                incidents_created_count +=1

                WeatherConditions.objects.create(
                    incident=incident,
                    temperature=round(random.uniform(-10.0, 40.0), 2),  # Celsius
                    humidity=round(random.uniform(10.0, 100.0), 2),    # Percentage
                    wind_speed=round(random.uniform(0.0, 70.0), 2),   # km/h
                    weather_description=random.choice(['Clear', 'Partly Cloudy', 'Overcast', 'Light Rain', 'Heavy Rain', 'Snow', 'Foggy', 'Windy'])
                )
                weather_created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created {incidents_created_count} incidents.'))
            self.stdout.write(self.style.SUCCESS(f'Successfully created {weather_created_count} weather conditions.'))
        else:
            self.stdout.write(self.style.WARNING('No locations available to create incidents.'))

        self.stdout.write(self.style.SUCCESS('Database population complete!'))