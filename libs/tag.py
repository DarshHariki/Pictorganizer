import image_tagger
import glob
import os

class tag(object):
    def __init__(self, tagname, parent=None):
        self.tagname = tagname
        self.parent = parent
        self.children = []
        self.relevant_tags = []
        self.load_relevant()
        self.irrelevant_tags = []
        self.load_irrelevant()
    def get_tagname(self):
        return self.tagname
    def add_child(self, child_tag):
        self.children.append(child_tag)
    def get_parent(self):
        return self.parent
    def get_children(self):
        return self.children
    def get_root(self):
        if self.parent == None:
            return self
        else:
            return self.parent.get_root()
    def get_siblings(self):
        if self.parent == None:
            return []
        return self.parent.get_children()
    def _get_ascendants_helper(self):
        if self.parent == None:
            return [self]
        else:
            return [self]+self.parent._get_ascendants_helper()+self.parent.get_siblings()
    def _get_descendants_helper(self):
        if len(self.children) == 0:
            return [self]
        else:
            return [self]+list({r for c in self.children for r in c._get_descendants_helper()})
    def get_ascendants(self):
        return self._get_ascendants_helper()[1:] #Remove self
    def get_descendants(self):
        return self._get_descendants_helper()[1:] #Remove self

    def get_dir(self):
        if self.parent==None:
            return self.tagname
        else:
            return self.parent.get_dir()+'/'+self.tagname
    def load_relevant(self):
        path = self.get_dir()+'/.relevant_tags'
        if os.path.exists(path):
            f = open(path, 'r')
            self.relevant_tags += [tagname.lstrip().rstrip() for tagname in filter(None, f.read().split(','))]
    def load_irrelevant(self):
        path = self.get_dir()+'/.irrelevant_tags'
        if os.path.exists(path):
            f = open(path, 'r')
            self.irrelevant_tags += [tagname.lstrip().rstrip() for tagname in filter(None, f.read().split(','))]
    def save_relevant(self):
        f = open(self.get_dir()+'/.relevant_tags', 'w')
        f.write(','.join(self.relevant_tags))
        f.close()
    def save_irrelevant(self):
        f = open(self.get_dir()+'/.irrelevant_tags', 'w')
        f.write(','.join(self.irrelevant_tags))
        f.close()
    def add_relevant(self, other):
        if not other.get_tagname() in self.relevant_tags:
            self.relevant_tags.append(other.get_tagname())
            self.save_relevant()
        self.remove_irrelevant(other)
    def add_irrelevant(self, other):
        if not other.get_tagname() in self.irrelevant_tags:
            self.irrelevant_tags.append(other.get_tagname())
            self.save_irrelevant()
        self.remove_relevant(other)
    def remove_relevant(self, other):
        if other.get_tagname() in self.relevant_tags:
            self.relevant_tags.remove(other.get_tagname())
            self.save_relevant()
    def remove_irrelevant(self, other):
        if other.get_tagname() in self.irrelevant_tags:
            self.irrelevant_tags.remove(other.get_tagname())
            self.save_irrelevant()
    def assess_relevance(self, other):
        relevant = not (other in self.get_ascendants() or other in self.get_descendants()) and len(set([os.path.realpath(p) for p in self.get_filepaths()]) & set([os.path.realpath(p) for p in other.get_filepaths()])) > 0
        if relevant:
            self.add_relevant(other)
            other.add_relevant(self)
        else:
            self.add_irrelevant(other)
            other.add_irrelevant(self)
        return relevant
    def is_relevant(self, other):
        if other.get_tagname() in self.relevant_tags:
            return True
        elif other.get_tagname() in self.irrelevant_tags:
            return False
        else:
            return self.assess_relevance(other)
    def get_relevant_tags(self, taglist=None):
        if type(taglist)==type(None):
            valid=lambda t: True
        else:
            valid=lambda t: t in taglist
        return [t for t in self.get_root().get_descendants() if t.tagname in self.relevant_tags if valid(t)]
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
