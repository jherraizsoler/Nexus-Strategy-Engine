import sqlite3
import os
from langgraph.checkpoint.sqlite import SqliteSaver

def get_checkpointer():
    """
    Inicializa la persistencia dentro de backend/data/ y retorna el motor de 
    persistencia para el Nexus Strategy Engine.
    Garantiza que el estado de los hilos de ejecución se mantenga en una base de datos local.
    """
    # 1. Forzamos la ruta relativa a la carpeta 'backend/data'
    # Usamos __file__ para asegurar que siempre se cree relativa a este script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(base_dir, "data")
    db_path = os.path.join(db_dir, "nexus_strategy.db")
    
    # 2. Creamos backend/data si no existe
    if not os.path.exists(db_dir):
        print(f"[STORAGE] Creando directorio interno: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    
    # 3. Conexión SQLite
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return SqliteSaver(conn)