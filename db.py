def Save(db):
	with open("data.py", 'w') as file:
		file.write(f"db = {str(db)}")
