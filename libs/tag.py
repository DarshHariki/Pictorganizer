import glob
import os

class tag(object):
    def __init__(self, tagname, parent=None):
        self.tagname = tagname
        self.parent = parent
        self.children = []
    def add_child(self, child_tag):
        self.children.append(child_tag)
    def get_parent(self):
        return self.parent
    def get_children(self):
        return self.children
    def get_dir(self):
        if self.parent==None:
            return self.tagname
        else:
            return self.parent.get_dir()+'/'+self.tagname
    def ensure_dir(self):
        if not os.path.exists(self.get_dir()):
            os.makedirs(self.get_dir())
    def get_filepaths(self, *queries, **kwargs):
        if len(queries) == 0:
            queries = ["*.*"]
        recurse=True
        if 'recurse' in kwargs:
            recurse=kwargs['recurse']
        
        filepaths = []
        for query in queries:
            filepaths += [os.path.abspath(p) for p in glob.glob(self.get_dir()+'/'+query)]

        if recurse:
            for child in self.children:
                filepaths += child.get_filepaths(*queries, recurse=True)

        return filepaths
    def search(self, tagname):
        if self.tagname == tagname:
            return self
        for child in self.children:
            s = child.search(tagname)
            if s != None:
                return s
        return None
    def search_up(self, tagname):
        if self.tagname == tagname:
            return self
        elif self.parent == None:
            return None
        else:
            return self.parent.search_up(tagname)
