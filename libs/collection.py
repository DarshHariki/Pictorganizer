from tag import tag
from image import image, image_file, image_viewer
from image_tagger import image_tagger
import glob
import os

class collection(object):
    def __init__(self, direc):
        self.base_direc = direc
        self.base_tag = tag(tagname=filter(None, direc.split('/'))[-1])

        self.file_exts = ["*.jpg", "*.png"]

        def build_tags(t):
            direc = t.get_dir()
            subdirecs = [name for name in os.listdir(direc) if os.path.isdir(direc+'/'+name)]
            for subdirec in subdirecs:
                child = tag(tagname=filter(None, subdirec.split('/'))[-1], parent=t)
                t.add_child(child)
                build_tags(child)
        build_tags(self.base_tag)
        disp_size = (9,6.5)
        self.viewer = image_viewer(figsize=disp_size)
        self.tagger = image_tagger(self.base_tag,figsize=disp_size)
    def get_dir(self):
        return self.base_direc

    def retrieve_tag(self, tagname):
        return self.base_tag.search(tagname)

    def get_tagged_images(self, image_list):
        image_list = list(image_list)

        i=0
        while i < len(image_list):
            if isinstance(image_list[i], str):
                image_list[i] = image(image_list[i])
            elif isinstance(image_list[i], image_file):
                image_list[i] = image_list[i].to_image()
            elif isinstance(image_list[i], image):
                pass
            elif not isinstance(image_list[i], image):
                del image_list[i]
                i -= 1
            i += 1

        image_tags = {im.get_realpath():[] for im in image_list} 

        def fill_image_tags(t, image_tags=image_tags):
            for path in t.get_filepaths(*self.file_exts, recurse=False):
                try:
                    image_tags[os.path.realpath(path)].append(t)
                except KeyError:
                    pass
            for child in t.get_children():
                image_tags = fill_image_tags(child, image_tags)
            return image_tags

        image_tags = fill_image_tags(self.base_tag)
        for i,im in enumerate(image_list):
            image_list[i].add_tags(image_tags[im.get_realpath()])
        return image_list
    
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
