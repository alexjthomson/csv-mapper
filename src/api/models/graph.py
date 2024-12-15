from django.db import models
from django.core.validators import MinLengthValidator

class Graph(models.Model):
    """
    Contains the information required to describe a graph.

    Attributes:
    - name (str): A human-readable, easy-to-remember, and descriptive name that
      can be used to easily identify the graph. This should be unique. 
    - source_id (int, foreign key): ID of the data-source that supplies data to
      this graph.
    """

    class Meta:
        """
        Metadata for the graph model.

        Attributes:
        - app_label (str): Label of the app that the model belongs to.
        - db_table (str): Name of the table that the model corresponds to.
        - db_table_comment (str): Comment for the database table.
        """

        app_label = 'api'
        db_table = 'graph'
        db_table_comment = 'Contains information about a graph'

    name = models.CharField(max_length=128, unique=False, validators=[MinLengthValidator(4)])
    description = models.CharField(max_length=512)