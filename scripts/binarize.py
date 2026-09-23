import os
os.makedirs("dist", exist_ok=True)
open("dist/bundle.bin","wb").write(b"bundle 379k placeholder v1")
print("dummy bundle creado")
