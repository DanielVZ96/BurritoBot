import sqlite3

def get_response(db_location, command):
    """
    :param db_location: location of database.
    :param command: command for which we want a response
    :return: False if command doesn't exist, response if it does exists
    """
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    exists = cursor.execute("SELECT EXISTS(SELECT 1 FROM burritobot_command WHERE command==?)", (command,))
    exists = exists.fetchone()[0]
    if exists:
        response = cursor.execute("SELECT response FROM burritobot_command WHERE command==?", (command,))
        return response.fetchall()[0][0]
    else:
        return False


def get_commands(db_location):
    """
    :param db_location: location of database.
    :return: returns list containing commands.
    """
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    commands = cursor.execute("SELECT command,response FROM burritobot_command")
    return [pair[0] for pair in commands.fetchall()]


def new_command(db_location, command, new_response):
    """
    :param db_location: location of database.
    :param command: command to be added.
    :param new_response: respective response
    :return: True if success, False if failure
    """
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    exists = cursor.execute("SELECT EXISTS(SELECT 1 FROM burritobot_command WHERE command==?)", (command,)).fetchone()[0]
    print(exists)
    if not exists:
        cursor.execute("INSERT INTO burritobot_command (command, response) VALUES (?,?)", (command, new_response))
        connection.commit()
        return True
    else:
        return False

def delete_command(db_location, command):
    """
    :param db_location: location of database.
    :param command: command to be deleted.
    :return: True if success, False if failure
    """
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    exists = cursor.execute("SELECT EXISTS(SELECT 1 FROM burritobot_command WHERE command==?)", (command,)).fetchone()[0]
    if exists:
        cursor.execute("DELETE FROM burritobot_command WHERE command=?", (command,))
        connection.commit()
        return True
    return False

#TODO adapt code to be able to use different user's access tokens
def get_access_token(db_location):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    token = cursor.execute("SELECT (access_token) FROM burritobot_authinfo LIMIT 1").fetchone()[0]
    return token



if __name__ == '__main__':
    new_command('test.sqlite3', '!T1', 'IT WORKS!')
    response = get_response('test.sqlite3', '!T1')
    commands = get_commands('test.sqlite3')
    delete_command('test.sqlite3', '!T1')
    commands = get_commands('test.sqlite3')
    token = get_access_token('../../../db.sqlite3')
    print(token)
