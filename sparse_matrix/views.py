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
    if request.method=='POST':
        file_ = str(request.FILES.get('input_', None))
        import time
        start_time = time.time()
        length_matrix = len(CSM(file_))
        encrypt_CSM(file_)
        decrypt_CSM(encrypt_CSM(file_))
        sparseMatrix(decrypt_CSM(encrypt_CSM(file_)))
        data['result'] = str(time.time() - start_time)
        save_in_db['processing_time'] = data['result']
        save_in_db['length'] = length_matrix
        newSparse = Sparse(**save_in_db)
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
        latest_time_list = Sparse.objects.values(
            'processing_time').order_by('-id')[:5]
        all_processing_time = [p1['processing_time']
                               for p1 in latest_time_list]
        # import pdb; pdb.set_trace()

        return [all_processing_time]

    line_chart = TemplateView.as_view(template_name='sparse.html')
line_chart_json = LineChartJSONView.as_view()
