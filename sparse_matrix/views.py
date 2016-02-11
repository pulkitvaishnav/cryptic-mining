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
    if request.method=='POST':
        file_ = str(request.FILES.get('input_', None))
        import time
        start_time = time.time()
        length_matrix = CSM(file_)
        encrypt_CSM(file_)
        decrypt_CSM(encrypt_CSM(file_))
        sparseMatrix(decrypt_CSM(encrypt_CSM(file_)))
        data['result'] = str(time.time() - start_time)
        #import pdb; pdb.set_trace()
        response.write("%s"%(json.dumps(data)))
    return response





def sparse(request):
    # latest_time_list = Sparse.objects.order_by('-length')[:1]
    # output = ', '.join([str(p.processing_time) for p in latest_time_list])
    template = loader.get_template('sparse_matrix/sparse.html')
    if request.POST.has_key('client_response'):
        file_ = str(request.FILES['input_'])
        import time
        start_time = time.time()
        length_matrix = CSM(file_)
        encrypt_CSM(file_)
        decrypt_CSM(encrypt_CSM(file_))
        sparseMatrix(decrypt_CSM(encrypt_CSM(file_)))
        validated_data = {
            'processing_time': time.time() - start_time, 'length': len(length_matrix)
        }
        sparse_instance = Sparse.objects.create(**validated_data)
        response_dict = {}
        response_dict.update({'sparse_result': time.time() - start_time})
        return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')
    else:
        return render_to_response('sparse_matrix/sparse.html', context_instance=RequestContext(request))


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        latest_length_list = Sparse.objects.values(
            'length').order_by('-id')[:20]
        all_lengths = [p['length'] for p in latest_length_list]
        return all_lengths

    def get_data(self):
        """Return 3 datasets to plot."""
        latest_time_list = Sparse.objects.values(
            'processing_time').order_by('-id')[:20]
        all_processing_time = [p1['processing_time']
                               for p1 in latest_time_list]
        # import pdb; pdb.set_trace()

        return [all_processing_time]

    line_chart = TemplateView.as_view(template_name='sparse.html')
# line_chart_json = LineChartJSONView.as_view()
