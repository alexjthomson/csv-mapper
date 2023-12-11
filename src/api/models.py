from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator

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

class GraphDataset(models.Model):
    """
    Describes a single dataset that is to be plotted onto a graph.

    Attributes:
    - graph (int, foreign key): ID of the graph that this dataset belongs to.
    - plot_type (str): Describes how the dataset should be plotted.
    - label (str): Label for the dataset, this is synonymous with the name of
      the dataset.
    - is_axis (bool): Indicates if this dataset should be used as the X-axis
      labels. This is useful for datasets that contain information such as
      timestamps that the rest of the datasets may be plotted against.
    - source (int, foreign key): ID of the source that contains the data for the
      dataset.
    - column (int): Zero-indexed ID of the column within the source that
      contains the dataset.
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
        db_table = 'graph_dataset'
        db_table_comment = 'Describes individual datasets that can be plotted to a graph'
    
    class PlotType(models.TextChoices):
        """
        Describes each type of plot that a dataset can have.

        This maps a database value to a chartJs value.
        """
        NONE = 'none', 'none'
        LINE = 'line', 'line'
        BAR = 'bar', 'bar'
        BUBBLE = 'bubble', 'bubble'
        PIE = 'pie', 'pie'
        DOUGHNUT = 'doughnut', 'doughnut'
        POLAR_AREA = 'polar_area', 'polarArea'
        RADAR = 'radar', 'radar'
        SCATTER = 'scatter', 'scatter'

    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)    
    plot_type = models.CharField(max_length=16, choices=PlotType.choices)
    label = models.CharField(max_length=128, validators=[MinLengthValidator(4)])
    is_axis = models.BooleanField(default=False)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    column = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])