# **What is this?**
#### This is a basic [Bitkub](https://www.bitkub.com)'s API.
#### It has all [Bitkub Restful API](https://github.com/bitkub/bitkub-official-api-docs/blob/master/restful-api.md) functions, and some useful functions.

## **How to install?**
You can install by

``pip install Bitkub-Api``


## **How to use?**
#### You can use by

```
from Bitkub_Api.bitkub_api import Bitkub

api_key = 'YOUR_API_KEY'
api_secret = b'YOUR_API_SECRET'

bitkub = Bitkub(api_key, api_secret)

print(bitkub.servertime())
```
#### Output
``1620754498``


## **Is there a documentation?**
#### no but you can use this [documentation (bitkub restful api)](https://github.com/bitkub/bitkub-official-api-docs/blob/master/restful-api.md)