# pip install mysql-connector-python
import mysql.connector

mydb = mysql.connector.connect(
    # Configura la conexión
    host="localhost",
    user="root",
    passwd=""
)


def initDB():
    cursor = mydb.cursor()
    cursor.execute('CREATE SCHEMA IF NOT EXISTS python')
    cursor.execute('USE python')
    # Crea las tablas correspondientes al diagrama notas.png

    """
        Notas:
        -   id: int
        -   titulo varchar 250
        -   creada timestamp
        -   cuerpo texto
        -   autor varchar 50
    """
    tabla_notas = """
    create table if not exists python.notas (
        id      int             auto_increment primary key,
        titulo  varchar(250)    NOT NULL,
        creada  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
        cuerpo  text,
        autor   varchar(50)     NOT NULL
    );
    """
    cursor.execute(tabla_notas)



def muestraMenu():
    print('------- MENU -------')
    print('  1. Crear usuario')
    print('  2. Login')
    print('  3. Salir')
    print('--------------------')

def muestraOperaciones(usuario):
    print(f'------- OPERACIONES ({usuario}) -------')
    print('  1. Crear nota')
    print('  2. Listar mis notas')
    print('  3. Filtrar notas por fechas')
    print('  4. Borrar nota')
    print('  5. Logout')
    print('--------------------')


def crearUsuario():

    cursor = mydb.cursor()

    print('------ Registro de usuario ------\n')
    username =  input('Nombre de usuario : ')
    password =  input('Contraseña (¡visible!) : ')

    # Añadir el usuario a la BD
    crear_usuario = f"""
        create user '{username}' identified by '{password}';
        grant select, insert, update, delete on python.notas to '{username}';
    """

    cursor.execute(crear_usuario)

    print('------ Usuario añadido ------\n')

def login():
    username = input("Login: ")
    password = input("Password (¡visible!): ")

    # Comprobar que las credenciales son válidas
    credencialesValidas = mysql.connector.connect(
        # Configura la conexión
        host="localhost",
        user=username,
        passwd=password
    )

    # Si las credenciales son válidas, accedemos al meno principal
    if credencialesValidas:
        cursor = credencialesValidas.cursor()
        opcion = 0
        while opcion != 5:
            muestraOperaciones(username)
            opcion = int(input("Elige una opción : "))
            if opcion == 1:
                crearNota(username)
            elif opcion == 2:
                listarNotas(username)
            elif opcion == 3:
                filtrarNotas(username)
            elif opcion == 4:
                borrarNota(username)

def crearNota(username):

    cursor = mydb.cursor()
    
    titulo = input("Titulo: ")
    texto = input("Cuerpo: ")

    # Guardar nota en la BD

    comando_crear_nota = f"""
        insert into python.notas (autor, titulo, cuerpo)
        values ('{username}', '{titulo}', '{texto}')

    """
    cursor.execute(comando_crear_nota)
    mydb.commit()

def listarNotas(username):
    cursor = mydb.cursor()
    
    # Mostrar por pantalla las notas del usuario, ordenadas por fecha de creación decreciente
    comando_listar_notas = f"""
        select *
        from python.notas
        where python.notas.autor = '{username}'
        order by creada desc;
    """
    cursor.execute(comando_listar_notas)
    resultados = cursor.fetchall()
    if resultados:
        for row in resultados:
            print(row)
    return resultados

def filtrarNotas(username):
    cursor = mydb.cursor()
    
    # Mostrar por pantalla las notas del usuario creadas entre dos fechas pedidas por pantalla
    fecha_inicio = input('Fecha de inicio (YYYY-MM-DD): ')
    fecha_fin = input('Fecha de fin (YYYY-MM-DD): ')
    query = f"""
        SELECT * FROM notas 
        WHERE autor = %s AND creada BETWEEN %s AND %s
    """
    cursor.execute(query, (username, fecha_inicio, fecha_fin))

    # Obtener los resultados de la consulta
    resultados = cursor.fetchall()
    if resultados:
        for row in resultados:
            print(row)    
    return resultados


def borrarNota(username):
    cursor = mydb.cursor()
    
    # Pide el id de la nota que se quiere borrar y se elimina la fila correspondiente, siempre que la nota sea del usuario <username>
    
    print('Borrar Nota\n')
    nota_id = input('ID de la nota a borrar: ')

    # Verificar que la nota pertenece al usuario
    verificar_query = (
        "SELECT * FROM notas "
        "WHERE id = %s AND autor = %s"
    )
    cursor.execute(verificar_query, (nota_id, username))
    nota = cursor.fetchone()

    if nota:
        # Si la nota existe y pertenece al usuario, eliminarla
        borrar_query = "DELETE FROM notas WHERE id = %s AND autor = %s"
        cursor.execute(borrar_query, (nota_id, username))
        mydb.commit()
        print('Nota borrada exitosamente.')
    else:
        print('No se encontró una nota con ese ID para el usuario especificado.')
        


def run():
    n = 0
    while n != 3:
        muestraMenu()
        n = int(input("Elige una opción : "))
        if n == 1:
            crearUsuario()
        elif n == 2:
            login()
        elif n == 3:
            print('----- ¡Hasta pronto! -----')


if __name__ == '__main__':
    initDB()
    run()
