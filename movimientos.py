import datetime

def guardar_backup(nombre_archivo, lista_datos):
    """
    Recibe la lista completa de transacciones (diccionarios) y la guarda en un TXT.
    Sobrescribe el archivo anterior para evitar duplicados o datos viejos.
    """
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            #Cabecera (Simulando la cabecera de una tabla)
            archivo.write("ID,FECHA,TIPO,CATEGORIA,MONTO,DESCRIPCION\n")
            
            for d in lista_datos:
                # Convertir el diccionario de la DB a una línea de texto CSV
                # d['fecha'] viene como objeto date, se convierte a string
                linea = f"{d['id']},{d['fecha']},{d['tipo']},{d['categoria']},{d['monto']},{d['descripcion']}\n"
                archivo.write(linea)
                
        print(f"--> Backup actualizado correctamente en {nombre_archivo}")
        return True
    except Exception as e:
        print(f"Error al escribir archivo: {e}")
        return False

# Se adapta la función 'leer' para recuperar los datos del TXT si fuera necesario
def leer_backup(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            listado = archivo.readlines()
            # Quitar la cabecera
            datos_limpios = []
            if len(listado) > 1:
                for linea in listado[1:]: # Se empieza desde la línea 1, para ignonar la 0 (que sería la cabecera)
                    datos_limpios.append(linea.strip())
            return datos_limpios
    except FileNotFoundError:
        return []