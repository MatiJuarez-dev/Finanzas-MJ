import pymysql

# --- CONECTAR BASE DE DATOS ---
def conectar(ip, usuario, puerto, password, database):
    connection = pymysql.connect(host=ip,
                                user=usuario,
                                password=password,
                                port=puerto,
                                database=database,
                                cursorclass=pymysql.cursors.DictCursor)
    print("Conectado a la DB!\n--------------------------------")
    return connection

# --- FUNCIÓN PARA CREAR LA TABLA ---
def crear_tabla(conexion_db, t_transacciones):
    with conexion_db.cursor() as cursor:
        sql = f""" CREATE TABLE IF NOT EXISTS {t_transacciones} (
            id INT PRIMARY KEY AUTO_INCREMENT,
            monto DECIMAL(10, 2) NOT NULL,
            fecha DATE NOT NULL,
            tipo VARCHAR(10) NOT NULL, -- 'Ingreso' o 'Gasto'
            categoria VARCHAR(50) NOT NULL,
            descripcion VARCHAR(250)
            );"""
        cursor.execute(sql)
        conexion_db.commit()
        print("Tabla creada")

# --- FUNCIÓN PARA AGREGAR UNA TRANSACCIÓN ---
def agregar_transaccion(conexion_db, t_transacciones, monto, fecha, tipo, categoria, descripcion):
    with conexion_db.cursor() as cursor:
        sql = f""" INSERT INTO {t_transacciones} (monto, fecha, tipo, categoria, descripcion)
            VALUES (%s, %s, %s, %s, %s)
            """
        datos = (monto, fecha, tipo, categoria, descripcion) #Para insertar los datos en orden.
        cursor.execute(sql, datos)
        conexion_db.commit()
        print(f"¡Transacción agregada con éxito! (Monto: {monto})")

# --- FUNCIÓN PARA CONSULTAR TRANSACCIONES ---
def consultar_transacciones(conexion_db, t_transacciones):
    with conexion_db.cursor() as cursor:
        sql = f"SELECT * FROM {t_transacciones} ORDER BY fecha DESC"
        cursor.execute(sql)
        resultados = cursor.fetchall()# Trae todos los resultados encontrados.
        print(f"Consulta exitosa: {len(resultados)} transacciones encontradas.")
    return resultados #Devuelve la lista

# --- FUNCIÓN PARA ELIMINAR UNA TRANSACCIÓN ---
def eliminar_transaccion(conexion_db, t_transacciones, id_transaccion):
    with conexion_db.cursor() as cursor:
        sql = f"DELETE FROM {t_transacciones} WHERE id = %s"
        # Los datos (el ID a borrar) en una tupla
        datos = (id_transaccion,)
        cursor.execute(sql, datos)
        conexion_db.commit()
        print(f"Transacción con ID {id_transaccion} eliminada con éxito.")

# --- FUNCIÓN PARA EDITAR UNA TRANSACCIÓN ---
def editar_transaccion(conexion_db, t_transacciones, id_transaccion, monto_nuevo, fecha_nueva, tipo_nuevo, categoria_nueva, descripcion_nueva):
    with conexion_db.cursor() as cursor:
        #Se especifican todas las columnas que se van a cambiar
        sql = f"""
        UPDATE {t_transacciones} 
        SET 
            monto = %s,
            fecha = %s,
            tipo = %s,
            categoria = %s,
            descripcion = %s
        WHERE 
            id = %s 
        """
        # Los datos en orden
        datos = (
            monto_nuevo, 
            fecha_nueva, 
            tipo_nuevo, 
            categoria_nueva, 
            descripcion_nueva, 
            id_transaccion  # El ID va al final para el where
        )
        cursor.execute(sql, datos)
        conexion_db.commit()
        print(f"Transacción con ID {id_transaccion} actualizada con éxito.")