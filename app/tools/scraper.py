from typing import Any


def run_scraper(product_name: str, market: str) -> dict[str, Any]:
    """
    Mocked web scraper tool.

    Simulates data collection from Canadian e-commerce platforms.
    In production, replace with a real scraping service, third-party product API,
    or data provider integration — the interface stays the same.
    """
    return {
        "product_name": product_name,
        "market": market,
        "prices_by_retailer": {
            "Amazon.ca": 449.99,
            "BestBuy.ca": 459.99,
            "Official Store": 429.99,
        },
        "average_price": 446.66,
        "competitors": [
            {
                "name": "Samsung Galaxy Ring",
                "price_cad": 549.99,
                "retailer": "BestBuy.ca",
                "category": "fitness ring",
            },
            {
                "name": "RingConn Smart Ring",
                "price_cad": 329.99,
                "retailer": "Amazon.ca",
                "category": "fitness ring",
            },
            {
                "name": "Ultrahuman Ring AIR",
                "price_cad": 399.99,
                "retailer": "Amazon.ca",
                "category": "fitness ring",
            },
        ],
        "specifications": {
            "battery_life": "4-7 days",
            "water_resistance": "100m",
            "sensors": ["heart rate", "SpO2", "skin temperature", "accelerometer"],
            "connectivity": "Bluetooth 5.1",
            "materials": "Titanium",
            "weight": "4-6g",
            "subscription": "Oura Membership (optional, ~CAD $7.99/month)",
        },
        "review_samples": [
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
        ],
    }
