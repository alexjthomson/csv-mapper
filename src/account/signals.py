from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically add newly created users to the 'default' group. If the
    'default' group doesn't exist, a warning will be logged but the group will
    not be created.

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

        try:
            # Attempt to fetch the default group:
            group = Group.objects.get(name='default')
            # Add the user to the group:
            instance.groups.add(group)
        except Group.DoesNotExist:
            # Log a warning if the group doesn't exist:
            logger.warning("'default' group does not exist. User '%s' was not added to any group.", instance.username)
        except Exception as exception:
            # Log any other unexpected errors:
            logger.error("An error occurred while adding user '%s' to the 'default' group: %s", instance.username, str(exception))