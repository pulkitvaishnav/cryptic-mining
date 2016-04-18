from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from random import randint
from django.views.generic import TemplateView
# from chartjs.views.lines import BaseLineChartView
import json
from sympy import *
import numpy as np
from .models import Fibonacci
from fibonacci.utils import *


def index(request):
    return render_to_response('fibonacci/index.html', context_instance=RequestContext(request))


@csrf_exempt
def result(request):
    status, response = set_response_header(
        request=request, response=HttpResponse(content_type='application/json'))
    data = {'iterative_time': '', 'recursive_time': '', 'fibonacci_no': ''}
    if request.method == 'POST':
        fibo_number = request.POST.get('input_', None)
        plain_text = request.POST.get('input_plain', None)
        # import pdb; pdb.set_trace()
        import time
        start_time_iterative = time.time()
        number = iterative_fibo(fibo_number)
        end_iterative = time.time()
        start_time_recursive = time.time()
        recursive_fibo(fibo_number)
        data['iterative_time'] = end_iterative - start_time_iterative
        data['recursive_time'] = time.time() - start_time_recursive
        data['fibonacci_no'] = number
        fibo_matrix = Matrix([[number + 1, number], [number, number - 1]])
        fibo_inverse = fibo_matrix**-1
        plain_text = list(plain_text)
        plain_text_matrix = []
        for elements in plain_text:
            plain_text_matrix.append(ord(elements))
        if len(plain_text_matrix) % 2:
            plain_text_matrix.append(32)
        plain_text_matrix = Matrix(np.reshape(
            plain_text_matrix, (len(plain_text_matrix) / 2, 2)))
        
        encrypted_matrix = plain_text_matrix * fibo_matrix
        decrytped_matrix = encrypted_matrix * fibo_inverse
        
        newFibo = Fibonacci(**data)
        latest_fibonacci = Fibonacci.objects.values('fibonacci_no')
        all_fibonacci = [p['fibonacci_no'] for p in latest_fibonacci]
        if number in all_fibonacci:
            pass
        else:
            newFibo.save()

        #import pdb; pdb.set_trace()
        encrypted_matrix = str(encrypted_matrix.tolist())
        data['fibo_matrix'] = str(fibo_matrix)
        data['fibo_inverse'] = str(fibo_inverse)
        data['plain_text_matrix'] = str(plain_text_matrix)
        data['decrypted_matrix'] = str(decrytped_matrix)
        data['encrypted_matrix'] = json.dumps(encrypted_matrix)
        response.write("%s" % (json.dumps(data)))
    return response


# class LineChartJSONView(BaseLineChartView):
#     def get_labels(self):
#         """Return 7 labels."""
#         latest_fibonacci = Fibonacci.objects.values(
#             'fibonacci_no').order_by('fibonacci_no')[:5]
#         all_fibonacci = [p['fibonacci_no'] for p in latest_fibonacci]
#         return all_fibonacci

#     def get_data(self):
#         """Return 3 datasets to plot."""
#         latest_iterative_list = Fibonacci.objects.values(
#             'iterative_time').order_by('-id')[:5]
#         latest_recursive_list = Fibonacci.objects.values(
#             'recursive_time').order_by('-id')[:5]
#         i_time = [p1['iterative_time'] for p1 in latest_iterative_list]
#         r_time = [p2['recursive_time'] for p2 in latest_recursive_list]
#         return [r_time, i_time]

# line_chart = TemplateView.as_view(template_name='index.html')
# line_chart_json = LineChartJSONView.as_view()
