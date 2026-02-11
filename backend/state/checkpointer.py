import sqlite3
import os
from langgraph.checkpoint.sqlite import SqliteSaver

def get_checkpointer():
    """
    Inicializa la persistencia en backend/data/, subiendo un nivel desde el script actual.
    """
    # 1. Obtenemos el directorio donde está checkpointer.py (ej: backend/state)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Subimos un nivel para llegar a la raíz de /backend
    backend_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    # 3. Definimos la ruta en backend/data
    db_dir = os.path.join(backend_root, "data")
    db_path = os.path.join(db_dir, "nexus_strategy.db")
    
    # 4. Creamos el directorio si no existe
    if not os.path.exists(db_dir):
        print(f"[STORAGE] Creando directorio en la raíz de backend: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    
    # 5. Conexión SQLite
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return SqliteSaver(conn) # Nota: SqliteSaver recibe la conexión directamente