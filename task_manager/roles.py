from rolepermissions.roles import AbstractUserRole

class Manager(AbstractUserRole):
    available_permissions = {
        'crud_projects': True,
        'crud_tasks': True,
        'crud_users': True,
    }

class Developer(AbstractUserRole):
    available_permissions = {}