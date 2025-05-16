from rest_framework import generics
from rest_framework.permissions import AllowAny

from habit.models import Habit
from habit.paginators import CustomPagination
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer
from habit.services import send_tg_message


class PublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_habit_public=True)
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(habit_owner=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.habit_owner = self.request.user
        habit = serializer.save()
        habit.save()
        if habit.habit_owner.tg_chat_id:
            send_tg_message(habit.habit_owner.tg_chat_id, "Новая привычка создана")


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
