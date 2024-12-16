from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from api.models import Source, Graph, GraphDataset
from api.views.response import *
from api.views.utility import decode_json_body, read_source_at

import csv
from json import JSONDecodeError

class GraphListView(APIView):
    """
    RESTful API endpoint for interacting with many graphs.

    The main use of this endpoint is to either get a list of each of the graphs
    that exist with some information about the graph, or to create a new graph.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieves a list of every graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_graph'):
            return error_response_no_perms()
        
        # Get the graphs:
        graphs = Graph.objects.all()

        # Create a JSON array to write each graph to:
        graph_json = []

        # Add each graph to the graph JSON data:
        for graph in graphs:
            graph_json.append({
                'id': graph.id,
                'name': graph.name,
                'description': graph.description,
            })
        
        # Return the graph JSON data:
        return success_response(graph_json, 200)
    
    def post(self, request):
        """
        Creates a new graph.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.add_graph'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = decode_json_body(request)
        except JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get and validate JSON fields:
        name = json_request['name']
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        description = json_request['description']
        if description is None:
            return error_response_expected_field('description')
        elif not isinstance(description, str):
            return error_response_invalid_field('description')
        
        # Create the graph:
        try:
            graph_instance = Graph(name=name.strip(), description=description.strip())
            graph_instance.save()
        except ValidationError:
            return error_response('Failed to validate graph data.', 400)
        except Exception:
            return error_response('Failed to create graph.', 500)
        
        # Return success response:
        return success_response(None, 200, message='The graph was created successfully.')

