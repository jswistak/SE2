import Cookies from "js-cookie";

const backendUrl = "http://127.0.0.1:8000/";

export const callApi = (path, method = 'GET', body = null) => {
    const endpointUrl = backendUrl + path;
    const jwtToken = Cookies.get("accessToken");
    
    const headers = {
      'Content-Type': 'application/json',
    }

    if (jwtToken) {
      headers.Authorization = `Bearer ${jwtToken}`;
    }

    console.log(endpointUrl)
    const requestOptions = {
      method,
      headers: headers
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
  