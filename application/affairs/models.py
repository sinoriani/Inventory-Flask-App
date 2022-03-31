from calendar import month_name
from application.languages import LANG
from flask_login import current_user

class Affair:
    def __init__(self, id, name, date_created, status, close_date, amount, probability, origin, description, responsible_user, company,type=None, products=None,invoice=None,parent_id=None,children_affairs=None,matricule=None):
        curr_user = current_user
        self.id = id
        self.name = name
        self.date_created = date_created
        try:
            self.date_created_pretty = f"{date_created.day} { LANG[curr_user.lang].get(month_name[date_created.month],month_name[date_created.month]) } {date_created.year} {str(date_created.hour).zfill(2)}:{str(date_created.minute).zfill(2)} "
        except:
            self.date_created_pretty = str(date_created)
        self.status = status
        self.close_date= close_date
        self.amount = amount
        self.probability = probability
        self.origin = origin 
        self.description = description 
        self.responsible_user = responsible_user
        self.company = company
        self.products= products
        self.type = type
        self.close_date_pretty = f"{close_date.day} { LANG[curr_user.lang].get(month_name[close_date.month],month_name[close_date.month]) } {close_date.year} " if self.close_date else ''
        self.invoice = invoice
        self.parent_id = parent_id
        self.children_affairs = children_affairs
        self.matricule=matricule
