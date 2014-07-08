from psycopg2.extensions import AsIs
from django.db import models
from django.db import connections, transaction
from time import mktime, gmtime

# polls are disabled, but let this function stay for now
def new_topic(poll):
	subject = "Poll: %s" % poll.title
	descr = poll.description
	game = poll.game

	now = int(mktime(gmtime()))
	cursor = connections['fluxbb'].cursor()

	#cursor.execute("SELECT id FROM users WHERE username = '%s'", ['longturn'])
	cursor.execute("SELECT id FROM users WHERE username = 'longturn'")
	poster_id = cursor.fetchone()[0]

	cursor.execute("SELECT id FROM forums WHERE forum_name = '%s'", [AsIs(game)])
	forum_id = cursor.fetchone()[0]

	cmd = "INSERT INTO topics (poster, subject, forum_id, last_poster, posted, last_post) VALUES ('%s', '%s', %d, '%s', %d, %d)"
	cursor.execute(cmd, ['longturn', AsIs(subject), forum_id, 'longturn', now, now])
	transaction.commit_unless_managed(using='fluxbb')

	cursor.execute("SELECT max(id) FROM topics WHERE poster = '%s' AND subject = '%s'", ['longturn', AsIs(subject)])
	topic_id = cursor.fetchone()[0]

	cmd = "INSERT INTO posts (poster, poster_id, topic_id, posted, message) VALUES ('%s', %d, %d, %d, '%s')"
	cursor.execute(cmd, ['longturn', poster_id, topic_id, now, AsIs(descr)])
	transaction.commit_unless_managed(using='fluxbb')

	cmd = "UPDATE forums SET num_topics = num_topics + 1, num_posts = num_posts + 1, last_post = %d, last_poster = '%s' WHERE forum_name = '%s'"
	cursor.execute(cmd, [now, 'longturn', AsIs(game)])
	transaction.commit_unless_managed(using='fluxbb')

	return topic_id

def topic_subject(id):
	cursor = connections['fluxbb'].cursor()

	try:
		cursor.execute("SELECT subject FROM topics WHERE id = %d", [id])
		subject = cursor.fetchone()[0]
	except:
		subject = None
	return subject

### topic:
# id            | integer                | not null default nextval('topics_id_seq'::regclass)
# poster        | character varying(200) | not null default ''::character varying
# subject       | character varying(255) | not null default ''::character varying
# posted        | integer                | not null default 0
# first_post_id | integer                | not null default 0
# last_post     | integer                | not null default 0
# last_post_id  | integer                | not null default 0
# last_poster   | character varying(200) | 
# num_views     | integer                | not null default 0
# num_replies   | integer                | not null default 0
# closed        | smallint               | not null default 0
# sticky        | smallint               | not null default 0
# moved_to      | integer                | 
# forum_id      | integer                | not null default 0

### posts:
# id           | integer                | not null default nextval('posts_id_seq'::regclass)
# poster       | character varying(200) | not null default ''::character varying
# poster_id    | integer                | not null default 1
# poster_ip    | character varying(39)  | 
# poster_email | character varying(80)  | 
# message      | text                   | 
# hide_smilies | smallint               | not null default 0
# posted       | integer                | not null default 0
# edited       | integer                | 
# edited_by    | character varying(200) | 
# topic_id     | integer                | not null default 0

