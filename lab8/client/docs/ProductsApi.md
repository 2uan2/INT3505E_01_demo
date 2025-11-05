# swagger_client.ProductsApi

All URIs are relative to *http://localhost:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_products_get**](ProductsApi.md#api_v1_products_get) | **GET** /api/v1/products | Returns list of all products
[**api_v1_products_id_delete**](ProductsApi.md#api_v1_products_id_delete) | **DELETE** /api/v1/products/{id} | Delete product using id
[**api_v1_products_id_get**](ProductsApi.md#api_v1_products_id_get) | **GET** /api/v1/products/{id} | Getting product by id
[**api_v1_products_id_patch**](ProductsApi.md#api_v1_products_id_patch) | **PATCH** /api/v1/products/{id} | Edit a product using id
[**api_v1_products_id_put**](ProductsApi.md#api_v1_products_id_put) | **PUT** /api/v1/products/{id} | Edit a product using id
[**api_v1_products_post**](ProductsApi.md#api_v1_products_post) | **POST** /api/v1/products | Creates a new product

# **api_v1_products_get**
> list[ProductResponse] api_v1_products_get()

Returns list of all products

Returns list of all products

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProductsApi()

try:
    # Returns list of all products
    api_response = api_instance.api_v1_products_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProductsApi->api_v1_products_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ProductResponse]**](ProductResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_products_id_delete**
> str api_v1_products_id_delete(id)

Delete product using id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProductsApi()
id = 789 # int | Product's id

try:
    # Delete product using id
    api_response = api_instance.api_v1_products_id_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProductsApi->api_v1_products_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Product&#x27;s id | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_products_id_get**
> ProductResponse api_v1_products_id_get(id)

Getting product by id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProductsApi()
id = 789 # int | Product's id

try:
    # Getting product by id
    api_response = api_instance.api_v1_products_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProductsApi->api_v1_products_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Product&#x27;s id | 

### Return type

[**ProductResponse**](ProductResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_products_id_patch**
> ProductResponse api_v1_products_id_patch(body, id)

Edit a product using id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProductsApi()
body = swagger_client.ProductPatchRequest() # ProductPatchRequest | Describe product to be edited
id = 789 # int | Product's id

try:
    # Edit a product using id
    api_response = api_instance.api_v1_products_id_patch(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProductsApi->api_v1_products_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProductPatchRequest**](ProductPatchRequest.md)| Describe product to be edited | 
 **id** | **int**| Product&#x27;s id | 

### Return type

[**ProductResponse**](ProductResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_products_id_put**
> ProductResponse api_v1_products_id_put(body, id)

Edit a product using id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProductsApi()
body = swagger_client.ProductCreateRequest() # ProductCreateRequest | Describe product to be edited
id = 789 # int | Product's id

try:
    # Edit a product using id
    api_response = api_instance.api_v1_products_id_put(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProductsApi->api_v1_products_id_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProductCreateRequest**](ProductCreateRequest.md)| Describe product to be edited | 
 **id** | **int**| Product&#x27;s id | 

### Return type

[**ProductResponse**](ProductResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_products_post**
> ProductResponse api_v1_products_post(body)

Creates a new product

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProductsApi()
body = swagger_client.ProductCreateRequest() # ProductCreateRequest | Parameters for new product

try:
    # Creates a new product
    api_response = api_instance.api_v1_products_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProductsApi->api_v1_products_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProductCreateRequest**](ProductCreateRequest.md)| Parameters for new product | 

### Return type

[**ProductResponse**](ProductResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

