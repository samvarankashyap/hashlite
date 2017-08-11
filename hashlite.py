import os
import json

def wrap(pre, post):
    def decorate(func):
        def call(*args, **kwargs):
            pre(func, *args, **kwargs)
            result = func(*args, **kwargs)
            post(func, *args, **kwargs)
            return result
        return call
    return decorate

def savedb(func, *args, **kwargs):
    db_obj = args[0]
    path = db_obj.path
    fd = open(db_obj.path, "w")
    fd.write(json.dumps(db_obj.db, sort_keys=True, indent=4))
    fd.close()

def loaddb(func, *args, **kwargs):
    fd = open(args[0].path, "r").read()
    args[0].db = json.loads(fd)


class hashlite:
    def __init__(self, path, reset=False):
        self.path = path
        if os.path.exists(path):
           f = open(path, "r").read() 
           self.db = json.loads(f)
        elif reset or not os.path.exists(path):
            self.db = {}
            with open(self.path, 'w') as dbfile:
                dbfile.write(json.dumps(self.db))

    @wrap(loaddb, savedb)
    def set(self, key, value, subkey=None, force=False):
        try:
            if subkey and self.db.get(key, False):
                if type(self.db.get(key, None)) is list:
                    self.db[key][subkey] = value
                    return True
                if type(self.db.get(key, None)) is dict:
                    r = self.db[key].setdefault(subkey, value )
                    if r == value:
                        return True
                    elif force == True:
                        self.db[key] = value
                        return True
        except Exception as e:
            return False
        if not subkey:
            r = self.db.setdefault(key, value)
            if r == value:
                return True
            elif force == True:
                self.db[key] = value
                return True
        return False 
      
    @wrap(loaddb, savedb)
    def get(self, key=None, subkey=None):
        """
        subkey can be positional key or alphabetical
        """
        if subkey:
            if type(self.db.get(key, None)) is list:
                if subkey < len(self.db.get(key)):
                    return self.db.get(key)[subkey] 
                else: 
                    return None
            if type(self.db.get(key, None)) is dict:
                return self.db.get(key).get(subkey, None)
        if not key and not subkey:
            return self.db
        return self.db.get(key, None)
        
        
    @wrap(loaddb, savedb)
    def listcreate(self, key, subkey=None, force=False):
        if subkey and self.db.get(key, None) != None:
            if force:
                # when you want that key to reset 
                self.db[key][subkey] = []
            else:
                # when db[key] is a list we dont perform
                if type(self.db[key]) is list:
                    print("Operation cant be performed")
                # when its a dict use setdefault and confirm it happened or not
                if type(self.db[key]) is dict:
                    r = self.db[key].setdefault(subkey, [])
                    if r == []:
                        return True
                    else:
                        return False
                
        else:
            if force:
                self.db[key] = []
            else:
                r = self.db.setdefault(key, [])
                if r == []:
                    return True
                else:
                    return False

    @wrap(loaddb, savedb)
    def listpop(self, key, subkey=None):
        if subkey != None and self.db.get(key, False): 
            if type(self.db[key]) is list:
                # operation not permitted
                return False
            if type(self.db[key]) is dict and subkey in self.db[key].keys():
                try:
                    return self.db[key][subkey].pop()
                except IndexError as e:
                    # coz of empty list cant be popped
                    return False
            else:
                # need to return proper messages
                return False
        else:
            try:
                if type(self.db.get(key, None)) is list:
                    return self.db[key].pop()
                else:
                    # coz operation not permitted
                    return False
            except IndexError as e:
                return False 
        return False

    @wrap(loaddb, savedb)
    def listpush(self, key, value, subkey=None):
        if subkey != None and type(self.db.get(key, False)) is dict:
            if subkey in self.db[key] and \
               type(self.db[key].get(subkey, False)) is list:
                self.db[key][subkey].append(value)
            else:
                # need to return proper messages
                return False
        else:
            if type(self.db.get(key, None)) is list:
                return self.db[key].append(value)
            else:
                # coz operation not permitted
                return False
        return False

    @wrap(loaddb, savedb)
    def delete(self, key, subkey=None):
        if subkey != None and self.db.get(key, None):
            if type(self.db[key]) is dict:
                return self.db[key].pop(key, False)
            elif type(self.db[key]) is list: 
                return self.db[key].pop(key, False)
            else:
                return False
        else:
            return self.db.pop(key, False)
  
    @wrap(loaddb, savedb)
    def listreset(self, key, subkey=None):
        return self.lcreate(key, subkey, force=True)

    @wrap(loaddb, savedb)
    def emptydb(self):
        self.db = {}
        return True

# testscript
#tdb = hashlite("/tmp/tdb.json")
#tdb.set("hello",[])
#tdb.set("hai",{})
#tdb.set("some",[1,2, "apples", "otherthings"])
#print tdb.get("some")
#tdb.emptydb()
#print tdb.get()
#print tdb.get("some")
#tdb.set("testlcreate_dict", {})
#print tdb.lcreate("testlcreate_dict","lcreate_sub_key")
#print tdb.listreset("testlcreate_dict","lcreate_sub_key")
#print("lcreate_list")
#print tdb.get()
#print tdb.listpop("testlcreate_dict", "lcreate_sub_key" )
#print tdb.listpop("tcreate")
#print tdb.get()
#print tdb.listpush("hai", "testkeyshouldnotenter")
#print tdb.listpush("some", "testkeyshouldenter")
#print tdb.listpop("some")
#print tdb.get()
#tdb.listcreate("hai", "newlist")
#print tdb.get()
#print tdb.listpush("hai", "someval", "newlist")
#print tdb.get()
