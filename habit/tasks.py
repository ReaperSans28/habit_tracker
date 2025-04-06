from celery import shared_task

from habit.services import send_tg_message


@shared_task
def send_habit_remind(habbit):
    message = f'Напоминание про привычку "{habbit}"'
    if habbit.is_enjoyable:
        send_tg_message(habbit.owner.tg_id, message)
    else:
        message += f", а еще награда за привычку: {habbit.reward if habbit.reward else habbit.related_message}"
        send_tg_message(habbit.owner.tg_id, message)
