
from django.db.models.signals import Signal
from django.dispatch import receiver


user_created = Signal()


@receiver(user_created)
def user_created_handler(sender, **kwargs):
    # Your logic here
    # For example, you can access the newly created user instance using "sender" variable.
    print("New user created!", sender)
