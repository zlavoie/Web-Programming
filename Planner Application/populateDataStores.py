import pickledb

if __name__ == '__main__':
    db = pickledb.load('users.db',False)
    db.set('bob','csrocks55')
    db.set('ralph','csrocks55')
    db.set('shai','csrocks55')
    db.dump()

    db = pickledb.load('survey.db',False)
    db.set('1111',['The Talisman','Stephen King','0'])
    db.set('2222',['The Stand','Stephen King','0'])
    db.set('3333',['The Shining','Stephen King','0'])
    db.set('4444',['The Dark Tower','Stephen King','0'])
    db.dump()

