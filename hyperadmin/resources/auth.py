from django.conf.urls.defaults import patterns, url
from django.utils.functional import update_wrapper
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from hyperadmin import views

from resources import CRUDResource #TODO singleton resource

class AuthenticationResourceForm(AuthenticationForm):
    def save(self, commit=True):
        assert self.request
        user = self.get_user()
        login(self.request, user)
        return user

class AuthResource(CRUDResource):
    form_class = AuthenticationResourceForm
    
    detail_view = views.AuthenticationResourceView
    
    def __init__(self, **kwargs):
        self._app_name = kwargs.pop('app_name', '_authentication')
        self._resource_name = kwargs.pop('resource_name', 'auth')
        kwargs.setdefault('resource_adaptor', None)
        super(AuthResource, self).__init__(**kwargs)
    
    def get_app_name(self):
        return self._app_name
    app_name = property(get_app_name)
    
    def get_resource_name(self):
        return self._resource_name
    resource_name = property(get_resource_name)
    
    def get_urls(self):
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.as_nonauthenticated_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        init = self.get_view_kwargs()
        
        # Admin-site-wide views.
        urlpatterns = self.get_extra_urls()
        urlpatterns += patterns('',
            url(r'^$',
                wrap(self.detail_view.as_view(**init)),
                name='authentication'),
        )
        return urlpatterns
    
    def get_form_class(self):
        return self.form_class
    
    def get_instance_url(self, instance):
        return self.get_absolute_url()
    
    def get_absolute_url(self):
        return self.reverse('authentication')
    
    def get_outbound_links(self, instance=None):
        return []

