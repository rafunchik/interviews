#Wikipedia assistant

the app can be seen at [http://ec2-54-171-162-193.eu-west-1.compute.amazonaws.com:8080/]

it is hosted on AWS, the main page has two links which lead to:
1) __Find the most outdated page__:
    For a given category, find the the most outdated page (a possible category can be found by querying the categorylinks
    table, an example would be __Art__), once the query is issued, the result, if any, is returned along
    with the processing time in nanoseconds.
2) __Run a SQL query__:
    A generic SQL query can be input, currently there is just basic validation, please put limits in the query and try to avoid 
    modifying the data.
    
As Wiki dump used [https://dumps.wikimedia.org/simplewiki/20180820/](_simplewiki_), initially made the mistaken decision
of using Postgres as the RDBMS, as had an instance with it installed already, however it proved to be difficult to change 
the dumps from mysql to postgres format, plus encoding issues, etc. So settled with MySQL eventually, these are the 
tables used:

_describe wikipage_;
```
+----------------+--------------+------+-----+-------------------+-----------------------------+
| Field          | Type         | Null | Key | Default           | Extra                       |
+----------------+--------------+------+-----+-------------------+-----------------------------+
| page_id        | integer      | NO   | PRI | NULL              |                             |
| page_title     | varchar(255) | NO   | MUL | NULL              |                             |
| rev_timestamp  | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+----------------+--------------+------+-----+-------------------+-----------------------------+
```
    
_describe categorylinks_;
```
+---------+-----------------+------+-----+---------+-------+
| Field   | Type            | Null | Key | Default | Extra |
+---------+-----------------+------+-----+---------+-------+
| cl_from | integer         | NO   | PRI | 0       |       |
| cl_to   | varchar  (255)  | NO   | PRI |         |       |
+---------+-----------------+------+-----+---------+-------+
```

_describe newpagelinks_;
```
+-------------------+-----------------+------+-----+---------+-------+
| Field             | Type            | Null | Key | Default | Extra |
+-------------------+-----------------+------+-----+---------+-------+
| ref_page_id       | integer         | NO   |     | 0       |       |
| link_title        | varchar(255)    | NO   |     |         |       |
| pos               | integer         | NO   |     | 0       |       |
+-------------------+-----------------+------+-----+---------+-------+
```

Imported the data from the categorylinks SQL dump, then modified an existing script to convert the page.xml to a sql file 
([https://github.com/andreasnuesslein/mwdump.py](mwdump.py), the script is in Python and uses _xml.etree.ElementTree_ to 
parse the XML file line by line, rather than loading it in memory, modified it to just import the data I was interested 
in, especially added methods to parse the revision content (used the page current revision dump) and extract internal links 
in the order they appear (which go into the _pos_ column in the newpagelinks table).

Also had to enable _utf8mb4_ to be able to store utf8 chars which take more than 4 bytes:

``` sql
SET NAMES utf8mb4;
ALTER DATABASE wikis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE newpagelinks MODIFY COLUMN link_title VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;
```

Once the data about pages, new links and category sql had been imported into MySQL, created a new table _wikipage_,
joining the last revision's timestamp to the page:

```sql
INSERT INTO wikipage select page_id, page_title, rev_timestamp FROM page p join revision r on p.page_id = r.rev_page 
where p.page_latest=r.rev_id;
```

I had developed already a Scala http4s web app (needs adding more thorough tests, and others), which reads from a local
mysql db (configurable), which was testing with a tiny db, once the big dump files were imported, it was clear I needed 
some indices added to the tables involved in the _most outdated query_:

```sql
select page_title from ( select p.page_id, p.page_title, p.rev_timestamp from wikipage p join categorylinks cl 
on p.page_id=cl.cl_from where cl.cl_to = 'Art' ) as categorized inner join 
(select p.page_id, max(ap.rev_timestamp - p.rev_timestamp) as max_modified from wikipage p join 
newpagelinks l on p.page_id=l.ref_page_id join wikipage ap on l.link_title=ap.page_title group by p.page_id) as modified 
on categorized.page_id = modified.page_id order by max_modified desc limit 1;
```

Tried to create indices on the relevant table/columns (e.g. with 

``` sql
CREATE INDEX newpagelinks_link_title ON pagelinks(link_title);)
CREATE INDEX categorylinks_cl_from ON categorylinks(cl_from);)
etc...
```

but creating the indices was taking quite long, then increased the innodb buffer size, and adding the indices worked 
like a charm, reducing the query time considerably. There are no foreign keys set, as the app assumes just those 
queries to be issued, without any cascading or similar.

