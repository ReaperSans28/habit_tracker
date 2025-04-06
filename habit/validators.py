from datetime import timedelta
from rest_framework.serializers import ValidationError

class HabitValidator:
    def __call__(self, value):
        val = dict(value)

        if val.get("complete_time") > timedelta(seconds=120):
            raise ValidationError(
                "Совет от Комару. Не стоит выделять дольше 2 минут на привычку."
            )

        period = int(val.get("period", 0))
        if period < 1 or period > 7:
            raise ValidationError(
                "Совет от Комару. Привычка должна выполнятся хотя бы 1 раз за неделю."
            )

        nice_habit = val.get("nice_habit")
        award = val.get("award")
        associated_habit = val.get("associated_habit")

        if not nice_habit and not award and not associated_habit:
            raise ValidationError(
                "Совет от Комару. Для полезной привычки нужна либо 'награда', либо 'связанная привычка'"
            )

        if not nice_habit and award and associated_habit:
            raise ValidationError(
                "Совет от Комару. Для полезной привычки нужно выбрать только 1 поле. Либо 'награда', либо 'связанная привычка'"
            )

        if nice_habit and associated_habit:
            raise ValidationError(
                "Совет от Комару. У приятной привычки не должно быть связанной привычки."
            )

        if nice_habit and award:
            raise ValidationError(
                "Совет от Комару. У приятной привычки не должно быть вознаграждения."
            )
