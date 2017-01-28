from rolepermissions.roles import AbstractUserRole

class Manager(AbstractUserRole):
    available_permissions = {
        'create_project': True,
        'edit_project': True,
        'delete_project': True,
        'create_task': True,
        'edit_task': True,
        'delete_task': True,
        'create_user': True,
        'edit_user': True,
        'delete_user': True,
    }

class Developer(AbstractUserRole):
    available_permissions = {}