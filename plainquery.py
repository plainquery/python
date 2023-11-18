# SQL from commandline as param



# SQL from commandline as file
python3 deleter.py "$(cat test.sql)"
python3 writer.py "$(cat test.sql)"
python3 reader.py "$(cat test.sql)"