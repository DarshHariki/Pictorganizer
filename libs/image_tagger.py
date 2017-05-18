from image import image, image_viewer
from tag import tag
import os

class image_tagger(image_viewer):
    file_exts = ["*.jpg", "*.png"]
    def __init__(self, base_tag, init_image_list=[]):
        self.base_tag = base_tag
        image_viewer.__init__(self, init_image_list)
    def retrieve_tag(self, tagname):
        return self.base_tag.search(tagname)
    def add_images(self, new_image_list):
        i = 0
        while i < len(new_image_list):
            if isinstance(new_image_list[i], str):
                new_image_list[i] = image(new_image_list[i])
            elif isinstance(new_image_list[i], image_file):
                new_image_list[i] = new_image_list[i].to_image()
            elif not isinstance(new_image_list[i], image):
                del new_image_list[i]
                i -= 1
            i += 1
        self.image_list += new_image_list
        if len(self.image_list) > 0:
            self.get_image_tags()
    def get_image_tags(self):
        image_tags = {im.get_realpath():[] for im in self.image_list} 

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
        for i,im in enumerate(self.image_list):
            self.image_list[i].add_tags(image_tags[im.get_realpath()])
    def dispatch(self, get_response):
        self.show()
        self.start_i = self.counter
        for n in range(len(self.image_list)):
            self._tag_current(get_response)
            self.next()
        self.hide()
    def _tag_current(self, get_response):
        current = self.image_list[self.counter]
        def get_current_tags(img, tnames):
            current_tags = []

            realtag = img.get_realtag()
            if realtag.tagname in tnames:
                current_realtags = [realtag.tagname]
            else:
                current_realtags = []
            
            linktags = img.get_linktags()
            current_linktags = []
            for tname in [t.tagname for t in linktags]:
                if tname in tnames:
                    current_linktags.append(tname)
            return [current_realtags, current_linktags]
            
        def traverse_tags(parent):
            children = parent.get_children()
            tnames = [t.tagname for t in children]
            related_tnames = [t.tagname for t in current.get_related_tags(children)]
            current_tags = get_current_tags(current, tnames)
            available_tags = [tname for tname in tnames if not (tname in current_tags[0] or tname in current_tags[1])]
            picked_tnames = get_response(available_tags, show_also=current_tags)
            recognized_tnames = [tname for tname in picked_tnames if tname in tnames]
            unrecognized_tnames = [tname for tname in picked_tnames if not tname in tnames and tname != 'This']
            for tname in unrecognized_tnames:
                print 'CREATING TAG',tname
                t = tag(tname, parent=parent)
                parent.add_child(t)
                t.ensure_dir()
            for tname in picked_tnames:
                if tname == 'This':
                    current.add_new_tag(parent)
                    continue
                t = self.retrieve_tag(tname)
                if len(t.get_children()) == 0:
                    current.add_new_tag(t)
                else:
                    traverse_tags(t)
        traverse_tags(self.base_tag) 
