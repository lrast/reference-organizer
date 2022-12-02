# functions for working with CSV database

def fetchEntry(fileID):
    ''' fetches files from the table'''
    with open( 'webapp/database/table.csv') as f:
        if fileID is None:
            # return all files 
            entries = f.readlines()[1:]
            outs = {}
            for entry in entries:
                values = entry.split(', ')
                outs[ values[0] ] = values[1:3]

            return outs

        for entry in f.readlines()[1:]:
            values = entry.split(', ')
            print(entry, values[0])
            if fileID == values[0]:
                return values[3].strip(), values[4].strip()


import uuid

def addEntry(name, date, path):
    ''' adds entry to the file'''
    toAdd = str( uuid.uuid1() ) + ', '
    toAdd += name + ', '
    toAdd += date + ', '

    lastSlash = path.rfind('/')
    toAdd += path[7:lastSlash] + ', '
    toAdd += path[lastSlash+1:] + '\n'

    with open( 'webapp/database/table.csv', 'a') as f:
        f.write(toAdd)