import os, sqlite3, time

#Set localtime to Eastern for unixepoch conversion
os.environ['TZ'] = 'EST+05EDT,M3.2.0,M11.1.0'
time.tzset()

# Creates cursor interface to the Trac DB
conn = sqlite3.connect('/var/www/trac/db/trac.db')
c = conn.cursor()

# Grabs all unique ticket numbers listed on ticket_change table
c.execute("SELECT DISTINCT ticket FROM ticket_change")
results = c.fetchall()

# Creates empty set for appending ticket/time pair tuples in following FOR statement
timestamps = []

for row in results:
	# Selects most recent 'closed' or 'reopened' update for each ticket from ticket_change
	c.execute("SELECT ticket, max(time), newvalue FROM ticket_change WHERE ticket = (?) AND (newvalue = 'closed' or newvalue = 'reopened')", row)
	status = c.fetchone()

	# IF statement to modify when most recent change is 'closed', not 'reopened'
	if status[2] == 'closed':
		closed_time = status[1]
		time_obj = time.localtime(int(closed_time/1000000))
		time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_obj)

		ticket_number = str(status[0])

		timestamps.append((ticket_number, time_str))

	#ELSE statement to enter cleared value when most recent change is 'reopened'
	else:
		time_str = ''
		ticket_number = str(status[0])
		timestamps.append((ticket_number, time_str))

for ts in timestamps:
	# Updates each closed_timestamp field with datetime-formatted timestamp
	c.execute("UPDATE ticket_custom SET value=:timestamp WHERE (ticket=:number AND name='closed_timestamp')", {'timestamp': ts[1], 'number': ts[0]})

	conn.commit()

conn.close()
