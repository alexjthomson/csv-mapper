from django.db import models
from django.core.validators import MinValueValidator

class SourceModel(models.Model):
    """
    Describes the location of CSV data that can be fetched by the application in
    order to build a graph.

    Attributes:
    - name (string): A human-readable, easy-to-remember, and descriptive name
      that can be used to easily identify the data source. This should be
      unique.
    - location (string): Location that the CSV data is expected to be found at.
      This should be formatted like a URL.
    - has_header (boolean): Describes if the CSV file is expected to have a
      header.
    """

    class Meta:
        """
        Metadata for the data-source model.

        Attributes:
        - app_label (string): Label of the app that the model belongs to.
        - db_table (string): Name of the table that the model corresponds to.
        - db_table_comment (string): Comment for the database table.
        """

        app_label = 'api'
        db_table = 'source'
        db_table_comment = 'Describes the location of CSV data.'

    name = models.CharField(max_length=128, unique=False)
    location = models.CharField(max_length=256)
    has_header = models.BooleanField(default=False)

class GraphModel(models.Model):
    """
    Contains the information required to describe a graph.

    Attributes:
    - name (string): A human-readable, easy-to-remember, and descriptive name
    that can be used to easily identify the graph. This should be unique.
    - source_id (integer, foreign key): ID of the data-source that supplies data
    to this graph.
    """

    class Meta:
        """
        Metadata for the graph model.

        Attributes:
        - app_label (string): Label of the app that the model belongs to.
        - db_table (string): Name of the table that the model corresponds to.
        - db_table_comment (string): Comment for the database table.
        """

        app_label = 'api'
        db_table = 'graph'
        db_table_comment = 'Contains graphs'

    name = models.CharField(max_length=128, unique=False)
    source_id = models.ForeignKey(SourceModel, on_delete=models.CASCADE)

class SourceColumnConfigModel(models.Model):
    """
    Contains configuration options for a singular column within a data-source.

    Attributes:
    - source_id (integer, foreign key): ID of the data-source that the
    configuration applies to.
    - column_id (16-bit integer): Zero-indexed ID of the column within the
      referenced data-source that the configuration applies to.
    - transform_type (string): An enum-like variable that can be used to
      transform raw values within the data-source column into another value
      using a transformer. The transformer is referenced by name in this field.
    - unit (string): The unit of the data within the data-source column. For
      instance, if the column is describing a bit-rate in megabits per second,
      this may be equal to `Mbps`.
    """

    class Meta:
        """
        Metadata for the data-source column config model.

        Attributes:
        - app_label (string): Label of the app that the model belongs to.
        - db_table (string): Name of the table that the model corresponds to.
        - db_table_comment (string): Comment for the database table.
        """

        app_label = 'api'
        db_table = 'source_column_config'
        db_table_comment = 'Contains configuration for individual columns of data-sources.'

    class Transformers(models.TextChoices):
        """
        Maps a transform name to a transformer function capable of transforming
        a column within a data-source into a new format.
        """
        NONE = 'none', ''

    source_id = models.ForeignKey(SourceModel, on_delete=models.CASCADE)
    column_id = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    column_name = models.CharField(max_length=128)
    transform_name = models.CharField(max_length=128, choices=Transformers.choices, default=Transformers.NONE)
    unit = models.CharField(max_length=32)