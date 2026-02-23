from app.tools.scraper import run_scraper


def test_scraper_returns_required_keys():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    for key in ("prices_by_retailer", "average_price", "competitors", "specifications", "review_samples"):
        assert key in result


def test_scraper_product_and_market_passthrough():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    assert result["product_name"] == "Oura Ring Gen 3"
    assert result["market"] == "Canada"


def test_scraper_prices_are_positive_floats():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    for retailer, price in result["prices_by_retailer"].items():
        assert isinstance(price, float), f"{retailer} price should be float"
        assert price > 0, f"{retailer} price should be positive"



def test_scraper_has_at_least_one_competitor():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    assert len(result["competitors"]) >= 1
    for comp in result["competitors"]:
        assert "name" in comp
        assert "price_cad" in comp
        assert isinstance(comp["price_cad"], float)


def test_scraper_has_reviews():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    assert len(result["review_samples"]) >= 1
    for review in result["review_samples"]:
        assert isinstance(review, str)
        assert len(review) > 0


def test_scraper_specifications_structure():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    specs = result["specifications"]
    assert "battery_life" in specs
    assert "sensors" in specs
    assert isinstance(specs["sensors"], list)


def test_scraper_retailers_structure():
    result = run_scraper("Oura Ring Gen 3", "Canada")
    assert "retailers" in result
    for shop, data in result["retailers"].items():
        assert "price_cad" in data,        f"{shop} missing price_cad"
        assert "in_stock" in data,         f"{shop} missing in_stock"
        assert "platform_rating" in data,  f"{shop} missing platform_rating"
        assert "review_count" in data,     f"{shop} missing review_count"
        assert "shipping" in data,         f"{shop} missing shipping"
        assert isinstance(data["in_stock"], bool)
        assert 0.0 <= data["platform_rating"] <= 5.0


