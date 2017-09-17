import os
import time
import threading
from getch import getch
import matplotlib.pyplot as plt
#plt.ion()
import matplotlib.image as mpimg

class image_file(object):
    def __init__(self, filepath):
        self.filepath = filepath
    def to_image(self):
        return image(self.filepath)
    def dirname(self):
        return '/'.join(self.filepath.split('/')[:-1])
    def filename(self):
        return self.filepath.split('/')[-1]
    def get_filepath(self):
        return self.filepath
    def get_realpath(self):
        return os.path.realpath(self.filepath)
    def real_dirname(self):
        return '/'.join(self.get_realpath().split('/')[:-1])
    def real_filename(self):
        return self.get_realpath().split('/')[-1]
    def get_img(self):
        try:
            return mpimg.imread(self.filepath)
        except IOError:
            raise IOError('File does not exist. '+self.filepath)
    def link(self, dirname, filename=None):
        if filename == None:
            filename = self.filename()
        if dirname[-1] == '/':
            dirname = dirname[:-1]
        
        linkpath = dirname+'/'+filename
        if os.path.exists(linkpath):
            print ('Link already exists at '+linkpath)
        else:
            try:
                os.symlink(os.path.relpath(self.get_realpath(), dirname), linkpath)
            except OSError:
                print ('Link already exists at '+linkpath+'. Weird. Check it.')
    def display(self, ax=None):
        if ax == None:
            fig = plt.figure()
            ax = fig.add_axes([0.0,0.0,1.0,1.0])
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        try:
            ax.imshow(self.get_img())
        except (IOError, ValueError):
            pass

class image(image_file):
    def __init__(self, filepath, init_taglist=[]):
        image_file.__init__(self, filepath)
        self.taglist=list(init_taglist)
    def add_tags(self, new_taglist):
        for t in new_taglist:
            if not t in self.taglist:
                self.taglist.append(t)
    def add_new_tag(self, t):
        for i in range(len(self.taglist)):
            self.taglist[i].add_relevant(t)
            t.add_relevant(self.taglist[i])
        self.taglist.append(t)
        self.link(t.get_dir())
    def get_tags(self):
        return [self.get_realtag()]+self.get_linktags()
    #def full_taglist(self):
    #    return list(set(self.taglist)|{r for t in self.taglist for r in t.get_ascendants()})
    def get_realtag(self):
        try:
            return [t for t in self.taglist if os.path.realpath(self.filepath) in t.get_filepaths(recurse=False)][0]
        except IndexError:
            try:
                os.remove(self.filepath)
            except OSError:
                pass #File already doesn't exist.
            #raise ValueError("Real image does not exist in known tag directories. "+os.path.realpath(self.filepath))
    def get_linktags(self):
        realtag = self.get_realtag()
        return [t for t in self.taglist if t != realtag]
    def get_relevant_tags(self, taglist=None):
        if type(taglist)==type(None):
            valid_tag = lambda r: True
        else:
            valid_tag = lambda r: r in taglist
        relevant_tags = [rtag for rtag in list(set(self.get_realtag().get_ascendants()) | set(self.get_realtag().get_relevant_tags()) | {r for t in self.get_linktags() for r in t.get_relevant_tags(t.get_siblings())}) if valid_tag(rtag)]
        return relevant_tags

class image_viewer(object):
    def __init__(self, init_image_list=[], **kwargs):
        self.image_list = []
        self.add_images(init_image_list)
        self.counter = 0
        self.fig_kwargs = kwargs
        self.create_viewer()
        self.is_shown = False
    def create_viewer(self, **kwargs):
        self.fig_kwargs.update(kwargs)
        self.figure = plt.figure(**self.fig_kwargs)
        self.viewer = self.figure.add_axes([0.0,0.0,1.0,1.0])
        self.viewer.get_xaxis().set_visible(False)
        self.viewer.get_yaxis().set_visible(False)
    def add_images(self, new_image_list):
        i = 0
        while i < len(new_image_list):
            if isinstance(new_image_list[i], str):
                new_image_list[i] = image_file(new_image_list[i])
            elif not isinstance(new_image_list[i], image_file):
                del new_image_list[i]
                i -= 1
            i += 1
        self.image_list += new_image_list
    def get_images(self):
        return self.image_list
    def clear_images(self):
        self.image_list = []
    def get_current_image(self):
        if len(self.image_list) == 0:
            return None
        self.ensure_counter()
        return self.image_list[self.counter]
    def get_counter(self):
        return self.counter
    def jump_counter(self, offset):
        self.counter += offset
        self.update_viewer()
    def ensure_counter(self):
        try:
            self.counter %= len(self.image_list)
        except ZeroDivisionError:
            self.counter = 0
    def next(self):
        self.counter += 1
        self.update_viewer()
    def prev(self):
        self.counter -= 1
        self.update_viewer()
    def update_viewer(self):
        img = self.get_current_image()
        try:
            self.viewer.cla()
            img.display(ax=self.viewer)
            self.figure.canvas.draw_idle()
        except (IOError, AttributeError):
            pass
    def show(self):
        self.figure.show()
        self.update_viewer()
        self.is_shown = True
    def hide(self):
        plt.close(self.figure)
        del self.figure
        self.create_viewer()
        self.update_viewer()
        self.is_shown = False
    def cycle(self, timer=3, numcycles=10):
        self.update_viewer()
        self.show()
        for n in range(10*len(self.image_list)):
            pause_fig(self.figure, timer)
            #time.sleep(timer)
            self.figure.canvas.draw_idle()

            self.next()


def pause_fig(fig, interval):
    """
    Pause for *interval* seconds.

    If there is an active figure it will be updated and displayed,
    and the GUI event loop will run during the pause.

    If there is no active figure, or if a non-interactive backend
    is in use, this executes time.sleep(interval).

    This can be used for crude animation. For more complex
    animation, see :mod:`matplotlib.animation`.

    This function is experimental; its behavior may be changed
    or extended in a future release.

    """
    backend = plt.rcParams['backend']
    if backend in plt._interactive_bk:
        canvas = fig.canvas
        if canvas.figure.stale:
            canvas.draw()
        fig.show()
        canvas.start_event_loop(interval)
        return

    # No on-screen figure is active, so sleep() is all we need.
    import time
    time.sleep(interval)
