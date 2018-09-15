#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

from dateutil.parser import parse

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def uprint(text):
    sys.stdout.buffer.write((text+'\n').encode('utf-8'))


wiki_namespaces = ["Talk",
    "User","User_talk","Wikipedia","Wikipedia_talk",
    "File","File_talk","MediaWiki","MediaWiki_talk",
    "Template","Template_talk","Help","Help_talk",
    "Category","Category_talk","Portal","Portal_talk",
    "Book","Book_talk",
    "Education_Program","Education_Program_talk",
    "TimedText","TimedText_talk",
    "Module","Module_talk"]


def escapeSQL(string):
    newstr = string.replace('\\','\\\\')\
            .replace("'", "\\'") \
            .replace('"','\\"') \
            .replace('\u0000','\\0')\
            .replace('\n','\\n')\
            .replace('\r','\\r')\
            .replace('\u001a','\\Z')
    return "'%s'" % newstr


class MWDump:
    def __init__(self, input_file, output_function):
        self.ETip = ET.iterparse(input_file,events=("start","end"))
        first = next(self.ETip)[1]
        self.xmlns = first.tag[:-len('mediawiki')]
        self.stack = []

        self.page = {}
        self.rev = {}
        self.latest_rev = {}
        self.output_function = output_function()

    def run(self):
        for ev, el in self.ETip:
            cleanTag = el.tag[len(self.xmlns):]

            if ev == 'start':
                if cleanTag == 'revision':
                    self.stack.append('revision')
                elif cleanTag == 'page':
                    self.stack.append('page')

            try:
                level = self.stack[-1]
            except:
                level = None

            if level == 'revision':
                if el.text and cleanTag in ['id', 'parentid', 'timestamp', 'text']:
                    self.rev[cleanTag] = el.text

                elif ev == 'end' and cleanTag == 'revision':

                    # prepare data
                    if not 'comment' in self.rev:
                        self.rev['comment'] = ""
                    if not 'text' in self.rev:
                        self.rev['text'] = ""
                    self.rev['page'] = self.page['id']
                    self.rev['timestamp'] = parse(self.rev['timestamp']).strftime("'%y-%m-%d %H:%M:%S'")

                    # latest rev
                    if 'timestamp' not in self.latest_rev or self.latest_rev['timestamp'] < self.rev['timestamp']:
                        self.latest_rev = self.rev

                    self.output_function.run('revision', self.rev)

                    self.rev = {}
                    self.stack.pop()


            elif level == 'page':
                if el.text and cleanTag in ['id','ns','title']:
                    if cleanTag == 'title':
                        try:
                            title = escapeSQL(el.text.replace(" ","_"))
                            splitsies = title.split(":",1)
                            if splitsies[0] in ["'"+x for x in wiki_namespaces]:
                                title = "'"+splitsies[1]
                        except:
                            title = ""
                        self.page['title'] = title

                    else:
                        self.page[cleanTag] = el.text

                elif ev == 'end' and cleanTag == 'page':
                    self.page['latest_rev'] = self.latest_rev['id']
                    self.output_function.run('page', self.page)
                    self.stack.pop()
                    self.page = {}
                    self.latest_rev = {}

            el.clear()
        self.output_function.end()


class MySQL_Output:

    class MyPrint:
        def __init__(self):
            self.limit = 80 * 1024 * 1024
            self.size = 0
            uprint('BEGIN;')

        def do(self, text):
            uprint(text)


    class SQLInsertLineBuffer:
        limit = 800 * 1024
        def __init__(self, print_function, sql_statement):
            self.statement = sql_statement
            self.size = 0
            self.array = []
            self.print_function = print_function

        def add(self, mydata):
            self.size += len(mydata)
            if self.size > self.limit:
                self.doprint()
            self.array += [mydata]

        def doprint(self):
            sql = self.statement % (",".join(self.array))
            self.print_function(sql)

            self.size = 0
            self.array = []

        def finish(self):
            self.doprint()

    def __init__(self):
        myprint = self.MyPrint()
        self.pagelinks = self.SQLInsertLineBuffer(myprint.do,
            "INSERT INTO newpagelinks (ref_page_id, link_title, pos) VALUES %s;")
        self.rev = self.SQLInsertLineBuffer( myprint.do,
            "INSERT INTO revision (rev_id, rev_page, rev_timestamp) VALUES %s;")
        self.page = self.SQLInsertLineBuffer( myprint.do,
            "INSERT INTO page (page_id,page_namespace,page_title,page_latest) VALUES %s;")

    def run(self, mytype, mydata):
        if mytype == 'page':
            page = mydata
            self.page.add("(%s,%s,%s,%s)" %(
                page['id'], page['ns'], page['title'], page['latest_rev'])
                )
        elif mytype == 'revision':
            rev = mydata
            content = escapeSQL(rev['text'])

            links = ','.join(set(["(%s,%s,%s)" % (rev['id'], link, i) for i, link in enumerate(self.find_links_in_text(content))]))
            if len(links) > 1:
                self.pagelinks.add(links)

            self.rev.add("(%s,%s,%s)" % (
                rev['id'], rev['page'], rev['timestamp'])
                )

    @staticmethod
    def valid_internal_link(x):
        split = x.split("|")
        return len(split) == 2 and len(x) < 255 and not split[0].startswith('http://') and not split[0].startswith('https://')

    def find_links_in_text(self, content):
        links = re.findall('\[\[(.+?)\]\]', content)
        if links:
            return [escapeSQL(x.split("|")[0]) for x in links if self.valid_internal_link(x)]
        else:
            return []

    def end(self):
        self.page.finish()
        self.pagelinks.finish()
        self.rev.finish()
        uprint('COMMIT;')


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = sys.stdin.readline()[:-1]


mwd = MWDump(filename, MySQL_Output)
uprint('drop table newpagelinks;')
uprint('drop table page;')
uprint('drop table revision;')
uprint('create table revision (rev_id integer, rev_page integer, rev_timestamp DATETIME, PRIMARY KEY (rev_id, rev_page));')
uprint('create table newpagelinks (ref_page_id integer, link_title character varying(255), pos integer not null);')
uprint('create table page (page_id integer PRIMARY KEY NOT NULL, page_namespace varchar(255), page_title varchar(255), page_latest integer);')
uprint('ALTER DATABASE wikis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
#ALTER TABLE newpagelinks MODIFY COLUMN link_title VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;
uprint('SET NAMES utf8mb4;')
mwd.run()

# trim the categorylinks table from unnecessary columns
# insert INTO wikipage select page_id, page_title, rev_timestamp FROM page p join revision r on p.page_id = r.rev_page where p.page_latest=r.rev_id;
