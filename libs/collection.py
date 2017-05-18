from tag import tag
from image import image_viewer
from image_tagger import image_tagger
import glob
import os

class collection(object):
    def __init__(self, direc):
        self.base_direc = direc
        self.base_tag = tag(tagname=filter(None, direc.split('/'))[-1])

        def build_tags(t):
            direc = t.get_dir()
            subdirecs = [name for name in os.listdir(direc) if os.path.isdir(direc+'/'+name)]
            for subdirec in subdirecs:
                child = tag(tagname=filter(None, subdirec.split('/'))[-1], parent=t)
                t.add_child(child)
                build_tags(child)
        build_tags(self.base_tag)
        self.viewer = image_viewer()
        self.tagger = image_tagger(self.base_tag)
    def get_dir(self):
        return self.base_direc

    def retrieve_tag(self, tagname):
        return self.base_tag.search(tagname)
    
    def query_images(self, tagnames, inclusive=False):
        image_paths = set()
        for tagname in tagnames:
            t = self.retrieve_tag(tagname)
            if t == None:
                print 'No tag found for', tagname
                continue
            t_image_paths = [os.path.realpath(path) for path in t.get_filepaths("*.jpg", '*.png')]
            if inclusive or tagname == tagnames[0]:
                image_paths = image_paths | set(t_image_paths)
            else:
                image_paths = image_paths & set(t_image_paths)
        return list(image_paths)

    def show_viewer(self):
        self.viewer.show()
    def hide_viewer(self):
        self.viewer.hide()
    def fill_viewer(self, tagnames, inclusive=False):
        self.viewer.add_images(self.query_images(tagnames, inclusive))
    def empty_viewer(self):
        self.viewer.clear_images()
    def cycle_images(self, tagnames, inclusive=False, timer=1.0):
        self.viewer.clear_images()
        self.fill_viewer(tagnames, inclusive)
        self.viewer.cycle(timer)
    def show_tagger(self):
        self.tagger.show()
    def hide_tagger(self):
        self.tagger.hide()
    def fill_tagger(self, tagnames, inclusive=False):
        self.tagger.add_images(self.query_images(tagnames, inclusive))
    def empty_tagger(self):
        self.tagger.clear_images()
    #def tag_images(self, tagnames, inclusive=False):
    #    self.tagger.clear_images()
    #    self.tagger.add_images(self.query_images(tagnames, inclusive))
