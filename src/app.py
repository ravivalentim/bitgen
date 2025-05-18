import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='TEX7E!ptUptgEN',
    database='bitvault'
)

cursor = conn.cursor()

print('BitGen your password manager v0.1')

def app_menu():
    print('\t[1] - Create an account')
    print('\t[2] - Save a password')
    print('\t[3] - View passwords')
    print('\t[4] - Exit from app')

def save_on_db(userid, password):
    cursor.execute('INSERT INTO users (userid, hash_password) VALUES (%s, %s)', (userid.lower(), password, ))
    conn.commit()

def create_accout():
    print('\n>>> Welcome to BitGen! You password manager. Let\'go create an account. <<<\n')
    print('\tEnter your userid..: ', end='')
    userid = str(input())
    print('\tEnter your password: ', end='')
    password = str(input())

    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    save_on_db(userid, hash_password)
    print('\n\t\aAccount created!')

def check_vault_password(userid, password):
    cursor.execute('SELECT hash_password FROM users WHERE userid=%s', (userid, ))
    result = cursor.fetchone()

    if (result == None):
        return False
    
    hash_password = result[0].encode('utf-8')

    return bcrypt.checkpw(password.encode('utf-8'), hash_password)
def save_password_db():

    userid = str(input('\tEnter your userid....: '))
    password = str(input('\tEnter your password: '))

    print()

    if check_vault_password(userid, password):
        login = str(input('\tEnter the login......: '))
        password = str(input('\tEnter the password: '))

        cursor.execute('INSERT INTO vault (userid, login, passwrd) VALUES (%s, %s, %s)', (userid, login, password))
        conn.commit()
    else:
        print('\aInvalid username or password. Try again')
    
def view_password():

    userid = str(input('\tEnter your userid....: '))
    password = str(input('\tEnter your password: '))

    if check_vault_password(userid, password):
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
                print(f'\tPassword: {password}\n')
            print('-----------------------\n')
    else:
        print('\aInvalid username or password. Try again')

while (True):
    app_menu()
    action = str(input('Enter your option: '))

    if action == '1':
        create_accout()
    elif action == '2':
        save_password_db()
    elif action == '3':
        view_password()
    elif action == '4':
        print("\aBye (:")
        exit()
    else:
        print("\aEnter a valid option")
