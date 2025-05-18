import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='TEX7E!ptUptgEN',
    database='bitvault'
)

cursor = conn.cursor()

print('\n\nBitGen your password manager v0.1\n')

def start_menu():
    print('\t[1] - Log in to the vault')
    print('\t[2] - Create an account')

def app_menu():
    print('\t[1] - Save a password')
    print('\t[2] - View your vault')
    print('\t[3] - Exit from app')

def save_on_db(userid, password):
    cursor.execute('INSERT INTO users (userid, hash_password) VALUES (%s, %s)', (userid.lower(), password, ))
    conn.commit()

def create_accout():
    print('\n>>> Welcome to BitGen! You password manager. Let\'go create an account. <<<\n')
    while True:
        try:
            print('\tCreate yout userID................................: ', end='')
            userid = str(input())
            print('\tCreate you password (must be 8 characters or more): ', end='')
            password = str(input())

            while (len(password) < 8):
                print('\tError: your PASSWORD must be 8 characters or more: ', end='')
                password = str(input())
            
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            save_on_db(userid, hash_password)
            print('\n\t\aAccount created!\n')
            break;
        except mysql.connector.errors.IntegrityError:
            print('Error: UserID already registered, please create a new one. (mysql.connector.errors.IntegrityError)')

def login():

    userid = str(input('\tEnter your userID....: '))
    password = str(input('\tEnter your password: '))

    cursor.execute('SELECT hash_password FROM users WHERE userid=%s', (userid, ))
    result = cursor.fetchone()
  
    if (result == None):
        return [False,]
    
    hash_password = result[0].encode('utf-8')

    return [bcrypt.checkpw(password.encode('utf-8'), hash_password), userid]
   

def save_password_db(userid):

    login = str(input('\tEnter the login......: '))
    password = str(input('\tEnter the password: '))
        
    cursor.execute('INSERT INTO vault (userid, login, passwrd) VALUES (%s, %s, %s)', (userid, login, password))
    conn.commit()

def view_password(userid):

    cursor.execute('SELECT login, passwrd FROM vault WHERE userid=%s', (userid, ))
    data = cursor.fetchall()

    if data == []:
        print('\a\nYour vault is empty.\n')
    else:
        print('\n-----------------------')
        for users in data:
            login = users[0]
            password = users[1]

            print(f'\tLogin...: {login}')
            print(f'\tPassword: {password}')
        print('-----------------------\n')

while (True):
    start_menu()
    start_action = str(input('Enter your option: '))

    if start_action == '1':
        login_result = login()   # gets login result [0] -> True or False | [1] UserID
        if login_result[0]:
            while (True):
                userID = login_result[1]
                print(f"\t\nWelcome to your vault, {str(userID).capitalize()}.\n")
                app_menu()
                action = str(input('Enter your option: '))
                if action == '1':
                    save_password_db(userID)
                elif action == '2':
                    view_password(userID)
                elif action == '3':
                    break;
                else:
                    print("\aEnter a valid option")
    if start_action == '2':
        create_accout()
    elif start_action == '4':
        print("\aBye (:")
        exit()
    else:
        print("\aEnter a valid option")
