from collection import collection
from table import table
import os

class menu(collection):
    def __init__(self, collection_string):
        collection.__init__(self, collection_string)
        self.tasknames = ['View Images', 'Tag Images', 'Quit']
        self.tasks = {'View Images':self.view,
                      'Tag Images':self.tag,
                      'Quit':self.quit}
        self.selector = option_selector()
    def main(self):
        task = self.selector.get_selection(self.tasknames)[0]
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
        get_response = lambda options, show_also=[], s=self.selector: s.get_selection(options, show_also=show_also, allow_writein=True)
        self.tagger.dispatch(get_response)
        return True
    def quit(self):
        print 'QUITTING'
        return False

class option_selector(object):
    def __init__(self):
        pass
    def get_selection(self, options, show_also=[], allow_writein=False):
        #for i, option in enumerate(options):
        #    print ('('+str(i)+')').ljust(5)+option
        self.display_options(options, show_also=show_also)
        selections = raw_input('Please make a selection:')
        final_selections = []
        for selection in [s.strip(' ').rstrip(' ') for s in filter(None,selections.split(','))]:
            try:
                snum = int(selection)
                if snum >= 0 and snum < len(options):
                    final_selections.append(options[snum])
                else:
                    return self.get_selection(options, allow_writein)
            except ValueError:
                if selection in options or allow_writein:
                    final_selections.append(selection)
                else:
                    return self.get_selection(options, allow_writein)
        return final_selections
    def display_options(self, options, show_also=[], sa_chars = ['*','#','%','^']):
        sa_chars = list(sa_chars)
        if len(show_also) > 0:
            tmp = []
            prev = []
            for i in range(len(show_also)):
                try:
                    iter(show_also[i])
                    if len(prev) > 0:
                        tmp.append(prev)
                        prev = []
                    tmp.append(show_also[i])
                except TypeError:
                    prev.append(show_also[i])
            if len(prev) > 0:
                tmp.append(prev)
            show_also = tmp

        def num_entries():
            return len(options) + sum([len(sa) for sa in show_also])

        rows, columns = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        columns = int(columns)

        n_columns = int(len(options) / (rows-1))+1
        fits = False
        while not fits and n_columns > 0:
            n_rows = int(len(options) / n_columns)
            arr = [[] for n in range(n_rows)]
            sa_num = 0
            for i,sa in enumerate(show_also):
                for entry in sa:
                    arr[sa_num%len(arr)].append('('+sa_chars[i%len(sa_chars)]+') '+entry)
                    sa_num += 1
            for i,opt in enumerate(options):
                arr[(i+sa_num)%len(arr)].append('('+str(i)+') '+opt)
            if len(arr) == 0:
                return  #Nothing to print
            tbl = table(init_keywords=[""]*len(arr[0]))
            for row in arr:
                tbl.insert_row(row)
            fits = max([len(line) for line in filter(None, tbl.str_entries().split('\n'))]) <= columns
            n_columns -= 1
        print tbl.str_entries()


