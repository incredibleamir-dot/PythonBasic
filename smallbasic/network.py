import urllib.request
import urllib.parse
import json
from typing import Optional, Dict, Any, Union


class Network:
    """
    Provides methods to access network resources and make REST API calls.
    
    Supports GET, POST, PUT, DELETE requests with JSON or form data.
    
    Usage:
        # Simple GET
        html = Network.GetWebPageContents("https://api.example.com")
        
        # REST API with JSON
        data = Network.Get("https://api.example.com/users")
        result = Network.Post("https://api.example.com/users", 
                              {"name": "John", "age": 30})
        Network.Put("https://api.example.com/users/1", {"name": "Jane"})
        Network.Delete("https://api.example.com/users/1")
        
        # Download a file
        path = Network.DownloadFile("https://example.com/image.png")
    """

    _headers = {
        "User-Agent": "SmallBasicPython/1.0",
        "Accept": "application/json, text/plain, */*",
    }

    @classmethod
    def GetWebPageContents(cls, url: str) -> str:
        """
        Gets the contents of a web page as text.
        
        Args:
            url: The URL to fetch.
            
        Returns:
            The text content of the web page, or error message.
        """
        try:
            req = urllib.request.Request(url, headers=cls._headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    def DownloadFile(cls, url: str) -> str:
        """
        Downloads a file from the internet and saves it locally.
        
        Args:
            url: The URL of the file to download.
            
        Returns:
            The local file path of the downloaded file, or error message.
        """
        try:
            import os
            import tempfile
            filename = os.path.basename(urllib.parse.urlparse(url).path)
            if not filename:
                filename = "downloaded_file"
            local_path = os.path.join(tempfile.gettempdir(), filename)
            urllib.request.urlretrieve(url, local_path)
            return local_path
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    def _request(cls, method: str, url: str,
                 data: Any = None,
                 headers: Optional[Dict[str, str]] = None,
                 json_data: bool = True) -> str:
        """
        Internal method to make HTTP requests.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            url: The URL to request.
            data: The data to send (dict or string).
            headers: Additional headers.
            json_data: If True, send data as JSON. If False, form-encoded.
            
        Returns:
            The response body as text.
        """
        all_headers = cls._headers.copy()
        if headers:
            all_headers.update(headers)

        body = None
        if data is not None:
            if isinstance(data, str):
                body = data.encode("utf-8")
                all_headers["Content-Type"] = "text/plain"
            elif json_data:
                body = json.dumps(data).encode("utf-8")
                all_headers["Content-Type"] = "application/json"
            else:
                body = urllib.parse.urlencode(data).encode("utf-8")
                all_headers["Content-Type"] = "application/x-www-form-urlencoded"

        try:
            req = urllib.request.Request(url, data=body, headers=all_headers,
                                         method=method)
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode("utf-8", errors="replace")
                return content
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            return f"HTTP {e.code}: {e.reason}\n{error_body}"
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    def Get(cls, url: str,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, str]] = None) -> str:
        """
        Makes a GET request to a REST API.
        
        Args:
            url: The URL to request.
            headers: Optional HTTP headers.
            params: Optional query parameters to append to the URL.
            
        Returns:
            The response body as text (usually JSON).
            
        Example:
            users = Network.Get("https://api.example.com/users")
            user = Network.Get("https://api.example.com/users/1")
        """
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return cls._request("GET", url, headers=headers)

    @classmethod
    def Post(cls, url: str,
             data: Any = None,
             headers: Optional[Dict[str, str]] = None,
             as_json: bool = True) -> str:
        """
        Makes a POST request to a REST API.
        
        Args:
            url: The URL to request.
            data: The data to send (dict or string).
            headers: Optional HTTP headers.
            as_json: Send data as JSON (True) or form-encoded (False).
            
        Returns:
            The response body as text.
            
        Example:
            result = Network.Post("https://api.example.com/users",
                                  {"name": "John", "age": 30})
        """
        return cls._request("POST", url, data=data, headers=headers,
                            json_data=as_json)

    @classmethod
    def Put(cls, url: str,
            data: Any = None,
            headers: Optional[Dict[str, str]] = None,
            as_json: bool = True) -> str:
        """
        Makes a PUT request to a REST API (update a resource).
        
        Args:
            url: The URL to request.
            data: The data to send (dict or string).
            headers: Optional HTTP headers.
            as_json: Send data as JSON (True) or form-encoded (False).
            
        Returns:
            The response body as text.
            
        Example:
            Network.Put("https://api.example.com/users/1",
                        {"name": "Jane"})
        """
        return cls._request("PUT", url, data=data, headers=headers,
                            json_data=as_json)

    @classmethod
    def Delete(cls, url: str,
               headers: Optional[Dict[str, str]] = None) -> str:
        """
        Makes a DELETE request to a REST API.
        
        Args:
            url: The URL to request.
            headers: Optional HTTP headers.
            
        Returns:
            The response body as text.
            
        Example:
            Network.Delete("https://api.example.com/users/1")
        """
        return cls._request("DELETE", url, headers=headers)

    @classmethod
    def Patch(cls, url: str,
              data: Any = None,
              headers: Optional[Dict[str, str]] = None,
              as_json: bool = True) -> str:
        """
        Makes a PATCH request to a REST API (partial update).
        
        Args:
            url: The URL to request.
            data: The data to send.
            headers: Optional HTTP headers.
            as_json: Send data as JSON (True) or form-encoded (False).
            
        Returns:
            The response body as text.
        """
        return cls._request("PATCH", url, data=data, headers=headers,
                            json_data=as_json)
