def engine_privacylist(privacylist_rule):
    from adblockparser import AdblockRules
    f1 = open(privacylist_rule,"r",encoding="utf8")
    easyprivacyrule = f1.readlines()
    easyprivacy = AdblockRules(easyprivacyrule)
    return easyprivacy

def engine_easylist(easylist_rule):
    from adblockparser import AdblockRules
    f2 = open(easylist_rule,"r",encoding="utf8")
    easylistrule = f2.readlines()
    easylist = AdblockRules(easylistrule)
    return easylist

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list