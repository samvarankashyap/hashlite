# testscript
import hashlite
tdb = hashlite("/tmp/tdb.json")
tdb.set("hello",[])
tdb.set("hai",{})
tdb.set("some",[1,2, "apples", "otherthings"])
print tdb.get("some")
tdb.emptydb()
print tdb.get()
print tdb.get("some")
tdb.set("testlcreate_dict", {})
print tdb.lcreate("testlcreate_dict","lcreate_sub_key")
print tdb.listreset("testlcreate_dict","lcreate_sub_key")
print("lcreate_list")
print tdb.get()
print tdb.listpop("testlcreate_dict", "lcreate_sub_key" )
print tdb.listpop("tcreate")
print tdb.get()
print tdb.listpush("hai", "testkeyshouldnotenter")
print tdb.listpush("some", "testkeyshouldenter")
print tdb.listpop("some")
print tdb.get()
tdb.listcreate("hai", "newlist")
print tdb.get()
print tdb.listpush("hai", "someval", "newlist")
print tdb.get()