# Python command line app.

Command line app developed in python 3 that receives a .cvs fiel as parameter and inserts the records in a SQLite db.

The script creates a table with the same name as the file passed by command line (without the csv flag). If its passed the same file name with the same columns the program will insert every record on the same table. When the program detects that the same file name has diferent number of columns the program creates a new table for the new csv file.

The script also checks for special characters in the records and removes them.

To run the app:
'''
python ./main.py file.csv
'''

To test the app run:
'''
python ./test.py -v
'''
## Remember:

You need python 3 for the script to run properly