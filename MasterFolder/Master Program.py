import subprocess
from pathlib import Path
def main():
    classify()
    

def classify():

    detect_path = 'detect.py'
    
    

    source_arguments = '--source 0'

    weight_arguments = '--weights best.pt'

    


    try:
        subprocess.run(['python', detect_path, weight_arguments, source_arguments], check=True)
    except subprocess.CalledProcessError as e:
         print(f'An error occurred: {e}')


def insertRecord(classification, filepath):
    host = "172.16.2.161:37306"
    user = "capstone"
    password = "capstone23!"
    database ="capstone"
    table = "TRANSACTIONS"

    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database

        )
    except Exception as e:
        print(f"Error: {e}")


    
main()