#Wikipedia assistant

the app can be seen at [http://ec2-54-171-162-193.eu-west-1.compute.amazonaws.com:8080/]

it is hosted on AWS, the main page has two links which lead to:
1) Find the most outdated page:
    For a given category, find the the most outdated page (a possible category can be found by querying the categorylinks
    table, an example would be _Canadian_pop_singers_), once the query is issued, the result, if any, is returned along
    with the processing time in nanoseconds.
2) Run a SQL query:
    A generic SQL query can be input, currently there is no validation, please put limits in the query and try to avoid 
    modifying the data;
    
As Wiki dump used [https://dumps.wikimedia.org/simplewiki/20180820/](_simplewiki_), initially made the mistaken decision
of using Postgres as the RDBMS, as had an instance with it installed already, however it proved to be difficult to change 
the dumps from mysql to postgres format, plus encoding issues, etc. So settled with MySQL eventually, these are the 
tables used:

_describe wikipage_;
```
+----------------+--------------+------+-----+-------------------+-----------------------------+
| Field          | Type         | Null | Key | Default           | Extra                       |
+----------------+--------------+------+-----+-------------------+-----------------------------+
| page_id        | int(11)      | NO   | PRI | NULL              |                             |
| page_title     | varchar(255) | NO   | MUL | NULL              |                             |
| page_namespace | int(11)      | NO   |     | NULL              |                             |
| rev_timestamp  | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+----------------+--------------+------+-----+-------------------+-----------------------------+
```
    
_describe categorylinks_;
```
+---------+-----------------+------+-----+---------+-------+
| Field   | Type            | Null | Key | Default | Extra |
+---------+-----------------+------+-----+---------+-------+
| cl_from | int(8) unsigned | NO   | PRI | 0       |       |
| cl_to   | varbinary(255)  | NO   | PRI |         |       |
+---------+-----------------+------+-----+---------+-------+
```

_describe pagelinks_;
```
+-------------------+-----------------+------+-----+---------+-------+
| Field             | Type            | Null | Key | Default | Extra |
+-------------------+-----------------+------+-----+---------+-------+
| pl_from           | int(8) unsigned | NO   | PRI | 0       |       |
| pl_namespace      | int(11)         | NO   | PRI | 0       |       |
| pl_title          | varbinary(255)  | NO   | PRI |         |       |
| pl_from_namespace | int(11)         | NO   | MUL | 0       |       |
+-------------------+-----------------+------+-----+---------+-------+
```

Imported the data from the dumps, used an existing script to convert the page.xml to a sql file 
([https://github.com/wikimedia/mediawiki-tools-mwdumper](mwdumper.jar), unfortunately due to time constraints could 
not include iii. The position of this link in the ordered list of all the links on the referring page, as for this would
have had to implement my own page content parser, therefore storing the page referred links in alphabetical order 
instead. 

To reduce the loading time of the data, used the following python script to remove the `text` inserts (page content),
from the sql dump:

```python
#!/usr/bin/env python3.6

with open("/Users/rafael.castro/dev/projects/interviews/mwdumper/simple.sql", 'w') as outfile:
    with open("/Users/rafael.castro/dev/projects/interviews/mwdumper/simplepages.sql") as infile:
        for line in infile:
            if not (line.startswith("INSERT INTO text ")):
                outfile.write(line)
```

Then proceeded to import the pages, links and category sql dumps into MySQL.

I had developed already a Scala http4s web app (needs adding more thorough tests, and others), which reads from a local
mysql db (configurable), which was testing with a tiny db, once the big dump files were imported, it was clear I needed 
some indices added to the tables involved in the most outdated query, as the app would freeze:

```sql
select page_title from ( select p.page_id, p.page_title, p.rev_timestamp from wikipage p join categorylinks cl 
on p.page_id=cl.cl_from where cl.cl_to = '"Weird_Al"_Yankovic_songs' ) as categorized inner join 
(select p.page_id, max(ap.rev_timestamp - p.rev_timestamp) as max_modified from wikipage p join 
pagelinks l on p.page_id=l.pl_from join wikipage ap on l.pl_title=ap.page_title group by p.page_id) as modified 
on categorized.page_id = modified.page_id order by max_modified desc limit 1;
```

Tried to create indices on the relevant table/columns (e.g. with CREATE INDEX pagelinks_pl_title ON pagelinks(pl_title);),
but creating the indices was taking quite long, then increased the innodb buffer size, and adding the indices worked 
as a charm, reducing the query time to roughly 10secs. There are no foreign keys set, as the app assumes just those 
queries to be issued, without any cascading or similar.

Thanks.
