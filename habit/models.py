from django.db import models

from users.models import User


class Habit(models.Model):
    habit_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Создатель привычки"
    )
    habit_place = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Место выполнения"
    )
    habit_time = models.TimeField(
        verbose_name="Время выполнения привычки",
        auto_now_add=False,
        auto_now=False
    )
    habit_action = models.CharField(
        max_length=100,
        verbose_name="Действие",
    )
    is_habit_pleasantly = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Признак приятной привычки",
    )
    related_habit = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
    )
    habit_periodicity = models.PositiveIntegerField(
        verbose_name="Периодичность привычки",
    )
    reward = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Награда",
    )
    habit_time_to_complete = models.PositiveIntegerField(
        default=120,
        verbose_name="Время на выполнение",
    )
    is_habit_public = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Признак публичности",
    )

    def __str__(self):
        return f"{self.habit_action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
