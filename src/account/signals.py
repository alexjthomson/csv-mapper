from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically add newly created users to the 'default' group. If the
    'default' group doesn't exist, log a warning and create it.

    Arguments:
    - sender: The model class sending the signal (`User`).
    - instance: The actual instance being saved (a `User` instance).
    - created: Boolean indicating if a new record was created.
    - kwargs: Additional keyword arguments.
    """
    
    if created:
        # Validate the instance:
        if not isinstance(instance, User):
            logger.error("Signal received for a non-User instance: %s", type(instance))
            return

        # Try add new user to default group:
        try:
            # Try to fetch the default group:
            group, group_created = Group.objects.get_or_create(name='default')
            if group_created:
                logger.warning("'default' group did not exist and was created.")

            # Add the user to the group:
            instance.groups.add(group)
        except Exception as exception:
            # Log any unexpected error:
            logger.error("Failed to add user to the 'default' group: %s", str(exception))