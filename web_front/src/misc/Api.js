import Cookies from "js-cookie";

const backendUrl = "http://127.0.0.1:8000/";

const updateToken = () => {
    const accessToken = Cookies.get("accessToken");
    const refreshToken = Cookies.get("refreshToken");

    if (!accessToken) {
      return;
    }
    
    console.log("Updating token");

    fetch(backendUrl+"api/token/verify/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({token: accessToken})
    }).then((response) => {
      if(!response.ok) {
        const body = {
          refresh: refreshToken,
          access: accessToken
        }
        fetch(backendUrl+"api/token/refresh/", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(body)
        }).then((response) => {
          if (response.ok) {
            const { newToken } = response; 
            Cookies.set("accessToken", newToken);
          }
        })
      }
    });  
}

export const callApi = (path, method = 'GET', body = null) => {
    updateToken();
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
    console.log(requestOptions);
    return fetch(endpointUrl, requestOptions)
      .then((response) => {
        if (!response.ok) {
          console.log(response);
          throw new Error('API request failed');
        }
        return response.json();
      })
      .catch((error) => {
        console.error('API request error:', error);
        throw error;
      });
  };
  