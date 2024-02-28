from .phone import *
from .partition import *

def help():
    print("""
          
          
          Bu kütüphane CUCM üzerinde cihazların, partition'ların, CSS'lerin üzerinde değişiklik yapılmasına olanak sağlamaktadır.
          
          2 adet farklı kütüphane bulunmaktadır. Bunlar; phone ve partition.
         
         ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
          
          phone kütüphanesini çağırmak için : from CUCMLib import phone
          
          Bu kütüphane ile CUCM üzerindeki cihazlar üzerinde değişiklik yapılmaktadır. Detaylı bilgi için kütüphane çağırıldıktan sonra phone.help() komutunu çağırabilirsiniz.
          
         ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
          
          partition kütüphanesini çağırmak için : from CUCMLib import partition
          
          Bu kütüphane ile CUCM üzerindeki partition'lar üzerinde değişiklik yapılmaktadır. Detaylı bilgi için kütüphane çağırıldıktan sonra partition.help() komutunu çağırabilirsiniz.
          
          """)