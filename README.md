# exceptions_and_logging

A **Django app** for logging custom application errors on the server side and also spits out JSON error info on the client side. You basically subclass our ```ApplicationErrors``` class and the rest is done for you.



**Dependencies**

- Django Rest Framework
- PyYaml



**Installation**

In your virtual environment run:

```pip install exceptions_and_logging``` 



**Usage**

1. Add ```exceptions_and_logging```  to your Django installed apps:

```python
# settings.py

INSTALLED_APPS = [
    ...
    
    'exceptions_and_logging',
]
```



2. Without logging config.

```python
# your_app.exceptions.py (or wherever your app exceptions are)

from exceptions_and_logging.exceptions import ApplicationErrors

class MyCustomException(ApplicationErrors):
    default_message = "This item: '%(item_name)s' isn't supposed to be null"

    def __init__(self, item_name):
        message = self.default_message % {"item_name": item_name}
        super().__init__(message)

```

When this error is raised:

- Generated response on the client side (via Rest Framework):

  - ```json
    {
      "error":{
          "type":"MyCustomException",
          "message":"This item: 'SomeItem' isn't supposed to be null",
          "code":"error"
          }
    }
    ```

  - An HTTP 500 Application Error response is returned.

- Generated log on the server console (stdout):

  - ```
    02/15/2021 04:30:34 PM - APPLICATION ERROR - ERROR
    Error Type: MyCustomException
    Error Message: This item: 'SomeItem' isn't supposed to be null
    Traceback (most recent call last):
      # Bunch of traceback info
      ...
      ...
        raise NullError("SomeItem")
    your_app.exceptions.MyCustomException: This item: 'SomeItem' isn't supposed to be null
    ```



3. With Logging Config

```python
# your_app.exceptions.py (or wherever your app exceptions are)

from exceptions_and_logging.exceptions import ApplicationErrors

# Path to your logging config file
module_dir = os.path.dirname(__file__)
config_file = os.path.join(module_dir, "myconfig.yaml")

class MyCustomException(ApplicationErrors):
    default_message = "This item: '%(item_name)s' isn't supposed to be null"
    log_config = config_file 	# Can also be a dict config
	
    # If no logger name is passed, it will use the default logger name.
    def __init__(self, item_name, logger_name=None):
        message = self.default_message % {"item_name": item_name}
        super().__init__(message, logger_name=logger_name)
        
```

- The ```ApplicationError``` class provides hooks for adding extra format strings to the logging message and also extra key, value pairs for the error dict.

- ```python
  # Assuming your formatter has extra values like user_id and user_email
  msg_format = '%(asctime)s - APPLICATION ERROR - %(levelname)s\n' \
               'User Email: %(user_email)s\n' \
      	     'User ID: %(user_id)s\n'\
               'Error Message: %(message)s\n'
              
  class MyCustomException(ApplicationErrors):
      def __init__(self, user_id, user_email, **err_dict_kwargs):
          self.user_id, self.user_email = user_id, user_email
          super().__init__(**err_dict_kwargs)
      
      # Override this method to return extra kwargs for logging
      def extra_kwargs(self) -> dict:
          dict_ = {
              "user_id": self.user_id,
              "user_email": self.user_email
          }
          return dict_
  ```

  ```python
  # in views.py
  
  from rest_framework.views import APIView
  
  from .exceptions import MyCustomException
  
  class TestException(APIView):
  
      def get(self, request):
          raise MyCustomException(
          	"id4", "name@gmail.com", foo="bar", hot="soup"
          	)
  
  ```

  Generated response on the client side via Rest Framework:

  ```json
  {
      "error":{
          "type":"MyCustomException",
          "message":"An application error occurred.",
          "code":"error",
          "foo":"bar",
          "hot":"soup"
      }
  }
  ```

  
