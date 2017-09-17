import pytumblr
from option_selector import option_selector
import os

class post_manager:
    def __init__(self, blog_name, auth_file):
        self.blog_name = blog_name
        self.sig_tags = ['People']
        self.opt_slct = option_selector()

        f = open(auth_file)
        auth_info = {line.split(':')[0]:line.split(':')[1] for line in filter(None, f.read().split('\n'))}
        f.close()

        self.client = pytumblr.TumblrRestClient(
                auth_info['consumer_key'],
                auth_info['secret_key'],
                auth_info['token'],
                auth_info['token_secret'])
        
    def post(self, image, state='draft'):
        #Set post data as the path to the image.
        data = image.get_realpath()

        #Determine list of tags.
        tags = image.get_tags()
        people_tags = [t for t in tags if t.get_parent().get_tagname() in self.sig_tags]
        strg_tags = [t.get_tagname().replace('_',' ') for t in people_tags]
        
        #Generate post content.
        line = lambda s: '<p>'+s+'</p>\n\n'
        bold = lambda s: '<b>'+s+'</b>'
        link = lambda s,l: '<a href="'+l+'">'+s+'</a>'
        caption = line(', '.join([bold(t.get_tagname().replace('_', ' ')) for t in people_tags]))+ '<hr> \n\n'
        sources, external_info = self.get_external_info(people_tags)
        source_info = self.get_source_info(image.get_realtag(), external_info.keys())
        for source in sources:
            if not source in external_info.keys():
                continue
            if source_info[source].lower() == 'none':
                caption += line(bold(source.replace('_',' ')+':'))
                scene_str = ''
            else:
                caption += line(bold(link(source.replace('_',' ')+':', source_info[source])))
                strg_tags.append(source.replace('_',' '))
                scene_link = raw_input('Is there an associated '+source+' scene?(\'None\' if not).')
                if scene_link.lower() != 'none':
                    scene_str = line('&emsp;'+link(scene_link, scene_link))
                else:
                    scene_str = ''
            for lnk in external_info[source]:
                if lnk != 'None':
                    caption += line('&emsp;'+link(lnk, lnk)) # &emsp; is a tab
            caption += scene_str

        strg_tags.extend([t.get_tagname().replace('_',' ') for t in tags if not t in people_tags])

        self.client.create_photo(self.blog_name, state=state, data=data, tags=strg_tags, caption=caption)

    def get_external_info(self, tags):
        tag_info = {}
        info_sources = set([])
        for t in tags:
            ext_info_path = t.get_dir()+'/.external_info'
            if not os.path.exists(ext_info_path):
                f = open(ext_info_path, 'w')
                f.close()
            
            f = open(ext_info_path)
            ext_info = {line.split(' ')[0]:line.split(' ')[1] for line in filter(None, f.read().split('\n'))}
            f.close()

            tag_info[t] = ext_info
            info_sources = info_sources | set(ext_info.keys())
        info_sources = list(info_sources)
        print info_sources, len(info_sources)
        
        use_sources = self.opt_slct.get_selection(info_sources, message="Which external sources would you like to include?", allow_writein=True)
        use_sources = [s.replace(' ','_') for s in use_sources]

        external_info = {}
        for source in use_sources:
            external_info[source] = []
            for t in tags:
                try:
                    external_info[source].append(tag_info[t][source])
                except KeyError:
                    #Tag has no info from this source.
                    info = raw_input('No '+source+' link for '+t.get_tagname()+'. What link should be used? (\'None\' for no link)')
                    f = open(t.get_dir()+'/.external_info', 'a')
                    f.write(source+' '+info+'\n')
                    f.close()
                    external_info[source].append(info)
            if len([info for info in external_info[source] if info!='None']) == 0:
                del external_info[source]

        return use_sources, external_info

    def get_source_info(self, tag, sources):
        src_info_path = tag.get_root().get_dir()+'/.source_info.txt'
        if not os.path.exists(src_info_path):
            f = open(src_info_path, 'w')
            f.close()
        
        f = open(src_info_path)
        src_info = {line.split(' ')[0]:line.split(' ')[1] for line in filter(None, f.read().split('\n'))}
        f.close()

        source_info = {}
        for source in sources:
            try:
                source_info[source] = src_info[source]
            except KeyError:
                info = raw_input('No link for '+source+'. What link should be used? (\'None\' for no link)')
                f = open(src_info_path, 'a')
                f.write(source+' '+info+'\n')
                f.close()
                source_info[source] = info
        return source_info
