import csv 
import sqlite3
import re

##############################
#  python3 functions         #
#  author: Mauricio Acevedo  #
##############################

### csv file transform into list
def process_csv(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
            return csv_list
    except IOError:
        print('[ERROR]: csv file not found or with errors!!')
        return -1

### insert list rows to sqlite db
### generic fashion, it means that if the file does not have first row with column names
### it will create generic column names
def execute_inserts(cvs_list, file, connection):
    #1. create table with file as name
    file=file.lower().replace('.csv','')
    column_count = len(cvs_list[0])
    column_names = ["'column"+ str(i) + "'" for i in range(column_count)]
    
    conn = connection.cursor()

    conn.execute("pragma table_info("+file+")")
    actual_table_columns_count=len(conn.fetchall())

    if actual_table_columns_count != 0:
        if actual_table_columns_count != (column_count + 1):
            # table already exists, for any reason columns changed.. need to drop the old one
            # column_count + 1: added 1 because there is an auto increment id column
            try:
                conn.execute("DROP TABLE "+file)
            except sqlite3.Error as error:
                print(error)
    
        
    conn.execute("CREATE TABLE IF NOT EXISTS "+file+" (id INTEGER PRIMARY KEY AUTOINCREMENT, %s)" % " , ".join(column_names))
    
    #2. iterate over csv_list and insert rows
    SQLITE_INSERT ="INSERT INTO "+file+"(%s) values " % ",".join(column_names)
    new_records = 0
    for row in cvs_list:
        #quote and clean the elements
        row = [ "'" + clean_string(element) + "'" for element in row]
        SQLITE_INSERT_TMP = SQLITE_INSERT + " (%s) " % ",".join(row)
        try:
            conn.execute(SQLITE_INSERT_TMP)
            new_records += 1
        except sqlite3.Error as error:
            print("[ERROR]: " + str(error))
            return -1,-1
    connection.commit()

    conn.execute("select count(*) from "+ file)
    total_rows = conn.fetchone()[0]
    
    return new_records,total_rows
        


### create a connection for sqlite
def get_sqlite_connection(db_path):

    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as error:
        print("[ERROR]: can't stablish connection to sqlite database: " + str(error))
        return -1
    return conn

### remove string special characters 
def clean_string(s):
    s=s.strip()
    s=re.sub('[^A-Za-z0-9 ]', '', s)
    return s


### check for command line params
### return the file name if there is no error in the parameters otherwise return -1
def param_checking (argv):
    params_length = len(argv)
    
    if params_length <= 1:
        print ('[ERROR]: not enough command line params ' + str(params_length))
        help()
        return -1
    ## file name
    file_param = argv[1]
    
    if file_param in ('--help' or '-h'):
        help()
        return -1

    ##check if its a valid csv file (by extension)
    if not file_param.lower().endswith('.csv'):
        print ('[ERROR]: file must be .csv extension.. passed: [' + file_param + ']')
        help()
        return -1
    
    return file_param

def help():
    print(  "\n############################################"
            "\nSmall Command Line app. "+
            "\n- Reads a csv file from command line and insert records to a sqlite db."+
            "\n- Creates a table with the same file name."+
            "\n- If with the same file name there are more or less columns it creates another table."+
            "\n- The script also check for special characters and remove them from the records."+
            "\nUsage: "+
            "\n run: python ./main.py file.csv"+
            "\n where file.csv is a valid csv file (format and extension) with delimiter ','.\n")
