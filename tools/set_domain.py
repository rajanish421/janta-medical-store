# Asli domain ek hi baar mein sab files mein lagane ke liye:  python tools/set_domain.py https://jantamedical.in
import os,sys
old="https://www.example.com";new=sys.argv[1].rstrip("/") if len(sys.argv)>1 else sys.exit("Use: python tools/set_domain.py https://aapka-domain.in")
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));n=0
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith((".html",".xml",".txt",".py",".json",".js")):
            p=os.path.join(dp,f);t=open(p,encoding="utf-8").read()
            if old in t:open(p,"w",encoding="utf-8").write(t.replace(old,new));n+=1
print("Updated",n,"files ->",new)
