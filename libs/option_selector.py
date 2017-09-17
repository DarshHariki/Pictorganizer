from table import table
import os

class option_selector:
    def __init__(self):
        pass
    def get_selection(self, options, show_also=[], message='Please make a selection: ',allow_writein=False, sort=True):
        if sort:
            options = sorted(options, key=lambda s: s.lower())
            show_also = [sorted(sa, key=lambda s: s.lower()) for sa in show_also]
        self.display_options(options, show_also=show_also)
        selections = raw_input(message)
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

        n_columns = int(num_entries() / (rows-1))+1
        fits = False
        while not fits and n_columns > 0:
            n_rows = int(num_entries() / n_columns)
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
