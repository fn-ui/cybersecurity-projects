def say_hello():
    print("Hello, welcome to the Cyber Security Toolkit")

say_hello()

def analyze_password():
    print("Welcome to password strength analyzer")
    password = input("Enter your password: ")
    common_passwords = [
        "password",
        "password123",
        "12345678",
        "123456789",
        "qwerty",
        "qwerty123",
        "admin",
        "admin123",
        "welcome",
        "letmein"
    ]
    print("You entered", password)

    if len(password) >= 8:
        print("Password length is good.")
    else:
            print("Password is too short. It should be at least 8 characters long.")


    has_uppercase = False
    has_lowercase = False
    has_number = False
    has_special = False

    for char in password:
        if char.isupper():
            has_uppercase = True
        if char.islower():
            has_lowercase = True
        if char.isdigit():
            has_number = True
        if not char.isalnum():
            has_special = True

    if has_uppercase:
        print("Password contains uppercase letters.")
    else:
        print("Password should contain at least one uppercase letter.")

    if has_lowercase:
        print("Password contains lowercase letters.")
    else:
        print("Password should contain at least one lowercase letter.")

    if has_number:
        print("Password contains numbers.")
    else:
        print("Password should contain at least one number.")

    if has_special:
        print("Password contains special characters.")
    else:
        print("Password should contain at least one special character.")

    #check password score
    score = 0

    if len(password) >= 8:
        score += 1
    if has_uppercase:
        score += 1
    if has_lowercase:
        score += 1
    if has_number:
        score += 1
    if has_special:
        score += 1


    is_common = False
    if password.lower() in common_passwords:
        is_common = True
        print("⚠️ Your password is a common password. Consider changing it to something more secure.")
    if is_common:
        score -= 2
    if score < 0:
        score = 0

    needs_improvement = (
        len(password) < 8
        or not has_uppercase
        or not has_lowercase
        or not has_number
        or not has_special
        or is_common
    )
    if needs_improvement:
        print("\nsuggestions to improve your password:")

    if len(password) < 8:
        print("- Increase the length of your password to at least 8 characters.")
    if not has_uppercase:
            print("- Add at least one uppercase letter.")
    if not has_lowercase:
            print("- Add at least one lowercase letter.")
    if not has_number:
            print("- Add at least one number.")
    if not has_special:
            print("- Add at least one special character.")
    if is_common:
                print("- Avoid using common passwords. Consider using a unique combination of letters, numbers, and special characters.")

    print("\nPassword strength score:", score , "/ 5")

    #Determine password strength based on score
    if score == 5:
        print("Password strength: Very Strong")
    elif score == 4:
        print("Password strength: Strong")
    elif score == 3:
        print("Password strength: Medium")
    elif score == 2:
        print("Password strength: Weak")
    else:
        print("Password strength: Very Weak")



def generate_password():
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





print("\n===Cyber Security Toolkit===\n")
print("1. Analyze Password Strength")
print("2. Generate a Secure Password")
print("3. Exit")

choice = input("Choose an option: ")

if choice == "1":
    analyze_password()
elif choice == "2":
    generate_password()
elif choice == "3":
    print("Exiting the toolkit.")
