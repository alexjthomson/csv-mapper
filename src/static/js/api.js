async function queryApi(endpoint, method='GET', body=null) {
    const csrfTokens = $('input[name=csrfmiddlewaretoken]');
    if (csrfTokens.length == 0) {
        console.error('No CSRF token found.');
        return {
            result: 'error',
            message: 'No CSRF token found.'
        };
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
        return {
            result: 'error',
            message: error
        }
    }
}
function formToJson($form) {
    json = {};
    $form.find('.form-control').each(function () {
        json[this.name] = this.value;
    });
    $form.find('.form-check-input').each(function () {
        json[this.name] = this.checked;
    });
    return json;
}