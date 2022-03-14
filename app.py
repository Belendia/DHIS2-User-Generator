import json
import csv
import os
import sys
import getopt
from libs.models import User, UserCredentials, System, OrgUnit
from libs.utils import Utils


class Parser:
    def __init__(self, generate_type):
        self.generate_type = generate_type
        self.org_units_filename = 'metadata/OrgUnits.json'
        self.users_json_file_name = 'output/users.json'
        self.users_csv_file_name = 'output/users.csv'
        self.org_units = {}
        self.uids = []
        self.usernames = []

        if not os.path.exists('output'):
            os.makedirs('output')

        self.read_org_units()

    def read_org_units(self):
        with open(self.org_units_filename) as f:
            org_units = json.load(f)

            for ou in org_units['organisationUnits']:
                self.org_units[ou['id']] = OrgUnit(ou['id'], ou['code'] if 'code' in ou else '', Utils.clean(ou['name']),
                                                   Utils.clean(ou['shortName']), int(ou['level']),
                                                   ou['parent']['id'] if 'parent' in ou else None)
            print(len(self.org_units))

    def generate_unique_uid(self):
        generate = True
        uid = ""
        while generate:
            uid = Utils.generate_uid()
            if uid not in self.uids:
                self.uids.append(uid)
                generate = False
        return uid

    def generate_unique_username(self, name):
        generate = True
        username = Utils.generate_username(name)
        while generate:
            if username not in self.usernames:
                self.usernames.append(username)
                generate = False
            else:
                username = Utils.generate_unique_username(Utils.generate_username(name))
        return username

    def prep_user(self, org_unit):
        user = User()
        user.id = self.generate_unique_uid()
        user.firstName = org_unit.shortName
        user.surname = "  "
        user.organisationUnits[0]['id'] = org_unit.org_unit_id
        user.dataViewOrganisationUnits[0]['id'] = org_unit.parent

        uc = UserCredentials()
        uc.id = self.generate_unique_uid()
        uc.name = user.firstName
        uc.displayName = uc.name
        uc.username = self.generate_unique_username(org_unit.shortName)
        uc.password = Utils.generate_password()

        uc.userRoles[0]['id'] = "YIJeGsUSjNr" if Utils.is_health_facility(org_unit) else "AuZEB5LnUHs"

        user.userCredentials = uc
        return user

    def prep_users(self):
        users = []
        for key, org_unit in self.org_units.items():
            users.append(self.prep_user(org_unit))
        return users

    def prep_groups(self):
        pass
        # groups = [UserGroup("W9zmctpZOB3", "PHEM Data Analysts"), UserGroup(
        #     "D7m0m53iGn5", "PHEM Users"), UserGroup("ymuSfWE4QPG", "PHEM Data Encoders")]
        # for i, row in dataset.iterrows():
        #     for j in range(groups.__len__()):
        #         groups[j].users.append({'id': row['user_uid']})
        #
        # return groups

    def write_json_to_file(self, file_name, json_data):
        try:
            with open(file_name, 'w') as f:
                f.write(json_data)
            return True
        except:
            return False

    def write_to_csv_file(self, users):
        header = ['id', 'First Name', 'Sur Name', 'User Name', 'Password', 'Org Units ID', 'National', 'Region',
                  'Zone', 'Woreda', 'PHCU', 'Facility', 'SubFacility']
        try:
            with open(self.users_csv_file_name, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for user in users:
                    row = [user.id, user.firstName, user.surname, user.userCredentials.username,
                           user.userCredentials.password, user.organisationUnits[0]['id']]
                    hierarchy = Utils.generate_org_units_hierarchy(self.org_units, user.organisationUnits[0]['id'])
                    row.extend(hierarchy)
                    writer.writerow(row)

                return True
        except:
            return False

    def generate_users(self):
        return self.prep_users()

    def generate_group(self):
        return self.prep_groups()

    def generate(self):
        print("Please wait ... ", end="")

        data = {'system': System()}

        filename = ""
        if self.generate_type == "user":
            data['users'] = self.generate_users()
            filename = self.users_json_file_name
        else:  # groups
            # data['userGroups'] = self.generate_group(dataset)
            # filename = self.groups_filename
            pass

        print('Done')
        print("Writing to json file ... ", end="")
        if (self.write_json_to_file(
                filename, json.dumps(data, default=lambda o: o.__dict__, indent=4))):
            print("done")
            print("File is written to {}".format(filename))
        else:
            print("done")
            print("Error writing file to {}".format(self.users_json_file_name))

        if self.generate_type == "user":
            print("Writing to csv file ... ", end="")
            if self.write_to_csv_file(data['users']):
                print("done")
                print("File is written to {}".format(self.users_csv_file_name))
            else:
                print("done")
                print("Error writing file to {}".format(self.users_csv_file_name))

    @staticmethod
    def help():
        print('app.py -g user')
        print('app.py --generate user')
        print('app.py -g group')
        print('app.py --generate group')


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg:", ["generate="])
    except getopt.GetoptError:
        Parser.help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            Parser.help()
            sys.exit()
        elif opt in ("-g", "--generate"):
            if arg.lower() in ("user", "group"):
                parser = Parser(arg.lower())
                parser.generate()
            else:
                Parser.help()
