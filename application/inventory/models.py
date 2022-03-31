from application.users.models import Contact
from application.database import DATABASE_USERNAME,DATABASE_NAME, DATABASE_PASSWORD
import mysql.connector

class Service():
    
    def __init__(self,id,name,price,family,description,tax_category,estimated_cost,unity,quantity=None):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.family = family
        self.description = description
        self.tax_category = tax_category
        self.estimated_cost = estimated_cost
        self.type = 'Service'
        self.unity = unity
        

class Product(Service):

    def __init__(self,id,name,price,family,description,tax_category,estimated_cost,location,ean_upc,quantity=None,sku=None,unity=None):
        Service.__init__(self,id,name,price,family,description,tax_category,estimated_cost,unity,quantity)
        self.sku = sku 
        self.location = location
        self.ean_upc = ean_upc
        self.type ='Product' 


class Company:
    def __init__(self,contacts,name,id,remarks = None,affairs=None,matricule=None):
        self.contacts = contacts
        self.name = name
        self.id = id
        self.remarks =  remarks
        self.affairs=affairs
        self.matricule = matricule

    def update_remarks(self,remarks):
        try:
            db = mysql.connector.connect(
                host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
            )
            c = db.cursor()
            c.execute("UPDATE company SET remarks = %s WHERE id = %s",(remarks, self.id))
            db.commit()
        except Exception as e:
            print("update_remarks error: ",e)
        finally:
            c.close()
            db.close()