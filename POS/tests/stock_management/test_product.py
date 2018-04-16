from POS.tests.base.base_test_case import BaseTestCase

from POS.models.base_model import AppDB
from POS.models.stock_management.product import Product


class TestProduct(BaseTestCase):
    product_name: str = "test_product_name"
    product_buying_price: float = 20
    product_selling_price: float = 20
    product_quantity: float = 19

    def setUp(self):
        self.init_test_app()
        self.create_users()

    def test_get_all_products(self):
        # Login as cashier
        self.login_as_cashier()

        # Get products
        rv = self.test_app.get("/product")

        self.assertEqual("200", rv.headers["code"])

    def test_add_product(self):
        # Login as admin
        self.login_as_admin()

        # Add product
        self.create_product()

        # Check if it has been created
        self.assertEqual(AppDB.db_session.query(Product).count(), 1)

    def test_modify_product(self):
        # Login as admin
        self.login_as_admin()

        # Add product
        self.create_product()

        # Get the product
        product = AppDB.db_session.query(Product).first()

        # New info
        product_id = product.id
        new_product_name = TestProduct.product_name + "more stuff"
        new_product_buying_price = TestProduct.product_buying_price + 10
        new_product_selling_price = TestProduct.product_selling_price + 10
        new_product_quantity = TestProduct.product_quantity + 10

        # Modify product
        self.send_json_put(
            endpoint="/product",
            id=product_id,
            name=new_product_name,
            buying_price=new_product_buying_price,
            selling_price=new_product_selling_price,
            quantity=new_product_quantity
        )

        # Check if changes have been effected
        # Get the product
        product = AppDB.db_session.query(Product).first()

        self.assertEqual(new_product_name, product.name)
        self.assertEqual(new_product_buying_price, product.buying_price)
        self.assertEqual(new_product_selling_price, product.selling_price)
        self.assertEqual(new_product_quantity, product.quantity)

    def test_delete_product(self):
        # Login as admin
        self.login_as_admin()

        # Add product
        self.create_product()

        # Get the product
        product = AppDB.db_session.query(Product).first()

        # Remove the product
        self.send_json_delete(
            endpoint="/product",
            id=product.id
        )

        # Check if it has been removed
        self.assertEqual(AppDB.db_session.query(Product).count(), 0)

    def create_product(self):
        self.send_json_post(
            "/product",
            name=TestProduct.product_name,
            buying_price=TestProduct.product_buying_price,
            selling_price=TestProduct.product_selling_price,
            quantity=TestProduct.product_quantity
        )
