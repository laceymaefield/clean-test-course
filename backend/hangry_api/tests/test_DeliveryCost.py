from api.controllers import Delivery
from django_mock_queries.query import MockSet, MockModel


def test_lots_of_items_get_high_delivery_fee():
    # Arrange an order with more than 10 items and a long delivery distance.
    order = MockSet()
    order.add(MockModel(quantity=5))
    order.add(MockModel(quantity=5))
    order.add(MockModel(quantity=5))

    # Act
    cost = Delivery.calculate(order, 6)

    # Assert the high-distance, high-quantity fee remains unchanged.
    assert cost == 7.50


def test_middle_quantity_and_distance_get_middle_delivery_fee():
    # Arrange an order with more than 5 items and a distance over 3.
    order = MockSet()
    order.add(MockModel(quantity=2))
    order.add(MockModel(quantity=2))
    order.add(MockModel(quantity=2))

    # Act
    cost = Delivery.calculate(order, 4)

    # Assert the middle delivery tier remains unchanged.
    assert cost == 5


def test_default_delivery_fee_is_350():
    # Arrange an order that does not qualify for either surcharge tier.
    order = MockSet()
    order.add(MockModel(quantity=3))
    order.add(MockModel(quantity=1))

    # Act
    cost = Delivery.calculate(order, 2)

    # Assert the standard delivery fee is now $3.50.
    assert cost == 3.50


def test_default_delivery_fee_applies_at_tier_boundaries():
    # Check boundary values: exactly 5 items or exactly 3 miles do not
    # qualify for the middle tier because the controller uses strict > checks.
    five_items = MockSet()
    five_items.add(MockModel(quantity=5))
    assert Delivery.calculate(five_items, 4) == 3.50

    six_items_short_distance = MockSet()
    six_items_short_distance.add(MockModel(quantity=6))
    assert Delivery.calculate(six_items_short_distance, 3) == 3.50
