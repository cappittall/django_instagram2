import uuid
my_dict = {'a':234,'b':'asff'}
my_dict.update({'ref_code':str(uuid.uuid4().hex)[0:4].lower()})
print(my_dict)