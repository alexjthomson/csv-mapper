const validMethods = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
    'OPTION',
    'HEAD',
    'TRACE'
];
const validPlotTypes = [
    'none',
    'axis',
    'line',
    'bar',
    'pie',
    'doughnut',
    'polar_area',
    'radar',
    'scatter'
];

/**
 * Handles an error when communicating with the API.
 * 
 * @param {string} message Message describing the error.
 * @returns Returns a JSON object that describes the error.
 */
function apiError(message) {
    console.error(message);
    return {
        result: 'error',
        message: message
    }
}

/**
 * Submits a request to the API.
 * 
 * @param {string} endpoint API endpoint to submit the request to.
 * @param {string} method HTTP method to use.
 * @param {*} body JSON body to submit to the API. This can be null.
 * @returns Returns a JSON object describing the success of the operation.
 */
async function queryApi(endpoint, method='GET', body=null) {
    if (typeof endpoint !== 'string' || endpoint.length == 0) {
        return apiError("Invalid parameter: `endpoint` must be a non-zero length string.");
    }
    if (typeof method !== 'string' || !validMethods.includes(method)) {
        return apiError("Invalid parameter: `method` must be a valid uppercase HTTP method.");
    }

    const csrfTokens = $('input[name=csrfmiddlewaretoken]');
    if (csrfTokens.length == 0) {
        return apiError("No CSRF token found.");
    }
    const csrfToken = csrfTokens[0].value;
    if (body != null && body.constructor == Object) {
        body = JSON.stringify(body);
    }
    try {
        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: body
        })
        return await response.json();
    } catch (error) {
        console.error(error);
        return apiError("Failed to communicate with API. Check console for more information.");
    }
}

/**
 * Queries the API for every source.
 * 
 * @returns Returns a list of every source as a JSON object.
 */
async function getSources() {
    return await queryApi('/api/source/', method='GET');
}

/**
 * Creates a new source.
 * 
 * @param {string} name Name of the source.
 * @param {string} location Location that the application should fetch the data
 * for this source from. This is typically an HTTPS endpoint.
 * @param {boolean} hasHeader A boolean that describes if the CSV provided by
 * the source contains a line for the header.
 * @returns Returns a JSON object describing the success of the operation.
 */
async function createSource(name, location, hasHeader) {
    // Validate parameters:
    if (typeof name !== 'string' && name.trim().length == 0) {
        return apiError("Invalid parameter: `name` must be a non-whitespace non-empty string.");
    }
    if (typeof location !== 'string' && location.trim().length == 0) {
        return apiError("Invalid parameter: `location` must be a non-whitespace non-empty string.");
    }
    if (typeof hasHeader !== 'boolean') {
        return apiError("Invalid parameter: 'hasHeader' must be a boolean.");
    }
    
    // Submit to the API:
    return await queryApi(
        '/api/source/',
        method = 'POST',
        body = {
            name: name.trim(),
            location: location.trim(),
            has_header: hasHeader
        }
    );
}

/**
 * Fetches information about a source.
 * 
 * @param {number} sourceId ID of the source.
 * @returns Returns a JSON object describing the success of the operation.
 */
