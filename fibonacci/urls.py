from django.conf.urls import url

from . import views
# from fibonacci.views import LineChartJSONView

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    # url(r'^(?P<fibonacci_id>[0-9]+)/$', views.output, name='output'),
    url(r'^result/', views.result, name='result'),
    # url(r'^fibonacci/', views.sparse, name='fibonacci'),
    # url(r'^fibonacci_json$', LineChartJSONView.as_view(), name="line_chart_json"),
    # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
