# Generated by Django 5.0 on 2023-12-09 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_graph_name_alter_graphdataset_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphdataset',
            name='plot_type',
            field=models.CharField(choices=[('none', 'none'), ('line', 'line'), ('bar', 'bar')], max_length=16),
        ),
    ]
