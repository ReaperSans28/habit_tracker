from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import time

from habit.models import Habit
from users.models import User


class HabitTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email="komaru@kkk.com")
        self.test_habit = Habit.objects.create(
            habit_owner=self.test_user,
            habit_place="У себя дома",
            habit_time=time(20, 31),
            habit_action="Выполнить дыхательную гимнастику",
            is_habit_pleasantly=False,
            habit_periodicity=1,
            reward="Кислород в легкие))))",
            habit_time_to_complete=120,
            is_habit_public=False,
        )
        self.client.force_authenticate(user=self.test_user)

    def test_create_habit(self):
        url = reverse("habit:create_habits")
        data = {
            "habit_place": "У себя дома",
            "habit_time": "20:31:00",
            "habit_action": "Выполнить дыхательную гимнастику",
            "is_habit_pleasantly": False,
            "habit_periodicity": 1,
            "reward": "Кислород в легкие))))",
            "habit_time_to_complete": 120,
            "is_habit_public": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_retrieve_habit(self):
        url = reverse("habit:retrieve_habits", args=(self.test_habit.pk,))
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("habit_periodicity"), self.test_habit.habit_periodicity)

    def test_list_habits(self):
        url = reverse("habit:habit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_update_habit(self):
        url = reverse("habit:update_habits", args=(self.test_habit.pk,))
        update_data = {
            "habit_place": "На кухне",
            "habit_time": "22:13:00",
            "habit_action": "Выпить таблетки",
            "is_habit_pleasantly": True,
            "habit_periodicity": 1,
            "habit_time_to_complete": 120,
            "is_habit_public": True,
        }
        response = self.client.patch(url, update_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("habit_place"), "На кухне")

    def test_delete_habit(self):
        url = reverse("habit:delete_habits", args=(self.test_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_public_habit_list(self):
        self.test_habit.is_habit_public = True
        self.test_habit.save()
        
        url = reverse("habit:public_habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
