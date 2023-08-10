class Device:
    
    def __init__(self,name,manufacture,R,G,B,vias):
        self.name=name
        
        self.manufacture=manufacture
        self.R=int(R)
        self.G=int(G)        
        self.B=int(B)
        self.vias=int(vias)
    