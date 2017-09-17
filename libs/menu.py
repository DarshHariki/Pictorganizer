from collection import collection
from tumblr_post import post_manager
from option_selector import option_selector
import os

class menu(collection):
    def __init__(self, collection_string):
        collection.__init__(self, collection_string)
        self.tasknames = ['View Images', 'Tag Images', 'Post Images', 'Quit']
        self.tasks = {'View Images':self.view,
                      'Tag Images':self.tag,
                      'Post Images':self.post,
                      'Quit':self.quit}
        self.poster = post_manager('gaypornstarsbyname', '../tumblr/.auth.txt')
        self.selector = option_selector()
    def main(self):
        task = self.selector.get_selection(self.tasknames, sort=False)[0]
        keep_going = self.tasks[task]()
        if keep_going:
            self.main()
    def view(self):
        print 'VIEW IMAGES'
        self.fill_viewer(self.selector.get_selection(options=[],allow_writein=True))
        options = ['Next', 'Prev', 'Cycle', 'Exit']
        self.show_viewer()
        selection = ""
        while selection != 'Exit':
            try:
                selection = self.selector.get_selection(options)[0]
            except IndexError:
                continue
            if selection == 'Next':
                self.viewer.next()
            if selection == 'Prev':
                self.viewer.prev()
            if selection == 'Cycle':
                self.viewer.cycle(timer=0.8)
        self.empty_viewer()
        self.hide_viewer()
        return True
    def tag(self):
        print 'TAG IMAGES'
        self.fill_tagger(self.selector.get_selection(options=[],allow_writein=True))
        get_response = lambda options, s=self.selector, **kwargs: s.get_selection(options, allow_writein=True, **kwargs)
        self.tagger.dispatch(get_response)
        self.empty_tagger()
        return True
    def post(self):
        print 'POST IMAGE'
        self.fill_tagger(self.selector.get_selection(options=[],allow_writein=True))
        #images = self.tagger.get_images()
        options = ['Next', 'Prev', 'Jump', 'Post', 'Tag', 'Exit']
        self.show_tagger()
        get_response = lambda options, s=self.selector, **kwargs: s.get_selection(options, allow_writein=True, **kwargs)
        selection = ""
        while selection != 'Exit':
            print 'Current Tags: '+', '.join([t.get_tagname() for t in self.tagger.get_current_image().get_tags()])
            try:
                selection = self.selector.get_selection(options)[0]
            except IndexError:
                continue
            if selection == 'Next':
                self.tagger.next()
            if selection == 'Prev':
                self.tagger.prev()
            if selection == 'Jump':
                try:
                    offset = int(raw_input('Jump by how many? '))
                    self.tagger.jump_counter(offset)
                except TypeError:
                    print 'INVALID INPUT. Jumps must be integer numbers.'
            if selection == 'Post':
                self.poster.post(self.tagger.get_current_image())
            if selection == 'Tag':
                self.tagger.tag_image(self.tagger.get_current_image(), get_response)

        self.empty_tagger()
        self.hide_tagger()
        return True

    def quit(self):
        print 'QUITTING'
        return False

