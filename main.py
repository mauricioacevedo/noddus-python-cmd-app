import functions
import sys
import os
##############################
#  python3 command line app  #
#  author: Mauricio Acevedo  #
##############################
SQLITE_DB_PATH = './sqlite.db'

def main(test_param = False):
    #1. check command line params and get the file name

    if test_param == True:
        filename = "file.csv"
    else:
        filename = functions.param_checking(sys.argv)

    if filename == -1: 
        return
    
    #2. reading csv file and list transform
    csv_list = functions.process_csv(filename)
    if csv_list == -1:
        return
        
    ### clean the filename from path
    filename = os.path.basename(filename)

    #3. get a connection to sqlite db
    connection = functions.get_sqlite_connection(SQLITE_DB_PATH)
    if connection == -1: 
        return

    #4. insert rows to database
    result,total_rows = functions.execute_inserts(csv_list, filename, connection)
    if result != -1:
        print("[SUCCESS] " + str(result) + " records inserted, total records are " + str(total_rows))

### Main function
if __name__ == '__main__':
    main()