import pandas as pd
from pymongo import MongoClient

# Tu URI de conexión a MongoDB Atlas (¡Asegúrate de que sea la misma que en app.py!)
MONGO_URI = "mongodb+srv://Jloyo:2580@cluster0.rbb8srm.mongodb.net/Paraguas?retryWrites=true&w=majority"
DB_NAME = "Paraguas"
MEDICAMENTOS_COLLECTION_NAME = "medicamentos"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    medicamentos_collection = db[MEDICAMENTOS_COLLECTION_NAME]

    # Lee tu archivo Excel. Reemplaza 'ruta/a/tu/archivo.xlsx' con la ubicación real de tu archivo.
    excel_file = pd.ExcelFile('C:/git/PP2/DB/Umbrella.xlsx')

    # Lee la primera hoja del Excel. Si tus datos están en otra hoja, cambia el índice.
    df = excel_file.parse(excel_file.sheet_names[0])

    # Mapea los nombres de las columnas de tu Excel a los nombres de los campos que quieres en MongoDB.
    # ¡ADAPTA ESTE DICCIONARIO SEGÚN LOS NOMBRES DE LAS COLUMNAS DE TU EXCEL!
    df = df.rename(columns={
        'PK': 'pk',
        'COD MONODROGA': 'cod_monodroga',
        'MONODROGA': 'monodroga',
        'ID PRESE. MONODROGA': 'id_prese_monodroga',
        'PRESE. MONODROGA': 'prese_monodroga',
        'CODIGO MEDICAMENTO': 'codigo_medicamento',
        'MEDICAMENTO': 'medicamento',
        'ID LABORATORIO': 'id_laboratorio',
        'LABORATORIO': 'laboratorio',
        'ID CATEGORIA': 'id_categoria',
        'CATEGORIA': 'categoria',
        'ID SUB CATEGORIA': 'id_sub_categoria',
        'SUB CATEGORIA': 'sub_categoria',
        'Trazabilidad': 'trazable'  # Asegúrate de que los valores sean True/False o conviértelos
        # Agrega aquí el resto de las columnas que necesites
    })

    # Convertir el DataFrame a una lista de diccionarios para insertar en MongoDB
    data_to_insert = df.to_dict('records')

    # Insertar los documentos en la colección 'medicamentos'
    if data_to_insert:
        result = medicamentos_collection.insert_many(data_to_insert)
        print(f"Se insertaron {len(result.inserted_ids)} medicamentos en la colección '{MEDICAMENTOS_COLLECTION_NAME}'.")
    else:
        print("No se encontraron datos para insertar.")

except Exception as e:
    print(f"Ocurrió un error durante la importación: {e}")

finally:
    if client:
        client.close()