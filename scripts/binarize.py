import os, requests, hashlib, hmac, pandas as pd
TENANT_ID=os.environ["TENANT_ID"]; CLIENT_ID=os.environ["CLIENT_ID"]; CLIENT_SECRET=os.environ["CLIENT_SECRET"]
GRAPH="https://graph.microsoft.com/v1.0"; USER="claudio.vergara@hbclatina.cl"; DRIVE=f"/users/{USER}/drive"; ROOT="BI/Data BI BDD"
SENSITIVE={'Cadena':'RETAILER','Retail':'RETAILER','Cód. Cadena':'RETAILER','Código Local HBC':'STORE','Local':'STORE','Código Interno':'SKU','Marca':'BRAND','Proveedor':'SUPPLIER','Unidad de Negocio':'COMPANY','Descripción Producto':'PRODUCT'}
KEY=hashlib.pbkdf2_hmac('sha256',os.environ.get("VAULT_PASSWORD","default").encode(),b'empresa-001',100000,dklen=32)
def tok(cat,val):
    import hashlib as H
    h=hmac.new(KEY,f"{cat}:{val}".encode(),H.sha256).hexdigest()[:8].upper()
    return f"{cat[:4].upper()}-{h}"
def token():
    r=requests.post(f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token",data={"client_id":CLIENT_ID,"client_secret":CLIENT_SECRET,"scope":"https://graph.microsoft.com/.default","grant_type":"client_credentials"})
    r.raise_for_status(); return r.json()["access_token"]
def g(url,t):
    r=requests.get(url,headers={"Authorization":f"Bearer {t}","Accept":"application/json"}); r.raise_for_status(); return r.json()
def main():
    t=token()
    root=g(f"{GRAPH}{DRIVE}/root:/{ROOT}",t)
    items=g(f"{GRAPH}{DRIVE}/items/{root['id']}/search(q='.xlsx')",t).get("value",[])
    print(f"archivos: {len(items)}")
    os.makedirs("dist",exist_ok=True)
    open("dist/bundle-v1.br","wb").write(b"bundle fase1")
    print("fase1 ok")
if __name__=="__main__": main()
