from calendar import month_name
class Task:

    def __init__(self, id, name , date_created, due_date, priority, creator, assigned_user, description, due_hour,progress=None,status=None, awaitedTasks = None):
        self.id = id
        self.name = name
        self.date_created = date_created
        self.due_date = due_date
        self.priority = priority
        self.creator = creator
        self.assigned_user = assigned_user
        self.description = description
        self.due_hour = due_hour
        self.due_date_pretty = f"{due_date.day} {month_name[due_date.month][:3]}. {due_date.year} "
        self.awaitedTasks = awaitedTasks
        self.progress = progress
        self.status = status
        if date_created:
            self.date_created_pretty = f"{date_created.day} {month_name[date_created.month][:3]} {date_created.year} at {date_created.hour}:{date_created.minute} " 