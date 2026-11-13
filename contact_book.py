#Contact book
import json
import re
File_name = "contacts.json"

def load_contacts():
    try:
        with open(File_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Contacts file is corrupted. Starting with an empty book.")
        return {}
    
def save_contacts():
    with open(File_name, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact(name,phone,email):
    contacts[name]={"phone": phone,"email": email}
    save_contacts()

def search_contact(name):
    if name in contacts:
        print(name," : ", contacts[name]["phone"]," ", contacts[name]["email"])
    else:
        print("No Such contact exists!!")

def del_contact(name):
    if name in contacts:
        x=input("Are you sure? (y/n):")
        if x.lower()=='y':
            contacts.pop(name)
            save_contacts()
            print("contact deleted successfully!!")
    else:
        print("No Such contact exists!!")

def listall_contacts():
    ct=0
    for x, y in sorted(contacts.items()):
        print(x ," : ", y["phone"]," ", y["email"])
        ct+=1
    print("total contacts: ",ct)

def validate_phone(phone):
    return re.fullmatch(r"[6-9]\d{9}", phone) is not None

def validate_email(email):
    return re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email) is not None

def ask_phone_email():
    while True:
        phone = input("Enter phone no.: ")
        if validate_phone(phone):
            break
        print("Invalid phone no.")
    while True:
        email = input("Enter email: ")
        if validate_email(email):
            break
        print("Invalid email!")
    return phone, email

contacts=load_contacts()

while True:
    print("1.add contact\n2.search contact\n3.delete contact\n4.update contact\n5.list all contacts\n6.exit")
    try:
        ch=int(input("enter your choice:"))
    except ValueError:
        print("Please enter a number!!")
        continue
    match ch:
        case 1 :
            name=input("enter name: ").strip().lower()
            if name in contacts:
                print("Contact already exists!!")
                continue
            phone,email=ask_phone_email()
            add_contact(name,phone,email)
            print("contact added successfullly!!")
        case 2:
            name=input("enter name to search: ").strip().lower()
            search_contact(name)
        case 3:
            name=input("enter name to delete: ").strip().lower()
            del_contact(name)
        case 4:
            name=input("enter name to update: ").strip().lower()
            if name not in contacts:
                print("No Such contact exists!!")
                continue
            phone,email=ask_phone_email()
            add_contact(name,phone,email)
            print("contact updated successfullly!!")
        case 5:
            listall_contacts()
        case 6:
            print("Exitting!!")
            break
        case _:
            print("Invalid choice! Try again.")




