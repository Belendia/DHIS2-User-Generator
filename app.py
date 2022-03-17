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
                self.org_units[ou['id']] = OrgUnit(ou['id'], ou['code'] if 'code' in ou else '',
                                                   Utils.clean(ou['name']),
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

    def prep_groups(self, users):
        temp_groups = {
            'PwExbEvrKCf': [],
            'Bcd2iHJzUu6': [],
            'I86aqEHvItw': [],
            'wkclTBPaDVi': [],
            'rjiHhv8FmyW': [],
            'bavmjFhqqqg': [],
            'mltSBvelpZD': [],
            'B0HpU9W6DBK': [],
            'KGS7WccBeDD': [],
            'pYzHMznQuiH': [],
            'eAWbodAQTsZ': [],
            'tXSEDKV365m': [],
            'rQoa96M8G4x': [],
            'HgvQMs6OLY8': [],
            'AZM2Mg5ntKF': [],
        }

        group = {
            'Addis Ababa Regional Health Bureau': {'groupId': 'PwExbEvrKCf', 'groupName': 'PHEM Addis Ababa'},
            'Afar Regional Health Bureau': {'groupId': 'Bcd2iHJzUu6', 'groupName': 'PHEM Afar'},
            'Amhara Regional Health Bureau': {'groupId': 'I86aqEHvItw', 'groupName': 'PHEM Amhara'},
            'Beneshangul Gumuz Regional Health Bureau': {'groupId': 'wkclTBPaDVi', 'groupName': 'PHEM Beneshangul Gumuz'},
            'Dire Dawa Regional Health Bureau': {'groupId': 'rjiHhv8FmyW', 'groupName': 'PHEM Dire Dawa'},
            'Gambella Regional Health Bureau': {'groupId': 'bavmjFhqqqg', 'groupName': 'PHEM Gambella'},
            'Harari Regional Health Bureau': {'groupId': 'mltSBvelpZD', 'groupName': 'PHEM Harari'},
            'Oromiya Regional Health Bureau': {'groupId': 'B0HpU9W6DBK', 'groupName': 'PHEM Oromiya'},
            'Sidama Regional Health Bureau': {'groupId': 'KGS7WccBeDD', 'groupName': 'PHEM Sidama'},
            'SNNP Regional Health Bureau': {'groupId': 'pYzHMznQuiH', 'groupName': 'PHEM SNNP'},
            'Somali Regional Health Bureau': {'groupId': 'eAWbodAQTsZ', 'groupName': 'PHEM Somali'},
            'South Western Ethiopia RHB': {'groupId': 'tXSEDKV365m', 'groupName': 'PHEM South Western'},
            'Tigray Regional Health Bureau': {'groupId': 'rQoa96M8G4x', 'groupName': 'PHEM Tigray'},
            'Ethiopian Public Health Institute': {'groupId': 'AZM2Mg5ntKF', 'groupName': 'PHEM National'},
            'Users': {'groupId': 'HgvQMs6OLY8', 'groupName': 'PHEM users'}
        }

        for user in users:
            hierarchy = Utils.generate_org_units_hierarchy(self.org_units, user.organisationUnits[0]['id'])
            if hierarchy[1] in group.keys():
                temp_groups[group[hierarchy[1]]['groupId']].append({'id': user.id})
            # all users should belong to PHEM users
            temp_groups['HgvQMs6OLY8'].append({'id': user.id})

        user_groups = []
        for key, g in group.items():
            user_groups.append({
                'name': g['groupName'],
                'id': g['groupId'],
                'users': temp_groups[g['groupId']]
            })
        return user_groups

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

    def generate_group(self, users):
        return self.prep_groups(users)

    def generate(self):
        print("Please wait ... ", end="")

        data = {'system': System()}

        filename = ""
        if self.generate_type == "user":
            data['users'] = self.generate_users()
            data['userGroups'] = self.generate_group(data['users'])
            filename = self.users_json_file_name
        else:
            print('Invalid parameter!')
            exit()

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
        # print('app.py -g group')
        # print('app.py --generate group')


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
