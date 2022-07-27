from django.test import TestCase

from purchases.models import Purchase


class PurchasesViewTestCase(TestCase):
    def setUp(self) -> None:
        Purchase.objects.create(name="test_purchase", cost=333, date="2022-02-22")
        return super().setUp()

    def test_create_purcase(self):

        data = {"name": "buing", "cost": 123, "date": "2022-02-22"}
        response = self.client.post("/purchases/", data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"id": 2, "name": "Buing", "cost": 123, "date": "2022-02-22"},
        )

    def test_create_list_of_purchases(self):

        data = [
            {"name": "buing_1", "cost": 123, "date": "2022-02-22"},
            {"name": "buin_2", "cost": 456, "date": "2022-02-25"},
            {"name": "buing_3", "cost": 789, "date": "2022-02-27"},
        ]
        response = self.client.post(
            "/purchases/", data=data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            [
                {"id": 2, "name": "Buing_1", "cost": 123, "date": "2022-02-22"},
                {"id": 3, "name": "Buin_2", "cost": 456, "date": "2022-02-25"},
                {"id": 4, "name": "Buing_3", "cost": 789, "date": "2022-02-27"},
            ],
        )

    def test_get_purchases(self):

        response = self.client.get("/purchases/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "name": "Test_Purchase", "cost": 333, "date": "2022-02-22"}],
        )

    def test_get_purchases_by_name(self):

        response = self.client.get("/purchases/?name=Test_Purchase")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "name": "Test_Purchase", "cost": 333, "date": "2022-02-22"}],
        )

    def test_get_purchases_by_wrong_name(self):

        response = self.client.get("/purchases/?name=wrong")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_purchases_by_cost(self):
        response = self.client.get("/purchases/?cost=333")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "name": "Test_Purchase", "cost": 333, "date": "2022-02-22"}],
        )

    def get_purchases_by_cost2(self):

        response = self.client.get("/purchases/?cost=4124932142")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_purchase_by_date1(self):
        response = self.client.get(
            "/purchases/?from_date=2022-01-31&to_date=2022-12-22"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "name": "Test_Purchase", "cost": 333, "date": "2022-02-22"}],
        )

    def test_get_purchase_by_date2(self):
        response = self.client.get(
            "/purchases/?from_date=2022-02-23&to_date=2022-02-24"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [],
        )

    def test_get_purchase(self):

        response = self.client.get("/purchases/1/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "name": "Test_Purchase", "cost": 333, "date": "2022-02-22"},
        )

    def test_get_purchase_404(self):

        response = self.client.get("/purchases/12345/")
        self.assertEqual(response.status_code, 404)

    def test_delete_purchase(self):

        response = self.client.delete("/purchases/1/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Purchase.objects.filter(name="test_purchase", cost=333).exists()
        )

    def test_update_purchase(self):

        data = {"name": "updated_name", "cost": 777, "date": "2023-03-23"}

        response = self.client.put(
            "/purchases/1/", data=data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "name": "Updated_Name", "cost": 777, "date": "2023-03-23"},
        )

    def test_patch_purchase(self):
        data = {"name": "update only name"}
        response = self.client.patch(
            "/purchases/1/", data=data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "name": "Update Only Name", "cost": 333, "date": "2022-02-22"},
        )


class PurchasesListTestCase(TestCase):
    def setUp(self) -> None:
        for i in range(10):
            Purchase.objects.create(
                name=f"test_purchase {i}", cost=100 * i, date=f"2022-07-{10+i}"
            )
        return super().setUp()

    def test_get_without_filters(self):

        response = self.client.get("/get_purchases/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)

    def test_get_purchases_with_start_date(self):
        response = self.client.get("/get_purchases/?from_date=2022-07-17")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_get_purchases_with_end_date(self):
        response = self.client.get("/get_purchases/?to_date=2022-07-14")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_get_purchases_with_dates(self):
        response = self.client.get(
            "/get_purchases/?from_date=2022-07-11&to_date=2022-07-14"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_get_purchases_with_future_dates(self):
        response = self.client.get(
            "/get_purchases/?from_date=2022-12-11&to_date=2022-12-14"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_purchases_one_date(self):

        Purchase.objects.create(name="something", cost=1234567, date="2022-07-17")

        response = self.client.get(
            "/get_purchases/?from_date=2022-07-17&to_date=2022-07-17"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_purchases_count_total(self):
        for _ in range(10):
            Purchase.objects.create(name="something", cost=123, date="2022-07-27")

        response = self.client.get(
            "/get_purchases/?from_date=2022-07-27&to_date=2022-07-27"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(
            response.json(), [{"name": "Something", "total": 1230, "count": 10}]
        )
