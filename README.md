A limitation of Trac (version 0.12.6) is that it does not provide
a unique closed-time value for tickets when they are closed.
Trac only provides the created date/time and the last modified date/time,
which makes reporting Ticket Statistics an awkward manual work-around. 

Prior to running these scripts, create the Closed Timestamp custom field
('closed_timestamp' in the 'ticket_custom' table of trac.db)
for providing a field in which the closed time could be populated.
The following SQL query, Python script, and Cron job will update all existing closed tickets with this timestamp,
a text string formatted as "YYYY-MM-DD HH:MM:SS".

Due to the limitations of Trac Custom Fields, information entered will remain a text string,
as Custom Fields don't currently support datetime data types.
(The time custom field type is being implemented in Trac 1.1.1 -
http://trac.edgewall.org/wiki/TracDev/Proposals/TracTicketsCustomTimeFields).

The SQL query will create the rows in the SQLite trac.db under ticket_custom table
for populating the values for the closed_timestamp field.
Any tickets that had been modified since the Closed Timestamp custom field was created
have records in the ticket_custom table, with a null value.
(http://trac.edgewall.org/wiki/0.12/TracTicketsCustomFields#Updatingthedatabase)

The Python script will use the PySQLite package to pull the closed timestamps from ticket_change,
convert them from UNIX epoch time (in microseconds) to local time,
and update the 'value' field in ticket_custom for all closed tickets.

Lastly, a cron job is set up to run hourly during weekdays to update any changes made to ticket resolution status.