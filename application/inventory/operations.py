import mysql.connector
from application.database import DATABASE_USERNAME,DATABASE_NAME, DATABASE_PASSWORD
from flask import flash
from application.inventory.models import Product, Company, Service
from application.users.models import Contact
from datetime import datetime 
import json


class Family:
    def __init__(self,id,name):
        self.id = id
        self.name = name

def add_product_op(product):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        import random
        sku = str(random.randrange(9999999999))
        
        c.execute("""INSERT INTO service(name,family,description,tax_category,estimated_cost,unity) VALUES( %s, %s, %s, %s,%s, %s) """
                    ,(product.name,product.family,product.description,product.tax_category,product.estimated_cost, product.unity))
        c.execute("SELECT max(id) FROM service ")
        pid = c.fetchone()[0]
        c.execute("INSERT INTO product_information(service_id,quantity,price) VALUES(%s, %s, %s)",(pid, 0, product.price))
        
        if isinstance(product,Product):
            c.execute("INSERT INTO product(id, sku , ean_upc, location) VALUES(%s, %s, %s, %s)"
                        ,(pid, sku, product.ean_upc, product.location))
        
        db.commit()
        flash('Product successfully added!','success')
        

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while inserting product.','danger')
    finally:
        c.close()
        db.close()

def edit_product_op(product):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        pid = product.id

        c.execute("""UPDATE service SET name=%s,family=%s,description=%s,tax_category=%s,estimated_cost=%s,unity=%s WHERE id = %s"""
                    ,(product.name,product.family,product.description,product.tax_category,product.estimated_cost,product.unity,product.id))
        if isinstance(product,Product):
            c.execute("UPDATE product SET ean_upc = %s, location = %s WHERE id = %s",( product.ean_upc, product.location, product.id))
        
        c.execute("SELECT quantity, price FROM product_information WHERE service_id = %s ORDER BY dat desc limit 1",(pid,))
        res = c.fetchone()
        if res[1] != product.price:
            quantity = res[0]
            c.execute("INSERT INTO product_information(service_id,quantity,price) VALUES(%s, %s, %s)",(pid, quantity, product.price))
            
        db.commit()
        flash('Product successfully updated!','success')
        

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while updating product.','danger')
    finally:
        c.close()
        db.close()

def get_families():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute("SELECT name FROM product_family ")
        res = c.fetchall()
        families = []
        #families.append(("-1","None"))
        for r in reversed(res):
            families.append((r[0],r[0]))
        return families

    except Exception as e:
        print('\n\n',datetime.now(),e)
    finally:
        c.close()
        db.close()

