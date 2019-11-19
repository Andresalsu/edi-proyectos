import psycopg2, hashlib, os

PSQL_HOST = "192.168.96.38"
PSQL_PORT = "5432"
PSQL_USER = "loken"
PSQL_PASS = "s3cur1ty"
PSQL_DB   = "prescriptiva"

try:
    
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

   
    cur = conn.cursor()

    
    sqlquery = "INSERT INTO usuario(nombre, correo, password, id)VALUES ('Elver Galarga', 'd@b.com', 'jijiji', default);"
    cur.execute(sqlquery)
    conn.commit()

    sqlquery = "select * from usuario where nombre="+"'"+"Pedro"+"';"
    cur.execute(sqlquery)
    row = cur.fetchone()

    
    cur.close()
    conn.close()

    
    username = row[0]

    salt = os.urandom(32)
    key=hashlib.pbkdf2_hmac('sha256',str(username),salt,100000)
    storage=salt+key
    salt_from_storage=storage[:32]
    key_from_storage=storage[:32]
    print(username)
    print(key)

except Exception as e:
    print(e)
    print("Error de base de datos")