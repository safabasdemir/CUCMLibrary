from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from lxml import etree
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

with open('information.json', 'r') as config_file:
    config = json.load(config_file)

disable_warnings (InsecureRequestWarning)

username = config["username"]
password = config["password"]
fqdn = config["fqdn"]
address = 'https://{}:8443/axl/'.format(fqdn)
wsdl = 'AXLAPI.wsdl'
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth (username , password)
transport = Transport(cache=SqliteCache(), session=session , timeout=20)
history = HistoryPlugin()
client = Client(wsdl = wsdl , transport = transport , plugins =[ history ])
axl = client.create_service( binding , address )

def show_history() :
    for item in [history.last_sent , history.last_received ]:
        print (etree.tostring ( item ["envelope"] , encoding ="unicode", pretty_print = True ))

###################################################################################################################################


def Help():
    print("""
          
          Bu kütüphane ile partition ile ilgili geliştirmeler yapılabilmektedir.
          
          listPartition() -> Bu fonksiyon ile Call Manager'a kayıtlı partition'ları consol ekranına listelemektedir. Deaylı bilgi için listPartitionHelp() fonksiyonunu çağırınız.
          
          listPartitionCsv() -> Bu fonksiyon ile Call Manager'a kayıtlı partition'ları CVS formatında fonksiyonun çağırıldığı klasöre kaydetmektedir. Detaylı bilgi için listPartitionCsvHelp() fonksiyonunu çağırınız.
          
          addPartitionExcel() -> Bu fonksiyon ile Call Manager'a yeni partition eklemek için kullanılmaktadır. Deaylı bilgi için addPartitionExcelHelp() fonksiyonunu çağırınız.
          
          removePartitionExcel() -> Bu fonksiyon ile Call Manager'da bulunan partition'u silmek için kullanılmaktadır. Deaylı bilgi için removePartitionExcelHelp() fonksiyonunu çağırınız.
          
          """  
    )

def addPartitionExcel():
    df_devices = pd.read_excel("partitionList.xlsx")
    
    veri = df_devices.to_dict()
    
    for item in veri.keys():
        arr = []
        for key in veri[item].keys():
            value = veri[item][key]
            if pd.isna(value):
                value = None
            arr.append(value)
        
        veri[item] = arr
        
    i = 0
    while (len(veri["Name"])) > i:
        add_list = axl.addRoutePartition(
            routePartition={
                "name":veri["Name"][i],
                "description":veri["Description"][i]
            })
        i = i + 1

def addPartitionExcelHelp():
    print("""
          
        Bu  fonksiyon ile CUCM'a yeni partition eklenmektedir. Fakat bu partition'un bilgilerini partitionList.xlsx olarak kayıt edilmesi gerekmektedir.
        
        Bu fonksiyonu çalıştırmak için yapılması gerekenler:
        
            1 - Bu fonksiyonu çalıştıracağınız klasörün içerisine partitionList.xlsx adında bir excel dosyası oluşturun.
            
            2 - Bu excel dosyasında 2 adet sütun olmalıdır. Bu sütunların isimleri sırasıyla Name - Description olacaktır.
            
            3 - İlgili sütununda yüklemek istediğiniz cihazın bilgileri doldurun. Örneğin Name sütunu içerisine sırayla yüklemek istediğiniz cihazların isimlerini yazınız.
            
            4 - Excel dosyasını kaydedin ve kapatın.
            
            5 - addPartitionExcelCsv() fonksiyonunu çağırarak gerekli eklemeyi yapabilirsiniz.
            
        
        NOTLAR:
        
            1 - Name kısmı zorunlu alandır. Bu alanın doldurulması gerekmektedir. Fakat Description kısmı isteğe bağlıdır. Boş bırakılabilmektedir.
            
            2 - Eğer sadece Name kısmı doldurulursa, diğer ayarlar varsayılan olarak boş gelmektedir.
        """)
                
def listPartition():
    
    list_partition = axl.listRoutePartition(searchCriteria={"name":"%"}, returnedTags={"name":""})

    veri = {
    "Name": [],
    "Description": []
    }
    
    for partition in list_partition["return"]["routePartition"]:
        get_partition = axl.getRoutePartition(name = partition["name"])
    
        names = get_partition["return"]["routePartition"]["name"]
        description = get_partition["return"]["routePartition"]["description"]

        veri["Name"].append(names)
        veri["Description"].append(description)
    

    print(veri)

def listPartitionHelp():
    print("""
          Bu fonksiyon çağırıldığında Call Manager üzeride bulunan partition'ları consol ekranında listemektedir. Fakat partition üzerinde bulunan bütün özellikleri listelememektedir.
        
          Liste sırasında verilecek olan bilgiler:
          
          Name  -  Description
          
          Bu bilgiler haricinde bulunan bilgiler listelenmemektedir.
       
          """
    )
    
def removePartitionExcel():
    df_devices = pd.read_excel("removePartitionList.xlsx")

    veri = df_devices.to_dict()

    for item in veri.keys():
        arr = []
        for key in veri[item].keys():
            value = veri[item][key]
            if pd.isna(value):
                value = None
            arr.append(value)
        
        veri[item] = arr


    i = 0
    while (len(veri["Name"])) > i:
        remove_partition = axl.removeRoutePartition(
            
                name = veri["Name"][i],  
            
        )
        i = i + 1

def removePartitionExcelHelp():
    print("""
        Bu  fonksiyon ile CUCM'da bulunan partition'ları silmektedir. Silinmesi istenen partition bilgilerini removePartitionList.xlsx olarak kayıt edilmesi gerekmektedir.
        
        Bu fonksiyonu çalıştırmak için yapılması gerekenler:
        
            1 - Bu fonksiyonu çalıştıracağınız klasörün içerisine removePartitionList.xlsx adında bir excel dosyası oluşturun.
            
            2 - Bu excel dosyasında 1 adet sütun olmalıdır. Bu sütunun ismi Name olmalıdır.
            
            3 - İlgili sütununda değiştirmek istediğiniz partition isimlerini yazınız.
            
            4 - Excel dosyasını kaydedin ve kapatın.
            
            5 - removePartitionList() fonksiyonunu çağırarak gerekli silmeyi yapabilirsiniz.
        
        """)
       
def listPartitionCsv():
    list_partition= axl.listRoutePartition(searchCriteria={"name":"%"}, returnedTags={"name":""})

    veri = {
        "Name": [],
        "Description": []
    }

    for partition in list_partition["return"]["routePartition"]:
        get_partition = axl.getRoutePartition(name = partition["name"])
    
        names = get_partition["return"]["routePartition"]["name"]
        description = get_partition["return"]["routePartition"]["description"]

        veri["Name"].append(names)
        veri["Description"].append(description)
    

    veri_listesi = pd.DataFrame(veri)

    veri_listesi.to_csv('PartitionList.csv', index=False)
  
def listPartitionCsvHelp():
    print("""
    Bu kütüphane ile CUCM'da bulunan partition bilgilerini, bulunduğu klasöre CSV formatında kaydetmektedir.
    
    Kaydedilen bilgiler : Name  -  Description
          
    Bu bilgiler haricinde bulunan bilgiler yazılmamaktadır.
    
    """)