async function getSource(sourceId) {
    // Validate parameters:
    if (typeof sourceId !== 'number' || !Number.isInteger(sourceId)) {
        return apiError("Invalid parameter: `sourceId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/source/${sourceId}/`,
        method = 'GET'
    );
}

/**
 * Deletes a source.
 * 
 * @param {number} sourceId ID of the source to delete.
 * @returns Returns a JSON object describing the success of the deletion
 * operation.
 */
async function deleteSource(sourceId) {
    // Validate parameters:
    if (typeof sourceId !== 'number' || !Number.isInteger(sourceId)) {
        return apiError("Invalid parameter: `sourceId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/source/${sourceId}/`,
        method = 'DELETE'
    );
}

/**
 * Updates the information for a given source.
 * 
 * @param {number} sourceId ID of the source.
 * @param {string} name Name of the source.
 * @param {string} location Location that the application should fetch the data
 * for this source from. This is typically an HTTPS endpoint.
 * @param {boolean} hasHeader A boolean that describes if the CSV provided by
 * the source contains a line for the header.
 * @returns Returns a JSON object describing the success of the update
 * operation.
 */
async function updateSource(sourceId, name, location, hasHeader) {
    // Validate parameters:
    if (typeof sourceId !== 'number' || !Number.isInteger(sourceId)) {
        return apiError("Invalid parameter: `sourceId` must be an integer.");
    }
    if (typeof name !== 'string' && name.trim().length == 0) {
        return apiError("Invalid parameter: `name` must be a non-whitespace non-empty string.");
    }
    if (typeof location !== 'string' && location.trim().length == 0) {
        return apiError("Invalid parameter: `location` must be a non-whitespace non-empty string.");
    }
    if (typeof hasHeader !== 'boolean') {
        return apiError("Invalid parameter: 'hasHeader' must be a boolean.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/source/${sourceId}/`,
        method = 'PUT',
        body = {
            name: name.trim(),
            location: location.trim(),
            has_header: hasHeader
        }
    );
}

/**
 * Fetches the source data.
 * 
 * @param {number} sourceId ID of the source.
 * @returns Returns a JSON object containing the source data.
 */
async function getSourceData(sourceId) {
    // Validate parameters:
    if (typeof sourceId !== 'number' || !Number.isInteger(sourceId)) {
        return apiError("Invalid parameter: `sourceId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/source/${sourceId}/data/`,
        method = 'GET'
    );
}

/**
 * Queries the API for every graph.
 * 
 * @returns Returns a list of every graph as a JSON object.
 */
async function getGraphs() {
    return await queryApi('/api/graph/', method='GET');
}

/**
 * Submits a new graph to the API.
 * 
 * @param {string} name Name of the graph. This must not be empty or consist of
 * only whitespace. Any leading or trailing whitespace characters will be
 * trimmed.
 * @param {string} description Optional description of the graph. This must be a
 * string, if no description is provided, use an empty string. Any leading or
 * trailing whitespace will be trimmed.
 * @returns 
 */
async function createGraph(name, description) {
    // Validate parameters:
    if (typeof name !== 'string' && name.trim().length == 0) {
        return apiError("Invalid parameter: `name` must be a non-whitespace non-empty string.");
    }
    if (typeof description !== 'string') {
        return apiError("Invalid parameter: `description` must be a string.");
    }

    // Submit to the API:
    return await queryApi(
        '/api/graph/',
        method='POST',
        body={
            name: name.trim(),
            description: description.trim()
        }
    );
}

/**
 * Queries the API for information about a specific graph.
 * 
 * @param {number} graphId ID of the graph to fetch information about. This
 * should be an integer.
 * @returns Returns a JSON object describing the graph.
 */
async function getGraph(graphId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/`,
        method = 'GET'
    );
}

/**
 * Requests the API to delete a specific graph.
 * 
 * @param {number} graphId ID of the graph to fetch information about. This
 * should be an integer.
 * @returns Returns a JSON object describing the success of the delete
 * operation.
 */
async function deleteGraph(graphId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/`,
        method = 'DELETE'
    );
}

/**
 * Updates the information for a given graph.
 * 
 * @param {number} graphId ID of the graph to fetch information about. This
 * should be an integer.
 * @param {string} name Name of the graph. This must not be empty or consist of
 * only whitespace. Any leading or trailing whitespace characters will be
 * trimmed.
 * @param {string} description Optional description of the graph. This must be a
 * string, if no description is provided, use an empty string. Any leading or
 * trailing whitespace will be trimmed.
 * @returns Returns a JSON object describing the success of the edit operation.
 */
async function updateGraph(graphId, name, description) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }
    if (typeof name !== 'string' && name.trim().length == 0) {
        return apiError("Invalid parameter: `name` must be a non-whitespace non-empty string.");
    }
    if (typeof description !== 'string') {
        return apiError("Invalid parameter: `description` must be a string.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/`,
        method = 'PUT',
        body = {
            name: name.trim(),
            description: description.trim()
        }
    );
}

/**
 * Queries the API for each of the datasets for a given graph.
 * 
 * @param {number} graphId ID of the graph to fetch information about. This
 * should be an integer.
 * @returns Returns a JSON object containing each of the datasets for the given
 * graph.
 */
async function getGraphDatasets(graphId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/dataset/`,
        method = 'GET',
    );
}

/**
 * Creates a new dataset for a given graph.
 * 
 * @param {number} graphId ID of the graph to fetch information about. This
 * should be an integer.
 * @param {string} label Label to display for the dataset. This is what will be
 * displayed in the hero for the graph.
 * @param {string} plotType Method to use for plotting the graph.
 * @param {boolean} isAxis A boolean that describes if this dataset should be
 * plotted as the y-axis on the graph.
 * @param {number} sourceId ID of the source of data for this dataset.
 * @param {number} columnId ID of the column within the data from the source
 * that should be used as the dataset.
 * @returns Returns a JSON object describing the success of the operation.
 */
async function createGraphDataset(graphId, label, plotType, isAxis, sourceId, columnId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }
    if (typeof label !== 'string') {
        return apiError("Invalid parameter: `label` must be a string.");
    }
    if (typeof plotType !== 'string' || !validPlotTypes.includes(plotType)) {
        return apiError("Invalid parameter: `plotType` must be a supported string plot-type.");
    }
    if (typeof isAxis !== 'boolean') {
        return apiError("Invalid parameter: `isAxis` must be a boolean.");
    }
    if (typeof sourceId !== 'number' || !Number.isInteger(sourceId)) {
        return apiError("Invalid parameter: `sourceId` must be an integer.");
    }
    if (typeof columnId !== 'number' || !Number.isInteger(columnId) || columnId < 0) {
        return apiError("Invalid parameter: `columnId` must be a positive integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/dataset/`,
        method = 'POST',
        body = {
            label: label.trim(),
            plot_type: isAxis ? 'none' : plotType,
            is_axis: isAxis,
            source_id: sourceId,
            column_id: columnId,
        }
    );
}

/**
 * Queries the API for information about a particular dataset on a graph.
 * 
 * @param {number} graphId ID of the graph to fetch information about. This
 * should be an integer.
 * @param {number} datasetId ID of the dataset on the graph to fetch information
 * about. This should be an integer.
 * @returns Returns a JSON object describing the dataset.
 */
async function getGraphDataset(graphId, datasetId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }
    if (typeof datasetId !== 'number' || !Number.isInteger(datasetId)) {
        return apiError("Invalid parameter: `datasetId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/dataset/${datasetId}/`,
        method = 'GET'
    );
}

/**
 * Requests the API delete a particular dataset on a graph.
 * 
 * @param {number} graphId ID of the graph to delete. This
 * @param {number} datasetId ID of the dataset on the graph to delete.
 * @returns Returns a JSON object describing the success of the operation.
 */
async function deleteGraphDataset(graphId, datasetId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }
    if (typeof datasetId !== 'number' || !Number.isInteger(datasetId)) {
        return apiError("Invalid parameter: `datasetId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/dataset/${datasetId}/`,
        method = 'DELETE'
    );
}

/**
 * Updates a dataset on a graph.
 * 
 * @param {number} graphId ID of the graph to update.
 * @param {number} datasetId ID of the dataset on the graph to update.
 * @param {string} label Label to display for the dataset. This is what will be
 * displayed in the hero for the graph.
 * @param {string} plotType Method to use for plotting the graph.
 * @param {boolean} isAxis A boolean that describes if this dataset should be
 * plotted as the y-axis on the graph.
 * @param {number} sourceId ID of the source of data for this dataset.
 * @param {number} columnId ID of the column within the data from the source
 * that should be used as the dataset.
 * @returns Returns a JSON object describing the success of the operation.
 */
async function updateGraphDataset(graphId, datasetId, label, plotType, isAxis, sourceId, columnId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }
    if (typeof datasetId !== 'number' || !Number.isInteger(datasetId)) {
        return apiError("Invalid parameter: `datasetId` must be an integer.");
    }
    if (typeof label !== 'string') {
        return apiError("Invalid parameter: `label` must be a string.");
    }
    if (typeof plotType !== 'string' || !validPlotTypes.includes(plotType)) {
        return apiError("Invalid parameter: `plotType` must be a supported string plot-type.");
    }
    if (typeof isAxis !== 'boolean') {
        return apiError("Invalid parameter: `isAxis` must be a boolean.");
    }
    if (typeof sourceId !== 'number' || !Number.isInteger(sourceId)) {
        return apiError("Invalid parameter: `sourceId` must be an integer.");
    }
    if (typeof columnId !== 'number' || !Number.isInteger(columnId) || columnId < 0) {
        return apiError("Invalid parameter: `columnId` must be a positive integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/dataset/${datasetId}/`,
        method = 'PUT',
        body = {
            label: label.trim(),
            plot_type: isAxis ? 'none' : plotType,
            is_axis: isAxis,
            source_id: sourceId,
            column_id: columnId,
        }
    );
}

/**
 * Requests the ChartJs data to plot for a given graph.
 * 
 * @param {number} graphId ID of the graph to fetch the ChartJs data for.
 * @returns Returns a JSON object containing the ChartJs data to plot for the
 * graph.
 */
async function getGraphChartJsData(graphId) {
    // Validate parameters:
    if (typeof graphId !== 'number' || !Number.isInteger(graphId)) {
        return apiError("Invalid parameter: `graphId` must be an integer.");
    }

    // Submit to the API:
    return await queryApi(
        `/api/graph/${graphId}/data/`,
        method = 'GET',
    );
}

/**
 * Gets a URL parameter from the URL.
 * 
 * @param {string} param Name of the parameter to fetch.
 * @returns Returns the value of the URL parameter, if it was not found,
 * undefined is returned instead.
 */
function getUrlParameter(param) {
    var url = window.location.search.substring(1), urlQuery = url.split('&'), paramName, i;
    for (i = 0; i < urlQuery.length; i++) {
        paramName = urlQuery[i].split('=');
        if (paramName[0] === param) {
            return paramName[1] === undefined ? true : decodeURIComponent(paramName[1]);
        }
    }
    return undefined;
};