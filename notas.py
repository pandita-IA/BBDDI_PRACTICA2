# pip install mysql-connector-python
import mysql.connector

mydb = mysql.connector.connect(
    # Configura la conexión
    host="localhost",
    user="",
    passwd=""
)


def initDB():
    cursor = mydb.cursor()
    cursor.execute('CREATE SCHEMA IF NOT EXISTS python')
    cursor.execute('USE python')
    # Crea las tablas correspondientes al diagrama notas.png


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

    print('------ Usuario añadido ------\n')

def login():
    username = input("Login: ")
    password = input("Password (¡visible!): ")

    # Comprobar que las credenciales son válidas
    credencialesValidas = ...

    # Si las credenciales son válidas, accedemos al meno principal
    if credencialesValidas:
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
    titulo = input("Titulo: ")
    texto = input("Cuerpo: ")

    # Guardar nota en la BD

def listarNotas(username):
    comando_listar_notas = """
            select *
            from python.notas
            where autor = username
            order by creada desc;
        """
    cursor.execute(comando_listar_notas,())
    pass

def filtrarNotas(username):
    username = input('Nombre de usuario: ')
    fecha_inicio = input('Fecha de inicio (YYYY-MM-DD): ')
    fecha_fin = input('Fecha de fin (YYYY-MM-DD): ')
    try:
        query = (
            "SELECT * FROM notas "
            "WHERE usuario = %s AND fecha_creacion BETWEEN %s AND %s"
        )
        cursor.execute(query, (username, fecha_inicio, fecha_fin))

        # Obtener los resultados de la consulta
        resultados = cursor.fetchall()

        if resultados:
            print(' Notas Encontradas\n')
            for row in resultados:
                print(row)
        else:
            print('No se encontraron notas para el usuario en el rango de fechas especificado.')

    pass

def borrarNota(username):
    username = input('Nombre de usuario: ')
    print('Borrar Nota\n')
    nota_id = input('ID de la nota a borrar: ')

    try:
        # Verificar que la nota pertenece al usuario
        verificar_query = (
            "SELECT * FROM notas "
            "WHERE id = %s AND usuario = %s"
        )
        cursor.execute(verificar_query, (nota_id, username))
        nota = cursor.fetchone()

        if nota:
            # Si la nota existe y pertenece al usuario, eliminarla
            borrar_query = "DELETE FROM notas WHERE id = %s AND usuario = %s"
            cursor.execute(borrar_query, (nota_id, username))
            mydb.commit()
            print('Nota borrada exitosamente.')
        else:
            print('No se encontró una nota con ese ID para el usuario especificado.')
    pass

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
