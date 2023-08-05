import typetools

import unittest


class Stock:
    market = typetools.MaxSizedIterable(size=5)
    shares = typetools.Integer()
    price = typetools.MaxSizedInteger(size=100)
    people_buying = typetools.MinSizedInteger(size=0)
    a = typetools.Dict()

    def __init__(self, market, shares, price, people_buying, a):
        self.market = market
        self.shares = shares
        self.price = price
        self.people_buying = people_buying
        self.a = a


@typetools.checkattrs(name=typetools.String(),
                      size=typetools.Integer(),
                      variations=typetools.List(),
                      cost=typetools.typed.GenericTyped(type=float))
class Font:
    def __init__(self, name, size, variations, cost):
        self.name = name
        self.size = size
        self.variations = variations
        self.cost = cost


class TestTypetools(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("ABC", 13, 56, 14, {"blah": "hah123"})
        self.arial_font = Font("Arial", 40, ["bold", "italic"], 0.00)

    def _change_market_to(self, market):
        self.stock.market = market

    def _change_shares_to(self, shares):
        self.stock.shares = shares

    def _change_price_to(self, price):
        self.stock.price = price

    def _change_people_buying_to(self, people_buying):
        self.stock.people_buying = people_buying

    def _change_a_to(self, a):
        self.stock.a = a

    def _change_name_to(self, name):
        self.arial_font.name = name

    def _change_variations_to(self, variations):
        self.arial_font.variations = variations

    def _change_cost_to(self, cost):
        self.arial_font.cost = cost

    def test_MaxSizedIterable(self):
        self.assertRaises(ValueError,
                          lambda: self._change_market_to("AAAAAAAAAA"))

    def test_Integer(self):
        self.assertRaises(TypeError,
                          lambda: self._change_shares_to("blah"))

    def test_MaxSizedInteger(self):
        self.assertRaises(ValueError,
                          lambda: self._change_price_to(128))
        self.assertRaises(TypeError,
                          lambda: self._change_price_to(["blah"]))

    def test_MinSizedInteger(self):
        self.assertRaises(ValueError,
                          lambda: self._change_people_buying_to(-1000))
        self.assertRaises(TypeError,
                          lambda: self._change_people_buying_to([1, 2, 3]))

    def test_Mapping(self):
        self.assertRaises(TypeError,
                          lambda: self._change_a_to(123))

    def test_checkattrs(self):
        self.assertRaises(TypeError,
                          lambda: self._change_name_to(12345))
        self.assertRaises(TypeError,
                          lambda: self._change_variations_to("bold and italic"))

    def test_GenericTyped(self):
        self.assertRaises(TypeError,
                          lambda: self._change_cost_to("abc123"))


if __name__ == "__main__":
    unittest.main()
