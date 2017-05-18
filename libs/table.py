import numpy as np

class table(object):
    def __init__(self, filepath=None, init_keywords=[]):
        self.filepath = filepath
        self.keywords = []
        self.entries = []
        self.insert_columns(init_keywords)
    def load(self, filepath=None):
        if filepath == None:
            filepath = self.filepath
        if self.filepath == None:
            self.filepath = filepath
        if filepath == None:
            raise ValueError("Cannot determine load destination from information given.")

        f = open(filepath, 'r')
        lines = [line for line in f.read().split('\n') if len(line)>0]
        f.close()
        header_lines = [line[1:] for line in lines if line[0]=='#']
        column_headers = [ch.rstrip(' ') for ch in header_lines[-1].split(',')]
        self.insert_columns(column_headers)
        entry_lines = [line for line in lines if line[0]!='#']
        for line in entry_lines:
            column_vals = [val.rstrip(' ') for val in line.split(',')]
            self.insert_row(column_vals)

    def save(self, filepath=None):
        if filepath == None:
            filepath = self.filepath
        if self.filepath == None:
            self.filepath = filepath
        if filepath == None:
            raise ValueError("Cannot determine save destination from information given.")

        f = open(filepath, 'w')
        f.write('#'+self.__str__(join_str=','))
        f.close()
    def insert_columns(self, new_keywords):
        for nkw in new_keywords:
            self.insert_column(nkw)
    def insert_column(self, new_keyword, i="end"):
        if i == "end":
            i = len(self.keywords)
        kw = str(new_keyword)
        n = 0
        while new_keyword in self.keywords:
            new_keyword = kw+str(n)
            n+=2
        self.keywords.insert(i, new_keyword)
        for indx in range(len(self.entries)):
            self.entries[indx].insert_value(i, np.nan)
    def insert_row(self, entry_dict=None, **kwargs):
        if isinstance(entry_dict, list):
            entry_dict = {kw:en for kw, en in zip(self.keywords, entry_dict)}
        self.entries.append(table_entry(self.keywords, entry_dict, **kwargs))
    def __str__(self, join_str="  "):
        return self.str_header()+'\n'+self.str_entries()
    def str_header(self, join_str="  "):
        cwidths = self.get_column_widths()
        return join_str.join([kw.ljust(cw) for kw, cw in zip(self.keywords, cwidths)])
    def str_entries(self, join_str="  "):
        cwidths = self.get_column_widths()
        return "\n".join([join_str.join([str(e_val).ljust(cw) for e_val, cw in zip(e.get_values(), cwidths)]) for e in self.entries])

    def get_column_headers(self):
        return self.keywords
    def get_entries(self):
        return self.entries
    def get_column_widths(self):
        return [max([kcw, ecw]) for kcw, ecw in zip(self.get_keyword_cwidths(), self.get_entries_cwidths())]
    def get_keyword_cwidths(self):
        return [len(str(kw)) for kw in self.keywords]
    def get_entries_cwidths(self):
        return [self.get_entries_cwidth(kw) for kw in self.keywords]
    def get_entries_cwidth(self, keyword):
        if len(self.entries) == 0:
            return 0
        indx = self.keywords.index(keyword)
        return max([len(str(entry[indx])) for entry in self.entries])

class table_entry(object):
    def __init__(self, keywords, entry_dict=None, **kwargs):
        if type(entry_dict)==type(None):
            entry_dict = kwargs
        if isinstance(entry_dict, dict):
            self.values = [entry_dict[kw] if kw in entry_dict else np.nan for kw in keywords]
        else:
            try:
                iter(entry_dict)
                self.values = entry_dict
            except TypeError:
                raise TypeError("Table entry must be made from an iterable. Got " + entry_dict)
    def __getitem__(self, i):
        return self.values[i]
    def get_values(self):
        return self.values
    def insert_value(self, i, val):
        self.values.insert(i, val)
