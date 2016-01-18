
def check_file_type(file_name, list_file):
    for name_part in list_file:
        if name_part in file_name:
            return True
    return False


def is_file_out(file_name):
    list_file_out = ['.out', '.ans', '.a', 'output']
    return check_file_type(file_name, list_file_out)


def is_file_in(file_name):
    return not is_file_out(file_name) and not is_other_file(file_name)


def is_other_file(file_name):
    list_other_file = ['.c', '.cpp', '.pas', '.java', '.py', '.exe', 'file.inp']
    return check_file_type(file_name, list_other_file)
