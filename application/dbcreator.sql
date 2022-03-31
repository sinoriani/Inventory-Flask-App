CREATE TABLE contact(
    id integer primary key AUTO_INCREMENT,
    email varchar(120) unique not null,
    surname varchar(25),
    name varchar(25)
);
CREATE TABLE user(
    id integer references contact(id),
    username varchar(20)   null,
    image_file char(20) not null default 'default.jpg',
    password char(60) not null,
    lang char(2) default 'FR'
);
CREATE TABLE role(type varchar(15) primary key );
CREATE TABLE user_role(uid integer references user(id) , role varchar(15) references role(type) ,primary key(uid,role));
CREATE TABLE company(
        id integer primary key AUTO_INCREMENT,
        name varchar(150),
        matricule varchar(20) default '',
        remarks text
);
CREATE TABLE companyContact(
        cid integer references contact(id),
        company_id integer references company(id),
        primary key(company_id,cid)
);
CREATE TABLE telephone(
        num varchar(20) primary key
);
CREATE TABLE contactTelephone(
        num varchar(20) references telephone(num),
        uid integer references contact(id),
        primary key(uid,num)
);
CREATE TABLE product_family(
        name varchar(150) primary key,
        family varchar(150) references product_family(name)
);
CREATE TABLE tax_category(
        name varchar(20) primary key,
        value real
);
CREATE TABLE service(
        id integer primary key auto_increment,
        name varchar(150),
        description varchar(250),
        estimated_cost real,
        unity varchar(10) default '',
        tax_category varchar(20) references tax_category(name),
        family varchar(150) references product_family(name)
);
CREATE TABLE product(
        id integer references service(id),
        sku varchar(20),
        ean_upc varchar(13),
        location varchar(25)
);
CREATE TABLE product_information(
        service_id integer references service(id),
        dat datetime default current_timestamp,
        quantity real,
        price real,
        primary key(dat,service_id)
);
CREATE TABLE companyProduct(
        company_id integer references company(id),
        product_id integer references service(id),
        primary key(company_id,product_id)
);
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
);
CREATE TABLE taskAwait(
        waitingTaskId integer references task(id),
        awaitedTaskId integer references task(id)
);
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
        invoice boolean,
        parent_affair integer references affair(id),
        type_ varchar(20),
        matricule varchar(20) 
);
CREATE table affairService(
        affair_id integer references affair(id),
        service_id integer references service(id),
        quantity real,
        primary key(affair_id, service_id)
);
CREATE TABLE operationRole(
        operation varchar(150),
        role_name varchar(15) references role(type),
        primary key(role_name, operation)
);

CREATE TABLE companyService(
    product_id int references service(id),
    company_id int references service(id),
);

CREATE TABLE presence(
        user_id integer REFERENCES user(id),
        dat date,
        clock_in char(5),
        clock_out char(5),
        primary key(user_id,dat)
);

INSERT INTO contact(name,email) VALUES('Admin','sampleuser@gmail.com');
INSERT INTO role(type) VALUES('Admin');
INSERT INTO user_role(uid,role) VALUES(1,'Admin');
INSERT INTO tax_category(name,value) VALUES('Normal',19);
INSERT INTO operationRole(operation,role_name) VALUES('Add affairs' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Add company' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Add products' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Add tasks' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Add users' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Check affairs list' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Check companies list' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Check products list' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Check tasks list' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Check users list' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Edit affairs' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Edit company' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Edit products' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Edit tasks' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Postpone tasks' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Update affair status' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Update parameters' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Update task status' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Check daily report' ,'Admin' );
INSERT INTO operationRole(operation,role_name) VALUES('Add presence' ,'Admin' );


