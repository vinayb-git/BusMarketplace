from sqlalchemy.orm import Session

from app.models.fleet_master import (
    AmenityMaster,
    BusClassMaster,
    BusConfigurationMaster,
    BusTypeMaster,
    FuelTypeMaster,
    ServiceCategoryMaster,
)


def seed_master_data(db: Session):

    bus_types = [
        ("SEATER", "Seater"),
        ("SLEEPER", "Sleeper"),
        ("SEATER_SLEEPER", "Seater/Sleeper"),
        ("SHUTTLE", "Shuttle"),
        ("MULTI_AXLE_SEATER", "Multi Axle Seater"),
        ("MULTI_AXLE_SLEEPER", "Multi Axle Sleeper"),
    ]

    for order, (code, name) in enumerate(bus_types, start=1):
        if not db.query(BusTypeMaster).filter_by(code=code).first():
            db.add(
                BusTypeMaster(
                    code=code,
                    name=name,
                    display_order=order,
                    is_active=True,
                )
            )

    fuel_types = [
        ("DIESEL", "Diesel"),
        ("PETROL", "Petrol"),
        ("CNG", "CNG"),
        ("ELECTRIC", "Electric"),
        ("HYBRID", "Hybrid"),
    ]

    for order, (code, name) in enumerate(fuel_types, start=1):
        if not db.query(FuelTypeMaster).filter_by(code=code).first():
            db.add(
                FuelTypeMaster(
                    code=code,
                    name=name,
                    display_order=order,
                    is_active=True,
                )
            )

    service_categories = [
        ("ORDINARY", "Ordinary"),
        ("EXPRESS", "Express"),
        ("DELUXE", "Deluxe"),
        ("LUXURY", "Luxury"),
        ("PREMIUM", "Premium"),
    ]

    for order, (code, name) in enumerate(service_categories, start=1):
        if not db.query(ServiceCategoryMaster).filter_by(code=code).first():
            db.add(
                ServiceCategoryMaster(
                    code=code,
                    name=name,
                    display_order=order,
                    is_active=True,
                )
            )

    bus_classes = [
        ("STANDARD", "Standard"),
        ("SEMI_LUXURY", "Semi Luxury"),
        ("LUXURY", "Luxury"),
        ("BUSINESS", "Business"),
        ("PREMIUM", "Premium"),
    ]

    for order, (code, name) in enumerate(bus_classes, start=1):
        if not db.query(BusClassMaster).filter_by(code=code).first():
            db.add(
                BusClassMaster(
                    code=code,
                    name=name,
                    display_order=order,
                    is_active=True,
                )
            )

    configurations = [
        ("2+2", "2+2"),
        ("2+1", "2+1"),
        ("1+1_SLEEPER", "1+1 Sleeper"),
        ("2+1_SLEEPER", "2+1 Sleeper"),
    ]

    for order, (code, name) in enumerate(configurations, start=1):
        if not db.query(BusConfigurationMaster).filter_by(code=code).first():
            db.add(
                BusConfigurationMaster(
                    code=code,
                    name=name,
                    display_order=order,
                    is_active=True,
                )
            )
    amenities = [
    ("WIFI", "WiFi"),
    ("USB_CHARGER", "USB Charger"),
    ("CHARGING_POINT", "Charging Point"),
    ("BLANKET", "Blanket"),
    ("PILLOW", "Pillow"),
    ("WATER_BOTTLE", "Water Bottle"),
    ("GPS", "GPS"),
    ("CCTV", "CCTV"),
    ("READING_LIGHT", "Reading Light"),
    ("EMERGENCY_EXIT", "Emergency Exit"),
    ("FIRE_EXTINGUISHER", "Fire Extinguisher"),
    ("LIVE_TRACKING", "Live Tracking"),
    ("TV", "TV"),
    ("SNACKS", "Snacks"),
    ]

    for order, (code, name) in enumerate(amenities, start=1):
        if not db.query(AmenityMaster).filter_by(code=code).first():
            db.add(
                AmenityMaster(
                    code=code,
                    name=name,
                    display_order=order,
                    is_active=True,
                )
            )
            
    db.commit()

    print("Master data seeded successfully.")