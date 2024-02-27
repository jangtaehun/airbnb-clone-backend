from typing import Any
from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenitise/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()
        # self.assertEqual(response.status_code, 200, "Status Code isn't 200.")
        self.assertIsInstance(data, list)  # data가 list인지 확인
        self.assertEqual(len(data), 1)  # 하나만 생성했기 때문에 1
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc"

        response = self.client.post(
            self.URL,
            data={"name": new_amenity_name, "description": new_amenity_description},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200, "Not 200")
        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_description)

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenityDetail(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenitise/1"
    URL1 = "/api/v1/rooms/amenitise/2"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get(self.URL1)
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESC)

    # code challenge
    def test_post_amenity(self):

        update_amenity_name = "Update Amenity"
        wrong_name = "qqwwqeqweqweqwwqewqasdseqwasfdsvfeqqwwqeqweqweqwwqewqasdseqwasfdsvfeqqwwqeqweqweqwwqewqasdseqwasfdsvfeqqwwqeqweqweqwwqewqasdseqwasfdsvfeqqwwqeqweqweqwwqewqasdseqwasfdsvfeqqwwqeqweqweqwwqewqasdseqwasfdsvfeqqwwqeqweqweqwwqewqasdseqwasfdsvfe"
        update_amenity_description = "Update Amenity desc"

        response = self.client.put(
            self.URL,
            data={"name": update_amenity_name},
        )
        data = response.json()
        self.assertEqual(response.status_code, 200, "Not 1")

        response = self.client.put(
            self.URL,
            data={"description": update_amenity_description},
        )
        data = response.json()
        self.assertEqual(response.status_code, 200, "Not 2")

        self.assertEqual(data["name"], update_amenity_name)
        self.assertEqual(data["description"], update_amenity_description)

    def test_delete_amenity(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    URL = "/api/v1/rooms/"

    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("1234")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )
        response = self.client.post(self.URL)
        print(response.json())
