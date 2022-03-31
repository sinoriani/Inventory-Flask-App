import mysql.connector
import time
import json
DATABASE_USERNAME = "yassine" 
DATABASE_PASSWORD = ""
#DATABASE_NAME = "inventory"

with open('dbname.json')  as f:
    DATABASE_NAME = json.load(f).get('name')

db = mysql.connector.connect(
    host='localhost',
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME,
    auth_plugin='mysql_native_password'
)
c = db.cursor(buffered=True)

db.close()
c.close()


contactQuery = """CREATE TABLE contact(
    id integer primary key AUTO_INCREMENT,
    email varchar(120) unique not null,
    surname varchar(25),
    name varchar(25)
)"""


userQuery = """CREATE TABLE user(
    id integer references contact(id),
    username varchar(20)   null,
    image_file char(20) not null default 'default.jpg',
    password char(60) not null,
    lang char(2) default 'FR'
)"""

roleQuery = "CREATE TABLE role(type varchar(15) primary key )"
user_roleQuery = "CREATE TABLE user_role(uid integer references user(id) , role varchar(15) references role(type) ,primary key(uid,role))"

companyQuery = """ 
    CREATE TABLE company(
        id integer primary key AUTO_INCREMENT,
        name varchar(150)
    )
"""

companyContactQuery = """ 
    CREATE TABLE companyContact(
        cid integer references contact(id),
        company_id integer references company(id),
        primary key(company_id,cid)
    )
"""



telephoneQuery = """ 
    CREATE TABLE telephone(
        num varchar(20) primary key
    )
"""

contactTelephoneQuery = """ 
    CREATE TABLE contactTelephone(
        num varchar(20) references telephone(num),
        uid integer references contact(id),
        primary key(uid,num)
    )
"""

prodFamilyQuery = """ 
    CREATE TABLE product_family(
        name varchar(150) primary key,
        family varchar(150) references product_family(name)
    )
"""



taxCategoryQuery = """ 
    CREATE TABLE tax_category(
        name varchar(20) primary key,
        value real
    )
"""
taxCategoryInserts = [
    "INSERT INTO tax_category(name,value) VALUES('Normal',0.19)"
]


serviceQurery = """ 
    CREATE TABLE service(
        id integer primary key auto_increment,
        name varchar(150),
        description varchar(250),
        estimated_cost real,
        tax_category varchar(20) references tax_category(name),
        family varchar(150) references product_family(name)
    )
"""


productQurery = """ 
    CREATE TABLE product(
        id integer references service(id),
        sku varchar(20),
        ean_upc varchar(13),
        location varchar(25)
    )
"""

productInformationQuery = """ 
    CREATE TABLE product_information(
        service_id integer references service(id),
        dat datetime default current_timestamp,
        quantity integer,
        price real,
        primary key(dat,service_id)
    )
"""


companyProductQuery = """ 
    CREATE TABLE companyService(
        company_id integer references company(id),
        product_id integer references service(id),
        primary key(company_id,product_id)
    )
"""


taskQuery = """ 
    CREATE TABLE task(
        id integer primary key auto_increment,
        name varchar(100),
        description text,
        priority varchar(15),
        creator integer references user(id),
        assigned_user integer references user(id),
        date_created timestamp DEFAULT CURRENT_TIMESTAMP,
        due_date date,
        due_hour char(5),
        status varchar(20) DEFAULT 'Waiting',
        progress int default 0
    )
"""

taskAwaitQuery = """ 
    CREATE TABLE taskAwait(
        waitingTaskId integer references task(id),
        awaitedTaskId integer references task(id)
    )
"""


affairQuery = """ 
    CREATE TABLE affair(
        id integer primary key auto_increment,
        name varchar(150),
        date_created timestamp DEFAULT CURRENT_TIMESTAMP,
        status varchar(20) DEFAULT 'Waiting',
        close_date date,
        amount real,
        probability integer,
        origin varchar(100),
        description text,
        responsible_user integer references user(id),
        company integer references company(id),
        type_ varchar(20)
    )
"""

affairServiceQuery = """ 
    CREATE table affairService(
        affair_id integer references affair(id),
        service_id integer references service(id),
        quantity integer,
        primary key(affair_id, service_id)
    )
"""

operationRoleQuery = """ 
    CREATE TABLE operationRole(
        operation varchar(150),
        role_name varchar(15) references role(type),
        primary key(role_name, operation)
    )
"""

#db.commit()