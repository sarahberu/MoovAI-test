from typing import Any

from faker import Faker

fake = Faker("en_CA")  # Canadian locale

# Static pool of 20 realistic reviews — Faker picks a random subset each call
REVIEW_POOL = [
    "The sleep tracking on this ring is incredibly accurate. It's changed how I approach my recovery.",
    "Great device but the subscription feels like a cash grab after paying $430 already.",
    "Comfortable enough to wear 24/7. Battery lasts about 5 days with my usage.",
    "Best fitness tracker I've owned. The readiness score actually helps me plan my workouts.",
    "Build quality is exceptional. Titanium feels premium and it's survived everything I've thrown at it.",
    "The app is intuitive but the monthly fee is a dealbreaker for some. I think it's worth it.",
    "Ordered from Amazon.ca, arrived quickly and well packaged. No sizing issues with the sizing kit.",
    "Compared to my previous Fitbit, the Oura Ring data depth is in a different league.",
    "No GPS and no display might bother some people, but I love the minimalist approach.",
    "Canadian shipping was fast. Price in CAD is steep but comparable to other premium wearables.",
    "Honestly surprised by how light it is. I forget I'm wearing it most of the time.",
    "The HRV tracking has been a game changer for understanding my stress levels.",
    "Returned it after a week — the subscription on top of the purchase price was too much for me.",
    "Perfect for someone who wants health data without a screen on their wrist.",
    "Battery life is solid. Charges fast and lasts nearly a week with regular use.",
    "The sizing kit process was a bit annoying but the fit is perfect once you get the right size.",
    "Sleep stages are more detailed than any smartwatch I've tried. Worth every penny.",
    "Wish it had a display, but the companion app makes up for it with really rich data.",
    "My doctor actually asked about my SpO2 trends after I showed her my Oura data. That's impressive.",
    "Great product overall but customer support was slow when I had a syncing issue.",
]

# Static competitor data — real product names, not randomized
COMPETITORS = [
    {"name": "Samsung Galaxy Ring", "price_cad": 549.99, "retailer": "BestBuy.ca", "category": "fitness ring"},
    {"name": "RingConn Smart Ring", "price_cad": 329.99, "retailer": "Amazon.ca", "category": "fitness ring"},
    {"name": "Ultrahuman Ring AIR", "price_cad": 399.99, "retailer": "Amazon.ca", "category": "fitness ring"},
]

# Static specifications — product facts, not randomized
SPECIFICATIONS = {
    "battery_life": "4-7 days",
    "water_resistance": "100m",
    "sensors": ["heart rate", "SpO2", "skin temperature", "accelerometer"],
    "connectivity": "Bluetooth 5.1",
    "materials": "Titanium",
    "weight": "4-6g",
    "subscription": "Oura Membership (optional, ~CAD $7.99/month)",
}


def run_scraper(product_name: str, market: str) -> dict[str, Any]:
    """
    Mocked web scraper tool.

    Simulates data collection from e-commerce platforms for the given market.
    Faker randomizes prices and review selection on each call.
    In production, replace with a real scraping service, third-party product API,
    or data provider integration — the interface stays the same.
    """
    # Faker varies prices and shop data within realistic ranges on each call
    base = 429.99
    retailers = {
        "Official Store": {
            "price_cad": round(base, 2),
            "in_stock": True,
            "platform_rating": round(fake.pyfloat(min_value=4.0, max_value=5.0, right_digits=1), 1),
            "review_count": fake.pyint(min_value=800, max_value=2000),
            "shipping": "Free standard shipping",
        },
        "Amazon.ca": {
            "price_cad": round(base + fake.pyfloat(min_value=5, max_value=25, right_digits=2), 2),
            "in_stock": fake.boolean(chance_of_getting_true=90),
            "platform_rating": round(fake.pyfloat(min_value=3.8, max_value=4.8, right_digits=1), 1),
            "review_count": fake.pyint(min_value=1000, max_value=5000),
            "shipping": "Free with Prime",
        },
        "BestBuy.ca": {
            "price_cad": round(base + fake.pyfloat(min_value=10, max_value=35, right_digits=2), 2),
            "in_stock": fake.boolean(chance_of_getting_true=80),
            "platform_rating": round(fake.pyfloat(min_value=3.5, max_value=4.6, right_digits=1), 1),
            "review_count": fake.pyint(min_value=200, max_value=1500),
            "shipping": "Free shipping over $35",
        },
    }
    prices = {shop: data["price_cad"] for shop, data in retailers.items()}
    average_price = round(sum(prices.values()) / len(prices), 2)

    # Faker picks 8 random reviews from the pool on each call
    reviews = fake.random_elements(elements=REVIEW_POOL, length=8, unique=True)

    return {
        "product_name": product_name,
        "market": market,
        "retailers": retailers,
        "prices_by_retailer": prices,
        "average_price": average_price,
        "competitors": COMPETITORS,
        "specifications": SPECIFICATIONS,
        "review_samples": reviews,
    }