def get_tax_categories(to_edit=None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute("SELECT name,value FROM tax_category ")
        res = c.fetchall()
        tax_categories = []
        #families.append(("-1","None"))
        if to_edit:
            for r in res:
                tax_categories.append((r[0],r[1] ) )
        else:
            for r in res:
                tax_categories.append((r[0],r[0]+ " " + "{:.1f} %".format(r[1] ) ) )
        return tax_categories

    except Exception as e:
        print('\n\n',datetime.now(),e)
    finally:
        c.close()
        db.close()

def get_products():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        #c.execute(""" SELECT p.id,p.name,inf.quantity,inf.price,p.family,inf.dat, p.description, p.tax_category, estimated_cost 
        #                FROM service p,product_information inf
        #                GROUP BY p.id,p.name,inf.quantity,inf.price,p.family,inf.dat, p.description, p.tax_category, estimated_cost
        #                HAVING inf.dat in (SELECT max(dat) FROM product_information WHERE service_id = p.id)""")
        
        c.execute(""" SELECT p.id,p.name,p.family, p.description, p.tax_category, estimated_cost ,unity
                        FROM service p""")
        res = c.fetchall()
        products = []
        for r in res:
            c.execute("SELECT sku, location, ean_upc FROM product WHERE id = %s",(r[0],))
            p = c.fetchone()

            c.execute("SELECt quantity, price FROM product_information WHERE service_id = %s order by dat desc limit 1",(r[0],))
            infos = c.fetchone()
            if p is not None:
                products.append(Product(
                    id=r[0],
                    name=r[1],
                    quantity=infos[0],
                    price=infos[1],
                    family=r[2],
                    sku = p[0] ,
                    description = r[3],
                    tax_category = r[4],
                    estimated_cost = r[5],
                    location = p[1] ,
                    ean_upc = p[2] ,
                    unity = r[6]
                ))
            else:
                products.append(Service(
                    id=r[0],
                    name=r[1],
                     quantity=infos[0],
                    price=infos[1],
                    family=r[2],
                    description = r[3],
                    tax_category = r[4],
                    estimated_cost = r[5],
                    unity = r[6]
                ))  
        
        return products

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while getting the products.','danger')
        return []
    finally:
        c.close()
        db.close()

def get_product(pid):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        #get the name and family of the product + the last updated price and quantity
        c.execute(""" SELECT p.id,p.name,inf.quantity,inf.price,p.family,inf.dat, p.description, p.tax_category, estimated_cost,unity
                        FROM service p,product_information inf
                        WHERE p.id = %s
                        GROUP BY p.id,p.name,inf.quantity,inf.price,p.family,inf.dat,  p.description, p.tax_category, estimated_cost
                        HAVING inf.dat in (SELECT max(dat) FROM product_information WHERE service_id = p.id)""", (pid,))
        r = c.fetchone()
        c.execute("SELECT sku, location, ean_upc FROM product WHERE id = %s",(r[0],))
        p = c.fetchone()
        print('\n\n\n',r[2])
        if p is not None:
            product = Product(
                    id=r[0],
                    name=r[1],
                    quantity=r[2],
                    price=r[3],
                    family=r[4],
                    sku = p[0] ,
                    description = r[6],
                    tax_category = r[7],
                    estimated_cost = r[8],
                    location = p[1] ,
                    ean_upc = p[2] ,
                    unity = r[9]
                )
        else:
            product = Service(
                    id=r[0],
                    name=r[1],
                    quantity=r[2],
                    price=r[3],
                    family=r[4],
                    description = r[6],
                    tax_category = r[7],
                    estimated_cost = r[8],
                    unity = r[9]
                )
        c.execute("SELECT CAST(inf.dat AS DATE),inf.price,inf.quantity FROM service p, product_information inf WHERE p.id = inf.service_id and p.id = %s",(pid,))
        res = c.fetchall()
        history = []
        for r in res:
            history.append(
                {
                    'date':str(r[0]),
                    'price':r[1],
                    'quantity':r[2]
                }
            )
        price_history = [{
            'date':history[0]['date'] ,
            'price':history[0]['price'] 
        }]
        quantity_history = [{
            'date':history[0]['date'] ,
            'quantity':history[0]['quantity'] 
        }]

        last_price = history[0]['price'] 
        last_quantity = history[0]['quantity'] 


        for h in history:
            if last_price != h['price']:
                last_price = h['price']
                price_history.append({
                    'date':h['date'],
                    'price':h['price']
                })
            if last_quantity != h['quantity']:
                last_quantity = h['quantity']
                quantity_history.append({
                    'date':h['date'],
                    'quantity':h['quantity']
                })

        product.price_history = price_history
        product.quantity_history = quantity_history
        return product

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while getting the products.','danger')
        return []
    finally:
        c.close()
        db.close()

def add_company_op( company_name,contact_name,contact_surname,contact_email,contact_phone , company_remarks, matricule):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute("INSERT INTO company(name,remarks,matricule) VALUES(%s,%s,%s)",(company_name,company_remarks,matricule))
        c.execute('SELECT max(id) FROM company')
        company_id = c.fetchone()[0]
        c.execute("INSERT INTO contact(name,surname,email) VALUES(%s, %s, %s)",(contact_name,contact_surname,contact_email))
        c.execute('SELECT max(id) FROM contact')
        contact_id = c.fetchone()[0]
        c.execute("INSERT INTO companyContact(company_id,cid) VALUES(%s, %s)",(company_id, contact_id))
        c.execute("INSERT INTO contactTelephone(num, uid) VALUES(%s, %s)",(contact_phone, contact_id))
        db.commit()
        flash('company added','success')

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()

def get_companies():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute(""" SELECT s.id, s.name , s.matricule
                        FROM company s """)
        res = c.fetchall()
        companies = []
        for r in res:
            company_id = r[0]
            company_name = r[1]
            matricule = r[2]

            c.execute("""SELECT c.id, c.email, c.name, c.surname 
                            FROM contact c, companyContact sc
                            WHERE c.id = sc.cid and sc.company_id = %s""", (company_id,))
            res2 = c.fetchall()
            contacts = []
            for r2 in res2:
                contact_id = r2[0]
                c.execute("""SELECT num, uid FROM contactTelephone WHERE uid = %s """, (contact_id, ))
                res3 = c.fetchall()
                numsTel = []
                for r3 in res3:
                    numsTel.append(r3[0])

            contacts.append(
                Contact(
                    id=r2[0],
                    email=r2[1],
                    name=r2[2],
                    surname=r2[3],
                    numsTel=numsTel
                )
            )
            companies.append(
                Company(
                    contacts = contacts,
                    name=company_name,
                    id=company_id,
                    matricule=matricule
                )
            )

        return companies

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        c.close()
        db.close()

def get_company(company_id):

    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        cursor = db.cursor(buffered=True)
    
        cursor.execute(""" SELECT s.id, s.name, s.remarks, s.matricule
                        FROM company s
                        WHERE s.id = %s """, (company_id,))
        res = cursor.fetchone()
        if res is  None:
            return None
        company_id = res[0]
        company_name = res[1]
        company_remarks = res[2]
        matricule = res[3]

        cursor.execute("""SELECT c.id, c.email, c.name, c.surname 
                        FROM contact c, companyContact sc
                        WHERE c.id = sc.cid and sc.company_id = %s""", (company_id,))
        res2 = cursor.fetchall()
        contacts = []
        for r2 in res2:
            contact_id = r2[0]
            cursor.execute("""SELECT num, uid FROM contactTelephone WHERE uid = %s """, (contact_id, ))
            res3 = cursor.fetchall()
            numsTel = []
            for r3 in res3:
                numsTel.append(r3[0])

            contacts.append(
                Contact(
                    id=r2[0],
                    email=r2[1],
                    name=r2[2],
                    surname=r2[3],
                    numsTel=numsTel
                )
            )


        company = Company(
                    contacts = contacts,
                    name=company_name,
                    id=company_id,
                    remarks = company_remarks,
                    matricule=matricule
                )
        return  company
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        cursor.close()
        db.close()   
     
def link_company_to_product_op(company_id, product_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute("""INSERT INTO companyService(company_id, product_id) VALUES(%s, %s) """,(company_id, product_id))
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        c.close()
        db.close()

    
def link_contact_to_company_op(company_id, contact):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute("INSERT INTO contact(name,surname,email) VALUES(%s, %s, %s)",(contact.name,contact.surname,contact.email))
        c.execute('SELECT max(id) FROM contact')
        contact_id = c.fetchone()[0]
        c.execute("INSERT INTO companyContact(company_id,cid) VALUES(%s, %s)",(company_id, contact_id))
        c.execute("INSERT INTO contactTelephone(num, uid) VALUES(%s, %s)",(contact.numsTel[0], contact_id))
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        c.close()
        db.close()


def remove_contact_from_company_op(company_id, contact_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute("DELETE FROM companyContact WHERE company_id =%s and cid = %s",(company_id, contact_id))
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        c.close()
        db.close()


def get_companies_for_product_op(product_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute(""" SELECT s.name, s.id FROM company s
                      WHERE s.id IN (SELECT company_id 
                                     FROM companyService
                                     WHERE product_id = %s) """,(product_id, ))
        res = c.fetchall()
        companies = []
        for r in res:
            company_name = r[0]
            company_id = r[1]
            companies.append(
                Company(
                    contacts = None,
                    name=company_name,
                    id=company_id
                )
            )

        return companies

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        c.close()
        db.close()

def get_products_for_company_op(company_id):
    """if the company id is provided: returns the products of that company
        otherwise it returns all the products in the stock list """
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        if company_id is not None:
            c.execute(""" SELECT p.id FROM service p
                        WHERE p.id IN (SELECT product_id 
                                        FROM companyService
                                        WHERE company_id = %s) """,(company_id, ))
        else:
            c.execute(""" SELECT p.id FROM service p
                        WHERE p.id """)
        res = c.fetchall()
        products = []
        for r in res:
            product_id = r[0]
            products.append(
                get_product(pid=product_id)
            )

        return products

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
        return []
    finally:
        c.close()
        db.close()

def add_family_op(name, parent_family):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute(""" INSERT INTO product_family(name, family) VALUEs(%s, %s) """,(name, parent_family ))
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('Family already exists.','danger')
    finally:
        c.close()
        db.close()

def add_tax_category_op(name, value):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute(""" INSERT INTO tax_category(name, value) VALUES(%s, %s) """,(name, value ))
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('Category already exists.','danger')
    finally:
        c.close()
        db.close()

def edit_tax_op(name, value):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
    
        c.execute(""" UPDATE tax_category SET value = %s WHERE name = %s """,( value, name ))
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('Category already exists.','danger')
    finally:
        c.close()
        db.close()

def update_stock_op(affair,prods= None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        if prods:
            for p in prods:
                product_id = p["service_id"]
                quantity = p["quantity"]
                c.execute("SELECT quantity, price FROM product_information WHERE service_id = %s order by dat desc limit 1",(product_id,))
                res = c.fetchone()
                if affair.type == 'Sale':
                    c.execute("INSERT INTO product_information(service_id, quantity , price) VALUES(%s,%s, %s)",(product_id,  res[0]-quantity , res[1]))
                else:
                    c.execute("INSERT INTO product_information(service_id, quantity , price) VALUES(%s,%s, %s)",(product_id,  res[0]+quantity , res[1]))
        else:        
            for p in affair.products:
                product_id = int(p) if isinstance(p,str) else p.id
                c.execute("SELECT quantity, price FROM product_information WHERE service_id = %s order by dat desc limit 1",(product_id,))
                res = c.fetchone()
                if affair.type == 'Sale':
                    c.execute("INSERT INTO product_information(service_id, quantity , price) VALUES(%s,%s, %s)",(product_id,  res[0]-p.quantity , res[1]))
                else:
                    c.execute("INSERT INTO product_information(service_id, quantity , price) VALUES(%s,%s, %s)",(product_id,  res[0]+p.quantity , res[1]))
                    
        db.commit()
        flash('Operation successful','success')
    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while updating stock.','danger')
    finally:
        c.close()
        db.close()
