from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from confirmaction.views import ConfirmCodeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^api/v1/confirm/(?P<pk>\d+)/',
        ConfirmCodeView.as_view(),
        name='confirm-action'
    )
)
