import re
import json
from django.http import HttpRequest, HttpResponse

whitedomain_list = ['127.0.0.1:8000','localhost:8000']
whitehost_list = ['127.0.0.1:8000', 'localhost:8000']

def recursive_fibo(input_):
    input_ = int(input_)
    if input_ == 0:
        return 0
    elif input_ == 1:
        return 1
    else:
        return recursive_fibo(input_ - 1) + recursive_fibo(input_ - 2)


def iterative_fibo(input_):
    input_ = int(input_)
    if input_ == 0:
        return 0
    elif input_ == 1:
        return 1
    else:
        a, b = 0, 1
        for i in range(input_):
            a, b = b, a + b
        return a

def set_response_header(**kwargs):
    #pdb.set_trace()
    pattern=re.compile("^chrome-extension://*")
    if isinstance(kwargs['request'],HttpRequest) and isinstance(kwargs['response'],HttpResponse):
        if kwargs['request'].META.has_key('HTTP_ORIGIN') and kwargs['request'].META['HTTP_ORIGIN'] in whitedomain_list:
            kwargs['response']['Access-Control-Allow-Credentials']='true'
            kwargs['response']['Access-Control-Allow-Methods']="GET, POST, OPTIONS, DELETE, PUT"
            kwargs['response']['Access-Control-Allow-Origin']="*"
            #kwargs['response']['Access-Control-Allow-Origin']="http://web-staging.flyrobeapp.com/, http://localhost:8000/"
            kwargs['response']['Access-Control-Max-Age']="1728000"
            kwargs['response']['Cache-Control']="max-age=0, private, must-revalidate"
            kwargs['response'].__delitem__("X-Frame-Options")
            return True,kwargs['response']
        elif kwargs['request'].META.has_key('HTTP_ORIGIN') and pattern.match(kwargs['request'].META['HTTP_ORIGIN']):
            return True,kwargs['response']
        elif kwargs['request'].META.has_key('HTTP_HOST') and kwargs['request'].META['HTTP_HOST'] in whitehost_list:
            kwargs['response']['Access-Control-Allow-Credentials']='true'
            kwargs['response']['Access-Control-Allow-Methods']="GET, POST, OPTIONS, DELETE, PUT"
            kwargs['response']['Access-Control-Allow-Origin']="*"
            #kwargs['response']['Access-Control-Allow-Origin']="http://web-staging.flyrobeapp.com/, http://localhost:8000/"
            kwargs['response']['Access-Control-Max-Age']="1728000"
            kwargs['response']['Cache-Control']="max-age=0, private, must-revalidate"
            kwargs['response'].__delitem__("X-Frame-Options")
            return True,kwargs['response']
        elif not kwargs['request'].META.has_key('HTTP_ORIGIN') and not kwargs['request'].META.has_key('HTTP_HOST'):
            return True,kwargs['response']
    else:
        return False,kwargs['response']

