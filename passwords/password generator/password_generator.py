import random

uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
special = "!@#$%^&*()-+"

all_characters = uppercase + lowercase + numbers + special

length = int(input("Enter the desired password length (minimum 8 characters): "))

password = []

password.append(random.choice(uppercase))
password.append(random.choice(lowercase))
password.append(random.choice(numbers))
password.append(random.choice(special))



remaining_length = length - 4

for _ in range(remaining_length):
    password.append(random.choice(all_characters))

    random.shuffle(password)

print("Generated password:", ''.join(password))



