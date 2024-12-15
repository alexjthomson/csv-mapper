from django.db import models
from django.core.validators import MinLengthValidator

class Source(models.Model):
    """
    Describes the location of CSV data that can be fetched by the application in
    order to build a graph.

    Attributes:
    - name (str): A human-readable, easy-to-remember, and descriptive name that
      can be used to easily identify the data source. This should be unique.
    - location (str): Location that the CSV data is expected to be found at.
      This should be formatted like a URL.
    - has_header (bool): Describes if the CSV file is expected to have a
      header.
    """

    class Meta:
        """
        Metadata for the data-source model.

        Attributes:
        - app_label (str): Label of the app that the model belongs to.
        - db_table (str): Name of the table that the model corresponds to.
        - db_table_comment (str): Comment for the database table.
        """

        app_label = 'api'
        db_table = 'source'
        db_table_comment = 'Describes the location of CSV data.'

    name = models.CharField(max_length=128, unique=False, validators=[MinLengthValidator(4)])
    location = models.CharField(max_length=256)
    has_header = models.BooleanField(default=False)