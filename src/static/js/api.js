async function queryApi(endpoint, method='GET', body=null) {
    const csrfTokens = $('input[name=csrfmiddlewaretoken]');
    if (csrfTokens.length == 0) {
        return {
            result: 'error',
            message: 'No CSRF token found.'
        };
    }
    const csrfToken = csrfTokens[0].value;
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            body: body
        })
        return await response.json();
    } catch (error) {
        return {
            result: 'error',
            message: error
        }
    }
}