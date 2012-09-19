import urllib

from hyperadmin.resources.storages.views import BoundFile
from hyperadmin.hyperobjects import Link
from hyperadmin.resources.crud.changelist import ChangeList

class StoragePaginator(object):
    #count, num_pages, object_list
    def __init__(self, index, storage):
        self.dirs, self.files = index
        self.storage = storage
        
        self.count = len(self.files)
        self.num_pages = 1
        
        self.links, self.instances = self.get_links_and_instances()
        self.object_list = self.instances
    
    def get_links_and_instances(self):
        items = list()
        for file_name in self.files:
            items.append(BoundFile(self.storage, file_name))
        
        links = list()
        for directory in self.dirs:
            url = './?%s' % urllib.urlencode({'path':directory})
            link = Link(url=url, resource=self, prompt=u"Directory: %s" % directory, classes=['filter', 'directory'], rel="filter")
            links.append(link)
        return links, items

class StorageChangeList(ChangeList):
    def populate_state(self, state):
        for section in self.sections.itervalues():
            section.populate_state(state)
        index = self.get_instances(state)
        paginator = self.get_paginator(index, storage=self.resource.storage)
        state['paginator'] = paginator
        state['links'] = paginator.links
        

