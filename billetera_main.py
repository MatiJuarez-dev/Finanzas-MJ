# billetera_main.py

from clase_billetera import Billetera
from billetera_gui import BilleteraGUI

# Definiendo los datos de la conexión
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PORT = 3306
DB_PASS = 'root'
DB_NAME = 'finanzas'
DB_TABLE = 't_transacciones'

# Crear el objeto Billetera y conectaro a la DB
try:
    billetera_logica = Billetera(DB_HOST, DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_TABLE)

    # Crea la GUI solo si la conexión fue exitosa
    app = BilleteraGUI(billetera_logica)
    app.mainloop()

except Exception as e:
    print(f"No se pudo iniciar la aplicación. Error: {e}")
    # El error de conexión ya se muestra en un messagebox desde clase_billetera.py