from rest_framework.serializers import ValidationError

class HabitValidator:
    def __call__(self, value):
        val = dict(value)

        time_to_complete = val.get("habit_time_to_complete")
        if time_to_complete is not None and time_to_complete > 120:
            raise ValidationError(
                "Совет от Комару. Не стоит выделять дольше 2 минут на привычку."
            )

        # Проверка периодичности
        periodicity = val.get("habit_periodicity")
        if periodicity is not None and (periodicity < 1 or periodicity > 7):
            raise ValidationError(
                "Совет от Комару. Привычка должна выполнятся хотя бы 1 раз за неделю."
            )

        # Проверка связанных полей
        is_pleasant = val.get("is_habit_pleasantly")
        reward = val.get("reward")
        related_habit = val.get("related_habit")

        if not is_pleasant and not reward and not related_habit:
            raise ValidationError(
                "Совет от Комару. Для полезной привычки нужна либо 'награда', либо 'связанная привычка'"
            )

        if not is_pleasant and reward and related_habit:
            raise ValidationError(
                "Совет от Комару. Для полезной привычки нужно выбрать только 1 поле. Либо 'награда', либо 'связанная привычка'"
            )

        if is_pleasant and related_habit:
            raise ValidationError(
                "Совет от Комару. У приятной привычки не должно быть связанной привычки."
            )

        if is_pleasant and reward:
            raise ValidationError(
                "Совет от Комару. У приятной привычки не должно быть вознаграждения."
            )
