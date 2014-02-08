from textlink.models import List, Entry, Phone

def basic_data(session):
    lst1 = List('TestList1')
    lst2 = List('TestList2')

    phone1 = Phone("TestRunner", "0987654321")
    phone2 = Phone("RunnerOfTest", "1234567890")

    session.add(lst1)
    session.add(lst2)
    session.add(phone1)
    session.add(phone2)

    session.commit()

    e11 = Entry(lst1.list_id, phone1.phone_id)
    e21 = Entry(lst1.list_id, phone2.phone_id)
    e12 = Entry(lst2.list_id, phone1.phone_id)

    session.add(e11)
    session.add(e21)
    session.add(e12)
