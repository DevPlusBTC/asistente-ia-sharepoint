import os, requests, hashlib, hmac, pandas as pd, numpy as np
TENANT_ID=os.environ["TENANT_ID"]; CLIENT_ID=os.environ["CLIENT_ID"]; CLIENT_SECRET=os.environ["CLIENT_SECRET"]
GRAPH="https://graph.microsoft.com/v1.0"; ROOT_PATH="BI/Data BI BDD"
SENSITIVE={'Cadena':'RETA','Retail':'RETA','Cód. Cadena':'RETA','Código Local HBC':'STORE','Local':'STORE','Código Interno':'SKU','Marca':'BRAN','Proveedor':'SUPP','Unidad de Negocio':'COMP','Descripción Producto':'PROD'}
VAULT_KEY=hashlib.pbkdf2_hmac('sha256', os.environ.get("VAULT_PASSWORD","default").encode(), b'empresa-001', 100000, dklen=32)
def tokenize(cat,val):
    h=hmac.new(VAULT_KEY, f"{cat}:{val}".encode(), hashlib.sha256).hexdigest()[:8].upper()
    return f"{cat[:4].upper()}-{h}"
def get_token():
    r=requests.post(f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token", data={"client_id":CLIENT_ID,"client_secret":CLIENT_SECRET,"scope":"https://graph.microsoft.com/.default","grant_type":"client_credentials"})
    r.raise_for_status(); return r.json()["access_token"]
def graph_get(url,token):
    r=requests.get(url, headers={"Authorization":f"Bearer {token}","Accept":"application/json"}); r.raise_for_status(); return r.json()
# TODO: implementar listado .xlsx en ROOT_PATH, lectura worksheets chunked (1000 filas), tokenización SENSITIVE, escritura data.parquet + embeddings.bin (packbits)
if __name__=="__main__":
    tok=get_token()
    print("Token OK, listo para compilar 379k con tokenización 10 columnas")
