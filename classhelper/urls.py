from django.conf.urls import patterns, include, url


urlpatterns = patterns('classhelper.views',
    url(r'^$', 'index', name='index'),
    url(r'^subject/new', 'subjectview', name='subject_new'),
    url(r'^subject/(?P<subject_id>\d+)/$', 'subject_details', name='subject_details'),
    url(r'^subject/(?P<subject_id>\d+)/edit$', 'subjectview', name='subject_edit'),
    url(r'^assessment/new/(?P<subject_id>\d+)/$', 'assessmentview', name='assessment_new'),
    url(r'^jsongrades/$', 'get_JSON_grades', name='get_JSON_grades'),
    url(r'^jsonsubjects/$', 'get_JSON_subjects', name='get_JSON_subects'),
    url(r'^document/new/(?P<subject_id>\d+)/$', 'document_view', name='document_view'),
)
