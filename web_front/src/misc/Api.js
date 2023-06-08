const backendUrl = "http://127.0.0.1:8000/";

export const callApi = (path, method = 'GET', body = null) => {
    const endpointUrl = backendUrl + path;
    const requestOptions = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };
  
    if (body) {
      requestOptions.body = JSON.stringify(body);
    }
  
    return fetch(endpointUrl, requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error('API request failed');
        }
        return response.json();
      })
      .catch((error) => {
        console.error('API request error:', error);
        throw error;
      });
  };
  