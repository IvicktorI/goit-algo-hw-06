from collections import UserList

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value : str):
           super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if self.is_valid_number(value):
            super().__init__(value)
        else:
            raise ValueError("Incorrect phone number")
    @staticmethod
    def is_valid_number(number: str):
        return str(number).isdigit() and len(str(number)) == 10

class Record:
    def __init__(self, name: str,phone=None):
        self.name = Name(name)
        if phone==None:
            self.phones = []
        else:
            _phone=Phone(phone)
            self.phones = [_phone]
    
    def add_phone(self,phone: Phone):
        flag=1
        for ph in self.phones:
            if ph.value==phone.value:
                flag=0
                break
        if flag:
            self.phones.append(phone)
        
    def remove_phone(self, phone: Phone):
        for ph in self.phones:
            if ph.value==phone.value:
                self.phones.remove(ph)
                break
    
    def edit_phone(self,old_phone: Phone,new_phone: Phone):
        for ph in self.phones:
            if ph.value==old_phone.value:
                ph.value = new_phone.value
                return 1
        return 0
        
    def find_phone(self, phone: Phone) ->Phone:
        for ph in self.phones:
            if ph.value==phone.value:
                return ph
            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
class AddressBook(UserList):
    def add_record(self, record: Record):
        flag=1
        for contact in self.data:
            if contact.name==record.name:
                flag=0
                break
        if flag:
            self.data.append(record)

    def find(self,name) ->Record:
        if isinstance(name, str):
            for contact in self.data:
                if contact.name.value==name:
                    return contact
        if isinstance(name, Name):
            for contact in self.data:
                if contact.name.value==name.value:
                    return contact

    def delete(self,name):
        if isinstance(name, str):
            for contact in self.data:
                if contact.name.value==name:
                    self.data.remove(contact)
        if isinstance(name, Name):
            for contact in self.data:
                if contact.name.value==name.value:
                    self.data.remove(contact)
    
    def edit_record(self,name,old_phone,new_phone) -> str:
        for contact in self.data:
            if contact.name.value==name:
                contact.edit_phone(Phone(old_phone),Phone(new_phone)) 
                return 'Record change'
        return 'Record not found'  
                
    def show_all(self):
        for contact in self.data:
            print(contact)

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'{e}'
        except KeyError:
            return 'No such name found'
        except IndexError:
            return 'Not found'
        except Exception as e:
            return f'Error: {e}'

    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_record(args, contacts: AddressBook):
    name, phone = args
    temp_rec=Record(name,phone)
    contacts.add_record(temp_rec)
    return "Record added."

@input_error
def edit_phone(args, contacts):
    if len(args)==3:
        name, old_phone, new_phone = args
    else :
        raise ValueError ('Insufficient parameters')
    for el in contacts:
        if el.name.value==name:
            if el.edit_phone(Phone(old_phone),Phone(new_phone)):
                return "Record change."
    return 'Record not found'

@input_error
def add_phone(args, contacts):
    if len(args)==2:
        name, phone = args
    else :
        raise ValueError ('Insufficient parameters')
    for el in contacts:
        if el.name.value==name:
            el.add_phone(Phone(phone))
            return "Phone add."
    return 'Record not found'

@input_error
def delete_phone(args, contacts):
    if len(args)==2:
        name, phone = args
    else :
        raise ValueError ('Insufficient parameters')
    for el in contacts:
        if el.name.value==name:
            el.remove_phone(Phone(phone))
            return "Phone delete."
    return 'Record not found'

@input_error
def find_record(args, contacts: AddressBook):
    name = args[0]
    rec=contacts.find(name)
    if rec is not None:
        return rec
    else : 
        return 'Record not found'
   
@input_error 
def delete_record(args, contacts: AddressBook):
    name = args[0]
    contacts.delete(name)

@input_error
def show_all(contacts: AddressBook):
    for contact in contacts:
        print(contact)

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case 'hello':
                print('How can I help you?')
            case 'add':
                print(add_record(args,contacts))
            case 'edit':
                print(edit_phone(args,contacts))
            case 'find':
                print(find_record(args,contacts))
            case 'delete':
                print(delete_record(args,contacts))
            case 'add_phone':
                print(add_phone(args, contacts))
            case 'delete_phone':
                print(delete_phone(args, contacts))
            case 'all':
                print(show_all(contacts))
            case 'close':
                print('Good bye!')
                break
            case 'exit':
                print('Good bye!')
                break
            case _:
                print('Invalid command.')


if __name__ == "__main__":
    main()