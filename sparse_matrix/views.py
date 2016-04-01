from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import json

from .models import Sparse
from sparse_matrix.utils import *


def index(request,):
    template = loader.get_template('sparse_matrix/index.html')
    return HttpResponse(template.render(request))


def output(request, sparse_id):
    return HttpResponse("You're looking at processing time %s." % sparse_id)


@csrf_exempt
def result(request):
    '''
        View to add all the tracking resources
    '''

    status,response = set_response_header(request=request,response=HttpResponse(content_type='application/json'))
    if not status:
        return HttpResponseBadRequest(json.dumps({"Message":"Unauthorized request"}),content_type='application/json')
    data = {'result': ''}
    save_in_db = {}
    # file_ = request.FILES.get('input_')

    if request.method=='POST':
        file_ = request.POST.get('input_', None)
        
        # import pdb; pdb.set_trace()
        import time
        length_matrix = len(CSM(file_))

        start_time1 = time.time()
        encrypt_CSM_linear(file_)
        decrypt_CSM_linear(encrypt_CSM_linear(file_))
        data['result_linear'] = str(time.time() - start_time1)

        start_time2 = time.time()
        encrypt_CSM_quadratic(file_)
        decrypt_CSM_quadratic(encrypt_CSM_quadratic(file_))
        data['result_quadratic'] = str(time.time() - start_time2)
        
        start_time3 = time.time()
        encrypt_CSM_cubic(file_)
        decrypt_CSM_cubic(encrypt_CSM_cubic(file_))
        data['result_cubic'] = str(time.time() - start_time3)

        save_in_db['processing_time_l'] = data['result_linear']
        save_in_db['processing_time_q'] = data['result_quadratic']
        save_in_db['processing_time_c'] = data['result_cubic']
        save_in_db['length'] = length_matrix
        newSparse = Sparse(**save_in_db)
        length_in_sparse = Sparse.objects.values('length')
        all_lengths = [p['length'] for p in length_in_sparse]
        if length_matrix in all_lengths:
            pass
        else:
            newSparse.save()
        response.write("%s"%(json.dumps(data)))
    return response





@csrf_exempt
def sparse(request):
    return render_to_response('sparse_matrix/sparse.html', context_instance=RequestContext(request))


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        latest_length_list = Sparse.objects.values(
            'length').order_by('-id')[:5]
        all_lengths = [p['length'] for p in latest_length_list]
        return all_lengths

    def get_data(self):
        """Return 3 datasets to plot."""
        latest_time_linear = Sparse.objects.values(
            'processing_time_l').order_by('-length')[:15]
        all_processing_linear = [p1['processing_time_l']
                               for p1 in latest_time_linear]
        
        latest_time_quadratic = Sparse.objects.values(
            'processing_time_q').order_by('-length')[:15]
        all_processing_quadratic = [p1['processing_time_q']
                               for p1 in latest_time_quadratic]

        latest_time_cubic = Sparse.objects.values(
            'processing_time_c').order_by('-length')[:15]
        all_processing_cubic = [p1['processing_time_c']
                               for p1 in latest_time_cubic]
        # import pdb; pdb.set_trace()

        return [all_processing_linear,all_processing_quadratic, all_processing_cubic] 

    
line_chart = TemplateView.as_view(template_name='sparse.html')
line_chart_json = LineChartJSONView.as_view()
