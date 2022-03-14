from datetime import datetime


class System:
    def __init__(self):
        self.id = "4fc19f7c-8933-4e73-89cf-a6ce4e659b40"
        self.rev = "1866d3b"
        self.version = "2.36.5"
        self.date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%j")


class User:
    def __init__(self):
        self.lastUpdated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%j")
        self.id = ""
        self.created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%j")
        self.surname = ""
        self.firstName = ""
        self.userCredentials = None
        self.organisationUnits = [{"id": None}]
        self.dataViewOrganisationUnits = [{"id": None}]


class UserCredentials:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.displayName = ""
        self.username = ""
        self.password = ""
        self.userRoles = [{"id": None}]


# class UserGroup:
#     def __init__(self, _id, name):
#         self.created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%j")
#         self.lastUpdated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%j")
#         self.name = name
#         self.id = _id
#         self.publicAcces = "rw------"
#         self.lastUpdatedBy = {"id": ""}
#         self.user = {"id": ""}
#         self.userGroupAccesses = []
#         self.attributeValues = []
#         self.users = []
#         self.managedGroups = []
#         self.translations = []
#         self.userAccesses = []


class OrgUnit:
    def __init__(self, org_unit_id, code, name, short_name, level, parent):
        self.org_unit_id = org_unit_id
        self.code = code
        self.name = name
        self.shortName = short_name
        self.level = level
        self.parent = parent

