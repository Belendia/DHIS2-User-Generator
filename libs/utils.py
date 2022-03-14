import random
import string


class Utils:

    @staticmethod
    def generate_uid(code_size=11):
        letters = "{}{}".format(string.ascii_lowercase, string.ascii_uppercase)
        allowed_chars = "{}{}".format(string.digits, letters)

        # First char should be a letter
        random_chars = [letters[
                            random.randrange(letters.__len__() - 1)]]

        for i in range(1, code_size):
            random_chars.append(allowed_chars[
                                    random.randrange(allowed_chars.__len__())])
        return ''.join(random_chars)

    @staticmethod
    def generate_username(name, length=8):
        return name.lower().strip().replace(' ', '')[:length]

    @staticmethod
    def generate_unique_username(name):
        return "{}{}".format(name, random.randrange(100, 999))

    @staticmethod
    def generate_password(length=10):
        upper = "ABCDEFGHJKLMNPQRSTUVWXYZ"
        lower = "abcdefghijkmnopqrstuvwxyz"
        digits = "346789"
        punctuation = "#$&*@"
        allowed_chars = "{}{}{}{}".format(digits, punctuation, lower, upper)
        # make sure one lower case, upper case, digit and punctuation characters are selected
        temp_password = random.sample(lower, 1) + random.sample(upper, 1) + random.sample(punctuation, 1) + random.sample(digits, 1) + random.sample(allowed_chars, length - 4)
        return "".join(temp_password)

    @staticmethod
    def is_health_facility(org_unit):
        if 'hospital' in org_unit.name.lower():
            return True
        if 'health center' in org_unit.name.lower():
            return True
        if 'health post' in org_unit.name.lower():
            return True
        if 'clinic' in org_unit.name.lower():
            return True
        if ' phcu' == org_unit.name.lower()[-5:]:
            return False
        if ' regional health bureau' == org_unit.name.lower()[-23:]:
            return False
        if ' worho' == org_unit.name.lower()[-6:]:
            return False
        if ' zhd' == org_unit.name.lower()[-4:]:
            return False

        if org_unit.level == '4' or org_unit.level == '5' or org_unit.level == '6':
            return True
        return False

    @staticmethod
    def generate_org_units_hierarchy(org_units, org_unit, hf_hierarchy_len=7):

        ou_hierarchy = []
        ou = org_units[org_unit]
        while ou is not None:
            ou_hierarchy.append(ou.name)
            ou = None if ou.parent is None else org_units[ou.parent]
        ou_hierarchy.reverse()
        if ou_hierarchy.__len__() < hf_hierarchy_len:
            for i in range(hf_hierarchy_len - ou_hierarchy.__len__()):
                ou_hierarchy.append('')
        return ou_hierarchy

    @staticmethod
    def clean(text):
        # remove punctuation from org units name
        return text.translate({ord(c): None for c in string.punctuation})
