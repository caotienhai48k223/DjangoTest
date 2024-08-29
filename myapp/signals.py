from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Room

@receiver(post_save, sender=User)
def create_or_update_room(sender, instance, created, **kwargs):
    if created:
        # Tạo một Room mới với tên là User mới
        Room.objects.create(name=instance.username)
    else:
        # Cập nhật Room nếu cần thiết
        Room.objects.filter(name=instance.username).update(name=instance.username)
