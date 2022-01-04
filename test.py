from helpers.db import Database

with Database() as db:
	query = "SELECT * from users;"

	db.curr.execute(query)
	data = db.curr.fetchall()

	print(data)
