import billetera_db
import movimientos
import sys 
from tkinter import messagebox
import datetime

class Billetera:
    def __init__(self, host, user, port, password, db_name, table_name):
        self.tabla = table_name
        self.conexion = None
        self.archivo_txt = "Transacciones.txt" # Nombre del archivo donde se guardará los datos de la DB
        
        try:
            self.conexion = billetera_db.conectar(host, user, port, password, db_name)
            billetera_db.crear_tabla(self.conexion, self.tabla)
            
            # Al iniciar se crea espejo en TXT para asegurar que exista
            self._actualizar_txt()
            
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"Error crítico DB: {e}")
            sys.exit(1)

    # --- MÉTODOS PRINCIPALES ---

    def agregar_transaccion(self, monto, fecha, tipo, categoria, descripcion):
        billetera_db.agregar_transaccion(self.conexion, self.tabla, monto, fecha, tipo, categoria, descripcion) # Guardar en MySQL
        self._actualizar_txt() # Actualizar TXT automáticamente

    def consultar_transacciones(self):
        return billetera_db.consultar_transacciones(self.conexion, self.tabla)

    def eliminar_transaccion(self, id_transaccion):
        billetera_db.eliminar_transaccion(self.conexion, self.tabla, id_transaccion)
        self._actualizar_txt()

    def editar_transaccion(self, id_trans, monto, fecha, tipo, cat, desc):
        billetera_db.editar_transaccion(self.conexion, self.tabla, id_trans, monto, fecha, tipo, cat, desc)
        self._actualizar_txt()

    # --- MÉTODO PARA EL BOTÓN DE LA GUI ---
    def generar_reporte_txt(self):
        """
        Este método es llamado por el botón 'Exportar TXT' de la interfaz.
        Fuerza la creación del archivo y devuelve un mensaje de éxito.
        """
        if self._actualizar_txt():
            return True, f"{self.archivo_txt} (Actualizado: {datetime.datetime.now().strftime('%H:%M:%S')})"
        else:
            return False, "Error al escribir el archivo."

    # --- LÓGICA INTERNA DE RESPALDO ---
    def _actualizar_txt(self):
        #Método privado que obtiene los datos de la BD y usa movimientos.py para guardar.
        try:
            # Traer datos frescos de la DB
            datos = self.consultar_transacciones()
            # Usar el archivo Transacciones.py para guardar
            movimientos.guardar_backup(self.archivo_txt, datos)
            return True
        except Exception as e:
            print(f"Error al sincronizar TXT: {e}")
            return False

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()