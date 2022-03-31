import mysql.connector
from application.database import DATABASE_USERNAME,DATABASE_NAME, DATABASE_PASSWORD
from flask import flash
from application.affairs.models import Affair
from application.inventory.operations import get_product, get_company, update_stock_op
from application.users.operations import get_user
from datetime import datetime


def add_affair_op(affair,parent_id=None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        if parent_id is not None:
            c.execute("""INSERT INTO affair(name, status, close_date, amount, probability, origin, description, responsible_user, company,type_,invoice,parent_affair,matricule) VALUES( %s, %s, %s, %s,%s ,%s, %s, %s, %s, %s, %s,%s, %s) """
                    ,(affair.name, affair.status, affair.close_date, affair.amount, affair.probability, affair.origin, affair.description, affair.responsible_user, affair.company, affair.type, affair.invoice,parent_id, affair.matricule))
        else:
             c.execute("""INSERT INTO affair(name, status, close_date, amount, probability, origin, description, responsible_user, company,type_,invoice,matricule) VALUES( %s, %s, %s, %s,%s ,%s, %s, %s, %s, %s, %s, %s) """
                    ,(affair.name, affair.status, affair.close_date, affair.amount, affair.probability, affair.origin, affair.description, affair.responsible_user, affair.company, affair.type, affair.invoice, affair.matricule))
        c.execute("SELECT max(id) FROM affair ")
        affair_id = c.fetchone()[0]
        prods = []
        for element in affair.products:
            if '_' in element:
                temp = element.split('_')
                service_id = int(temp[0])
                quantity = float(temp[1])
                prods.append({
                    "quantity":quantity,
                    "service_id":service_id
                })
                c.execute("INSERT INTO affairService(service_id,quantity,affair_id) VALUES(%s,%s, %s)",(service_id, quantity,affair_id))
            
        if affair.status == 'Done':
            update_stock_op(affair,prods = prods)
        
        db.commit()
        flash('Affair successfully added!','success')
        
        return affair_id

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while inserting product.','danger')
    finally:
        c.close()
        db.close()


def edit_affair_op(affair):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        
        c.execute("""UPDATE affair SET name =%s, status=%s, close_date=%s, amount=%s, probability=%s, origin=%s, description=%s, responsible_user=%s, company=%s, invoice=%s, matricule=%s WHERE id = %s """
                    ,(affair.name, affair.status, affair.close_date, affair.amount, affair.probability, affair.origin, affair.description, affair.responsible_user, affair.company,affair.invoice,affair.matricule,affair.id))
        
        
        db.commit()
        flash('Affair successfully updated!','success')
        
        if affair.status == 'Done':
            update_stock_op(get_affair(affair_id=affair.id))

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured.','danger')
    finally:
        c.close()
        db.close()

def get_children_affairs(parent_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        if parent_id:
            c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE parent_affair = %s 
                     ORDER BY id desc""" ,(parent_id,))
       
        res = c.fetchall()

        affairs = []
        for r in res:
            c.execute("SELECT service_id,quantity FROM affairService WHERE affair_id = %s",(r[0],))
            prods = c.fetchall()

            products = []
            for p in prods:
                product = get_product(p[0])
                product.quantity = p[1]
                products.append(
                    product
                )

            affairs.append( Affair(
                id=r[0],
                name=r[1],
                date_created=r[2],
                status=r[3],
                close_date=r[4],
                amount=r[5],
                probability=r[6],
                origin=r[7],
                description=r[8],
                responsible_user=get_user(id=r[9]),
                company=get_company(company_id=r[10]),
                products=products,
                type=r[11],
                invoice=r[12],
                parent_id = r[13],
                matricule=r[14]

            ))
        return affairs

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while getting affair info.','danger')
    finally:
        c.close()
        db.close()


def get_affair(affair_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        
        c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE id = %s """
                    ,(affair_id, ))
        res = c.fetchone()

        c.execute("SELECT service_id,quantity FROM affairService WHERE affair_id = %s",(affair_id,))
        prods = c.fetchall()

        products = []
        for p in prods:
            product = get_product(p[0])
            product.quantity = p[1]
            products.append(
                product
            )
        
        return Affair(
            id=res[0],
            name=res[1],
            date_created=res[2],
            status=res[3],
            close_date=res[4],
            amount=res[5],
            probability=res[6],
            origin=res[7],
            description=res[8],
            responsible_user=get_user(id=res[9]),
            company=get_company(company_id=res[10]),
            products=products,
            type=res[11],
            invoice=res[12],
            parent_id = res[13],
            children_affairs = get_children_affairs(parent_id=res[0]),
            matricule=res[14]
        )

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while getting affair info.','danger')
    finally:
        c.close()
        db.close()



def get_affairs(responsible_user_id=None, company_id=None, dat=None, with_products=False,month=None,year=None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        if responsible_user_id:
            c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE responsible_user = %s and status != 'Done' and parent_affair is null
                     ORDER BY id desc""" ,(responsible_user_id,))
        elif company_id:
            c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE company = %s  and parent_affair is null
                     ORDER BY id desc""" ,(company_id,))
        elif dat:
            c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE DATE(date_created) = %s  
                     ORDER BY id desc""" ,(dat.replace('-','/'),))
        elif month and year:
            c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE EXTRACT(MONTH FROM date_created) = %s AND EXTRACT(YEAR FROM date_created) = %s  
                     ORDER BY id desc""" ,(month,year,))
        else:
            c.execute("""SELECT id, name, date_created, status, close_date, amount,
                            probability, origin, description, responsible_user, company, type_, invoice, parent_affair, matricule
                     FROM affair
                     WHERE parent_affair is null
                     ORDER BY id desc""")
        res = c.fetchall()

        affairs = []
        for r in res:
            if with_products:
                c.execute("SELECT service_id,quantity FROM affairService WHERE affair_id = %s",(r[0],))
                prods = c.fetchall()

                products = []
                for p in prods:
                    product = get_product(p[0])
                    product.quantity = p[1]
                    products.append(
                        product
                    )
            else:
                products = []
            affairs.append( Affair(
                id=r[0],
                name=r[1],
                date_created=r[2],
                status=r[3],
                close_date=r[4],
                amount=r[5],
                probability=r[6],
                origin=r[7],
                description=r[8],
                responsible_user=get_user(id=r[9]),
                company=get_company(company_id=r[10]),
                products=products,
                type=r[11],
                invoice=False,
                parent_id = r[13],
                matricule = r[14]

            ))
        return affairs

    except Exception as e:
        print('\n\n getaffairs',datetime.now(),e)
        flash('An error occured while getting affair info.','danger')
    finally:
        c.close()
        db.close()