class GraphDetailView(APIView):
    """
    RESTful API endpoint for interacting with a single graph.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, graph_id):
        """
        Fetches data for a single graph.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.view_graph'):
            return error_response_no_perms()
        
        # Get the requested graph:
        try:
            graph = Graph.objects.get(id=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_not_found(graph_id)
        
        # Return the graph:
        return success_response({ 'name': graph.name, 'description': graph.description }, 200)
    
    def delete(self, request, graph_id):
        """
        Deletes a single graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.delete_graph'):
            return error_response_no_perms()
        
        # Get the requested graph:
        try:
            graph = Graph.objects.get(id=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_not_found(graph_id)
        
        # Delete the graph:
        graph.delete()
        return success_response(f'Deleted graph `{graph_id}`.', 200)
    
    def put(self, request, graph_id):
        """
        Updates an entire graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.change_graph'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = decode_json_body(request)
        except JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get JSON fields:
        name = json_request['name']
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        description = json_request['description']
        if description is None:
            return error_response_expected_field('description')
        elif not isinstance(description, str):
            return error_response_invalid_field('description')
        
        # Get the requested graph:
        try:
            graph = Graph.objects.get(id=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_not_found()
        
        # Edit the graph:
        graph.name = name.strip()
        graph.description = description.strip()
        graph.save()
        return success_response(None, 200, message=f'Updated graph `{graph_id}`.')

class GraphDatasetListView(APIView):
    """
    RESTful API endpoint for interacting with the datasets that belong to a
    graph.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, graph_id):
        """
        Gets every dataset that belongs to a graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_graphdataset'):
            return error_response_no_perms()
        
        # Get the datasets that belong to the graph:
        datasets = GraphDataset.objects.filter(graph=graph_id)

        # Create a JSON array to write each dataset into:
        datasets_json = []

        # Iterate each dataset:
        for dataset in datasets:
            datasets_json.append({
                'id': dataset.id,
                'label': dataset.label,
                'plot_type': dataset.plot_type,
                'is_axis': dataset.is_axis,
                'source_name': dataset.source.name,
                'source_id': dataset.source.id,
                'column_id': dataset.column
            })
        
        # Construct and return the response data:
        return success_response(datasets_json, 200)
    
    def post(self, request, graph_id):
        """
        Creates a new dataset for a graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.add_graphdataset'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = decode_json_body(request)
        except JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get JSON fields:
        label = json_request['label']
        if label is None:
            return error_response_expected_field('label')
        elif not isinstance(label, str):
            return error_response_invalid_field('label')
        plot_type = json_request['plot_type']
        if plot_type is None:
            return error_response_expected_field('plot_type')
        elif not isinstance(plot_type, str):
            return error_response_invalid_field('plot_type')
        is_axis = json_request['is_axis']
        if is_axis is None:
            return error_response_expected_field('is_axis')
        elif not isinstance(is_axis, bool):
            return error_response_invalid_field('is_axis')
        source_id = json_request['source_id']
        if source_id is None:
            return error_response_expected_field('source_id')
        elif not isinstance(source_id, int):
            return error_response_invalid_field('source_id')
        column_id = json_request['column_id']
        if column_id is None:
            return error_response_expected_field('column_id')
        elif not isinstance(column_id, int):
            return error_response_invalid_field('column_id')

        # Create the new dataset:
        try:
            dataset = GraphDataset(
                graph=Graph.objects.get(id=graph_id),
                plot_type=plot_type,
                label=label,
                is_axis=is_axis,
                source=Source.objects.get(id=source_id),
                column=column_id
            )
            dataset.save()
        except ValidationError:
            return error_response('Failed to validate dataset data.', 400)
        except Exception:
            return error_response('Failed to create dataset.', 500)
        return success_response('Created dataset.', 200)

class GraphDatasetDetailView(APIView):
    """
    RESTful API endpoint for interacting with a single datasets.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, graph_id, dataset_id):
        """
        Gets information about a dataset that belongs to the specified graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_graphdataset'):
            return error_response_no_perms()
        
        # Get the requested dataset:
        try:
            dataset = GraphDataset.objects.get(id=dataset_id, graph=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_dataset_not_found(dataset_id)

        # Return the dataset:
        response_data = {
            'label': dataset.label,
            'plot_type': dataset.plot_type,
            'is_axis': dataset.is_axis,
            'source_name': dataset.source.name,
            'source_id': dataset.source.id,
            'column_id': dataset.column
        }
        return success_response(response_data, 200)

    def delete(self, request, graph_id, dataset_id):
        """
        Deletes a dataset from a graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.delete_graphdataset'):
            return error_response_no_perms()
        
        # Get the requested dataset:
        try:
            dataset = GraphDataset.objects.get(id=dataset_id, graph=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_dataset_not_found(dataset_id)
        
        # Delete the dataset;
        dataset.delete()
        return success_response(f'Deleted dataset `${dataset_id}`.', 200)
    
    def put(self, request, graph_id, dataset_id):
        """
        The `PUT` method is used to update a dataset.
        """

        # Check permissions:
        if not request.user.has_perm('api.change_graphdataset'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = decode_json_body(request)
        except JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get JSON fields:
        label = json_request['label']
        if label is None:
            return error_response_expected_field('label')
        elif not isinstance(label, str):
            return error_response_invalid_field('label')
        plot_type = json_request['plot_type']
        if plot_type is None:
            return error_response_expected_field('plot_type')
        elif not isinstance(plot_type, str):
            return error_response_invalid_field('plot_type')
        is_axis = json_request['is_axis']
        if is_axis is None:
            return error_response_expected_field('is_axis')
        elif not isinstance(is_axis, bool):
            return error_response_invalid_field('is_axis')
        source_id = json_request['source_id']
        if source_id is None:
            return error_response_expected_field('source_id')
        elif not isinstance(source_id, int):
            return error_response_invalid_field('source_id')
        column_id = json_request['column_id']
        if column_id is None:
            return error_response_expected_field('column_id')
        elif not isinstance(column_id, int):
            return error_response_invalid_field('column_id')

        # Get the requested dataset:
        try:
            dataset = GraphDataset.objects.get(id=dataset_id, graph=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_dataset_not_found(dataset_id)
        
        # Modify the dataset:
        dataset.label = label
        dataset.plot_type = plot_type
        dataset.is_axis = is_axis
        dataset.source = Source.objects.get(id=source_id)
        dataset.column = column_id
        dataset.save()
        return success_response(f'Updated dataset `{dataset_id}`.', 200)

class GraphDataView(APIView):
    """
    RESTful API endpoint for fetching graph data for ChartJs.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, graph_id):
        """
        Fetches the ChartJs data for the graph.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.view_graph'):
            return error_response_no_perms()
        
        # Get graph:
        try:
            graph = Graph.objects.get(id=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_not_found(graph_id)

        # Get datasets for the graph:
        datasets = GraphDataset.objects.filter(graph_id=graph_id)

        # Create ChartJS fields:
        data_json = {}
        datasets_json = []
        options_json = {
            'scales': {
                'x': {},
                'y': {}
            }
        }
        csv_files = {}
        hide_scales = True

        # Populate the data with the datasets:
        if len(datasets) > 0:
            for dataset in datasets:
                if not dataset.is_axis and dataset.plot_type == 'none':
                    # The dataset should not be plotted.
                    pass
                else:
                    # The dataset should be plotted, we should read the dataset
                    # CSV values:
                    csv_file = csv_files.get(dataset.source.location)
                    if csv_file is None:
                        csv_read_result = read_source_at(dataset.source.location)
                        if not csv_read_result[0]:
                            # The read failed, this is an error response; we should
                            # return the error response:
                            return csv_read_result[1]
                        csv_file = csv_read_result[1]
                        csv_files[dataset.source.location] = csv_file
                    else:
                        csv_file.seek(0)
                    csv_reader = csv.reader(csv_file)

                    # If the source has a header, we should skip it:
                    if dataset.source.has_header:
                        next(csv_reader, None)
                    # We should get the current row:
                    current_row = next(csv_reader, None)
                    if current_row is None:
                        # There is no data to plot, we should skip this iteration:
                        continue
                    
                    # We should check that the columns value is in bounds:
                    # NOTE: The below section has been marked `nosec` because it
                    # flags a false-positive during a security scan and is
                    # identified as a potential SQL injection vector though
                    # string-based query construction. This is likely due to the
                    # variable names chosen. This code has nothing to do with
                    # SQL databases and never interacts with them. It is simply
                    # a bounds check that ensures the `column_index` exists.
                    column_index = dataset.column
                    if not (0 <= column_index < len(current_row)): # nosec
                        return error_response( # nosec
                            f'Column is out of bounds (value: `{column_index}`, min: `0`, max: `{len(current_row)}`). ' # nosec
                            f'Please update the column within the graph dataset to point to an existing column.', # nosec
                            400 # nosec
                        ) # nosec
                    
                    # We should read the dataset data:
                    dataset_data = []
                    while current_row is not None:
                        if column_index < len(current_row):
                            dataset_data.append(current_row[column_index])
                        else:
                            dataset_data.append(None)
                        current_row = next(csv_reader, None)
                    
                    # Remove trailing None values from the end of the dataset
                    # data:
                    while dataset_data and dataset_data[-1] is None:
                        dataset_data.pop()

                    # Determine if the dataset represents an axis or a plot:
                    if dataset.is_axis:
                        # The dataset represents an axis:
                        data_json['labels'] = dataset_data
                        options_json['scales']['x'] = {
                            'title': {
                                'display': True,
                                'text': dataset.label
                            }
                        }
                    else:
                        # The dataset needs plotting, get the plot type:
                        plot_type = GraphDataset.PlotType(dataset.plot_type)
                        # Construct the dataset JSON object:
                        datasets_json.append({
                            'type': plot_type.label,
                            'label': dataset.label if dataset.label is not None else f'Dataset {dataset.id}',
                            'data': dataset_data
                        })
                        # Check if the scales should be hidden:
                        if plot_type is GraphDataset.PlotType.LINE or plot_type is GraphDataset.PlotType.BAR or plot_type is GraphDataset.PlotType.SCATTER:
                            hide_scales = False

        if hide_scales:
            options_json.pop('scales')

        # Assign the datasets:
        data_json['datasets'] = datasets_json

        # Return the ChartJS data:
        return success_response({
            'data': data_json,
            'options': options_json,
        }, 200)