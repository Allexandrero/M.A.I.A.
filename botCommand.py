def dbStatement(database, emojiname):
    cursor = database.cursor()
    cursor.execute(f"SELECT code FROM emojicodes WHERE emoji = '{emojiname}'")
    mystring = ''.join(map(str, iter(cursor.fetchall())))
    return mystring


def removeBracketsFrom(inputstat):
    return inputstat.replace("('", "").replace("',)", "")
