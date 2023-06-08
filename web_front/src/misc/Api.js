export const callApi = (url, method = 'GET', body = null) => {
    const requestOptions = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };
  
    if (body) {
      requestOptions.body = JSON.stringify(body);
    }
  
    return fetch(url, requestOptions)
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
  