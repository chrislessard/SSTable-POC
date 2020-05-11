import database as database

BASEPATH = 'segments/'
FILENAME = 'database-1'

def main():
    '''
    Run the database interface.
    '''
    usage_msg = [
        'Commands: ',
        'store {key} {data}',
        'get {key}',
        'load_index',
        'save_index_snapshot {filename}',
        'load_index_snapshot {filename}',
        'help',
        'exit'
    ]

    db = database.Database(FILENAME, BASEPATH)

    print('\n\t'.join(usage_msg))

    while True:
        print('Enter a command below. Type "help" to see a list of commands.')
        cmd = input('$ ').lower().split(' ')

        if cmd[0] == 'store':
            key, val = cmd[1], cmd[2]
            db.db_set(key, val)
        elif cmd[0] == 'get':
            key = cmd[1]
            print(db.db_get(key), '\n')
        elif cmd[0] == 'load_index':
            db.load_index()
        elif cmd[0] == 'save_index_snapshot':
            name = cmd[1]
            db.save_index_snapshot(name)
        elif cmd[0] == 'load_index_snapshot':
            name = cmd[1]
            db.load_index_snapshot(name)
        elif cmd[0] == 'help':
            print('\n\t'.join(usage_msg))
        elif cmd[0] == 'exit':
            break
        else:
            print('Invalid command.')

if __name__ == "__main__":
    main()