import tkinter as tk
from tkinter import ttk, messagebox, Menu
import customtkinter as ctk  # LIBRERÍA NUEVA
from datetime import date
import requests

# --- CONFIGURACIÓN DE ESTILO ---
ctk.set_appearance_mode("Light")  # Modo Claro
ctk.set_default_color_theme("green")  # Tema principal Verde

class BilleteraGUI(ctk.CTk):
    def __init__(self, billetera_controller):
        super().__init__()
        self.billetera = billetera_controller
        
        # --- CONFIGURACIÓN VENTANA ---
        self.title("Mi Billetera")
        self.geometry("1200x720")
        
        # Layout principal (Grid)
        self.columnconfigure(0, weight=1) # Panel Izquierdo
        self.columnconfigure(1, weight=3) # Panel Derecho
        self.rowconfigure(0, weight=1)

        # --- PANELES PRINCIPALES ---
        # Usamos frames transparentes para organizar
        self.panel_izquierdo = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.panel_derecho = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_derecho.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        # --- CONSTRUCCIÓN DE LA UI ---
        # Esto crea los contenedores vacíos en la pantalla
        self._crear_tarjeta_saldo()
        self._crear_tarjeta_resumen()
        self._crear_tarjeta_dolar()
        self._crear_tabla_moderna()

        # Carga inicial
        self.actualizar_interfaz()

    # ==========================================
    # SECCIÓN IZQUIERDA (DASHBOARD)
    # ==========================================
    
    def _crear_tarjeta_saldo(self):
        # Tarjeta con fondo blanco y bordes redondeados
        card = ctk.CTkFrame(self.panel_izquierdo, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))

        # Contenido
        ctk.CTkLabel(card, text="SALDO TOTAL", font=("Roboto Medium", 12), text_color="gray").pack(pady=(20, 5))
        
        self.lbl_saldo = ctk.CTkLabel(card, text="$ 0.00", font=("Roboto", 36, "bold"), text_color="#10B981")
        self.lbl_saldo.pack(pady=(0, 25))

    def _crear_tarjeta_resumen(self):
        card = ctk.CTkFrame(self.panel_izquierdo, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(card, text="Resúmen", font=("Roboto", 14, "bold"), text_color="#333").pack(anchor="w", padx=20, pady=(15, 10))

        # Grid interno para Ingresos vs Gastos
        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Ingresos
        f_ing = ctk.CTkFrame(grid_frame, fg_color="#ECFDF5", corner_radius=10) # Fondo verde muy claro
        f_ing.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(f_ing, text="Ingresos", font=("Roboto", 10), text_color="#047857").pack(pady=(5,0))
        self.lbl_ingresos = ctk.CTkLabel(f_ing, text="$0", font=("Roboto", 14, "bold"), text_color="#059669")
        self.lbl_ingresos.pack(pady=(0, 5))

        # Gastos
        f_gas = ctk.CTkFrame(grid_frame, fg_color="#FEF2F2", corner_radius=10) # Fondo rojo muy claro
        f_gas.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(f_gas, text="Gastos", font=("Roboto", 10), text_color="#B91C1C").pack(pady=(5,0))
        self.lbl_gastos = ctk.CTkLabel(f_gas, text="$0", font=("Roboto", 14, "bold"), text_color="#DC2626")
        self.lbl_gastos.pack(pady=(0, 5))

        # Botón Grande
        btn = ctk.CTkButton(card, text="+ Nuevo Registro", height=40, corner_radius=10, font=("Roboto Medium", 14),
                            fg_color="#10B981", hover_color="#059669",
                            command=lambda: self.abrir_formulario())
        btn.pack(fill="x", padx=20, pady=(10, 20))

    def _crear_tarjeta_dolar(self):
        card = ctk.CTkFrame(self.panel_izquierdo, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))

        # Cabecera
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(header, text="Dólar Blue", font=("Roboto", 14, "bold"), text_color="#333").pack(side="left")
        
        btn_update = ctk.CTkButton(header, text="↻", width=30, height=30, corner_radius=15, 
                                   fg_color="#F3F4F6", text_color="#333", hover_color="#E5E7EB",
                                   command=self.obtener_cotizacion_dolar)
        btn_update.pack(side="right")

        # Valores
        values_frame = ctk.CTkFrame(card, fg_color="transparent")
        values_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(values_frame, text="COMPRA", font=("Roboto", 10), text_color="gray").grid(row=0, column=0, sticky="w")
        self.lbl_dolar_compra = ctk.CTkLabel(values_frame, text="-", font=("Roboto", 16), text_color="#333")
        self.lbl_dolar_compra.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        ctk.CTkLabel(values_frame, text="VENTA", font=("Roboto", 10), text_color="gray").grid(row=2, column=0, sticky="w")
        self.lbl_dolar_venta = ctk.CTkLabel(values_frame, text="-", font=("Roboto", 16), text_color="#333")
        self.lbl_dolar_venta.grid(row=3, column=0, sticky="w")

    # ==========================================
    # SECCIÓN DERECHA (TABLA)
    # ==========================================
    
    def _crear_tabla_moderna(self):
        card = ctk.CTkFrame(self.panel_derecho, fg_color="white", corner_radius=15)
        card.pack(fill="both", expand=True)

        # Titulo
        ctk.CTkLabel(card, text="Transacciones", font=("Roboto", 18, "bold"), text_color="#333").pack(anchor="w", padx=25, pady=(25, 10))

        # --- CONFIGURACIÓN DE ESTILO PARA EL TREEVIEW ---
        # Daándole estilo al Treeview con ttk.Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",
                        foreground="#333",
                        fieldbackground="white",
                        rowheight=50,
                        font=("Roboto", 11),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background="#F9FAFB", # Gris muy claro para encabezados
                        foreground="#4B5563",
                        font=("Roboto", 10, "bold"),
                        borderwidth=0)
        style.map("Treeview", 
                  background=[('selected', "#F0FDF4")], # Verde muy suave al seleccionar
                  foreground=[('selected', "#000000")])

        # Contenedor para la tabla
        frame_tabla = ctk.CTkFrame(card, fg_color="transparent")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        cols = ("id", "cat", "desc", "monto", "fecha", "menu")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", selectmode="browse")
        
        # Configuración Columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("cat", text="CATEGORÍA")
        self.tree.heading("desc", text="DESCRIPCIÓN")
        self.tree.heading("monto", text="MONTO")
        self.tree.heading("fecha", text="FECHA")
        self.tree.heading("menu", text="")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("cat", width=120, anchor="w")
        self.tree.column("desc", width=300, anchor="w")
        self.tree.column("monto", width=120, anchor="e")
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("menu", width=50, anchor="center")

        # Scrollbar moderna de CustomTkinter
        scrollbar = ctk.CTkScrollbar(frame_tabla, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tags de colores
        self.tree.tag_configure("ingreso", foreground="#10B981") # Verde
        self.tree.tag_configure("gasto", foreground="#EF4444")   # Rojo

        # Eventos
        self.tree.bind("<Button-1>", self.manejar_click_tabla)
        
        # Menú nativo (CustomTkinter no tiene menú contextual nativo aún, usamos el de tk)
        self.menu_contextual = Menu(self, tearoff=0, bg="white", fg="#333", relief="flat", activebackground="#F3F4F6")
        self.menu_contextual.add_command(label=" Editar", command=self.abrir_editar)
        self.menu_contextual.add_command(label=" Eliminar", command=self.eliminar_registro)

    # ================================================
    # LÓGICA DE DATOS (Idéntica a la versión anterior)
    # ================================================
    def actualizar_interfaz(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        data = self.billetera.consultar_transacciones()
        tot_ing, tot_gas = 0, 0

        for t in data:
            tag = "ingreso" if t['tipo'] == "Ingreso" else "gasto"
            val_monto = float(t['monto'])
            if t['tipo'] == "Ingreso": tot_ing += val_monto
            else: tot_gas += val_monto
            
            # Formato moneda y símbolo de menú
            self.tree.insert("", "end", values=(t['id'], t['categoria'], t['descripcion'], f"$ {val_monto:,.2f}", t['fecha'], "⋮"), tags=(tag,))

        saldo = tot_ing - tot_gas
        self.lbl_saldo.configure(text=f"$ {saldo:,.2f}")
        self.lbl_ingresos.configure(text=f"$ {tot_ing:,.2f}")
        self.lbl_gastos.configure(text=f"$ {tot_gas:,.2f}")

        if self.lbl_dolar_compra.cget("text") == "-":
            self.obtener_cotizacion_dolar()

    def obtener_cotizacion_dolar(self):
        try:
            r = requests.get("https://dolarapi.com/v1/dolares/blue", timeout=3)
            if r.status_code == 200:
                d = r.json()
                self.lbl_dolar_compra.configure(text=f"$ {d['compra']}")
                self.lbl_dolar_venta.configure(text=f"$ {d['venta']}")
        except:
            pass

    def manejar_click_tabla(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            if col == "#6": 
                row = self.tree.identify_row(event.y)
                self.tree.selection_set(row)
                self.menu_contextual.tk_popup(event.x_root, event.y_root)

    # ===============================================
    # VENTANA EMERGENTE (MODAL) - CustomTkinter Style
    # ===============================================
    def abrir_formulario(self, modo="nuevo", datos_editar=None):
        # CTkToplevel para una ventana moderna
        top = ctk.CTkToplevel(self)
        top.title("Registro")
        top.geometry("400x550")
        top.resizable(False, False)
        top.attributes("-topmost", True) # Mantener al frente
        
        # Centrar ventana (aproximado)
        top.geometry(f"+{self.winfo_x() + 400}+{self.winfo_y() + 100}")

        # Contenedor principal
        f = ctk.CTkFrame(top, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=30, pady=30)

        titulo = "Nueva Transacción" if modo == "nuevo" else "Editar Transacción"
        ctk.CTkLabel(f, text=titulo, font=("Roboto", 20, "bold"), text_color="#333").pack(anchor="w", pady=(0, 20))

        # --- CAMPOS ---
        def crear_campo(label_text):
            ctk.CTkLabel(f, text=label_text, font=("Roboto Medium", 12), text_color="gray").pack(anchor="w", pady=(10, 2))
            entry = ctk.CTkEntry(f, height=35, corner_radius=8, border_width=1, border_color="#E5E7EB")
            entry.pack(fill="x")
            return entry

        ctk.CTkLabel(f, text="TIPO", font=("Roboto Medium", 12), text_color="gray").pack(anchor="w", pady=(10, 2))
        combo_tipo = ctk.CTkComboBox(f, values=["Gasto", "Ingreso"], height=35, corner_radius=8, state="readonly")
        combo_tipo.pack(fill="x")
        combo_tipo.set("Gasto")

        entry_monto = crear_campo("MONTO ($)")
        entry_fecha = crear_campo("FECHA (YYYY-MM-DD)")
        entry_fecha.insert(0, str(date.today()))
        entry_cat = crear_campo("CATEGORÍA")
        entry_desc = crear_campo("DESCRIPCIÓN")

        # Cargar datos si es editar
        if modo == "editar" and datos_editar:
            entry_monto.insert(0, datos_editar['monto'])
            entry_fecha.delete(0, "end"); entry_fecha.insert(0, datos_editar['fecha'])
            entry_cat.insert(0, datos_editar['categoria'])
            entry_desc.insert(0, datos_editar['descripcion'])
            combo_tipo.set(datos_editar['tipo'])

        def guardar():
            try:
                monto = float(entry_monto.get())
                fecha = entry_fecha.get()
                cat = entry_cat.get()
                desc = entry_desc.get()
                tipo = combo_tipo.get()

                if not cat or not fecha:
                    messagebox.showwarning("Atención", "Faltan datos obligatorios")
                    return

                if modo == "nuevo":
                    self.billetera.agregar_transaccion(monto, fecha, tipo, cat, desc)
                else:
                    self.billetera.editar_transaccion(datos_editar['id'], monto, fecha, tipo, cat, desc)
                
                top.destroy()
                self.actualizar_interfaz()
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número.")

        ctk.CTkButton(f, text="GUARDAR", height=45, corner_radius=10, font=("Roboto", 12, "bold"),
                      fg_color="#10B981", hover_color="#059669", command=guardar).pack(fill="x", pady=(30, 0))

    def abrir_editar(self):
        sel = self.tree.selection()
        if not sel: return
        val = self.tree.item(sel[0])['values']
        tags = self.tree.item(sel[0])['tags']
        tipo = "Ingreso" if "ingreso" in tags else "Gasto"
        monto_clean = str(val[3]).replace("$", "").replace(",", "").strip()
        
        datos = {'id': val[0], 'categoria': val[1], 'descripcion': val[2], 'monto': monto_clean, 'fecha': val[4], 'tipo': tipo}
        self.abrir_formulario(modo="editar", datos_editar=datos)

    def eliminar_registro(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            id_trans = self.tree.item(sel[0])['values'][0]
            self.billetera.eliminar_transaccion(id_trans)
            self.actualizar_interfaz()