def get_affair_years():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("SELECT DISTINCT EXTRACT(YEAR FROM close_date) FROM affair WHERE EXTRACT(YEAR FROM close_date) is not null")
        years = c.fetchall()
        return years        

    except Exception as e:
        print('\n\n get_affair_years',datetime.now(),e)
        flash('An error occured getting years.','danger')
    finally:
        c.close()
        db.close()

def link_product_to_affair_op(affair_id, products):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

       
        for element in products:
            if '_' in element:
                temp = element.split('_')
                service_id = int(temp[0])
                quantity = float(temp[1])
                c.execute("SELECT service_id,quantity FROM affairService WHERE service_id = %s and affair_id = %s",(service_id, affair_id))
                result = c.fetchone()
                if result:
                    c.execute("UPDATE affairService SET quantity = %s WHERE service_id = %s and affair_id = %s",(quantity+result[1],service_id, affair_id))
                else:
                    c.execute("INSERT INTO affairService(service_id,quantity,affair_id) VALUES(%s,%s, %s)",(service_id, quantity,affair_id))
            else:
                print("fail",element)
        
        db.commit()
        flash('Operation successful!','success')
        

    except Exception as e:
        print('\n\n',datetime.now(),e)
        flash('An error occured while inserting product.','danger')
    finally:
        c.close()
        db.close()



def set_affair_status_op(affair_id,status):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("""UPDATE affair SET status = %s WHERE id = %s""", ( status , affair_id))
        db.commit()
        flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()
