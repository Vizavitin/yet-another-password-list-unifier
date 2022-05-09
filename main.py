# YAPLU - Yet Another Password List Unifier v 0.1a (09.05.2022) by Oleg Vizavitin
# This script helps to unify csv password databases from Apple KeyChain and iPassword

class Authenticator:
    def __init__(self, title: str, url: str, login: str, password: str):
        self.title = title
        self.url = url
        self.login = login
        self.password = password

    def __str__(self):
        return f"{self.title} | {self.url} | {self.login} | {self.password}"

    def __hash__(self):
        return hash((self.title, self.url, self.login, self.password))

    def __eq__(self, other):
        return self.title == other.title and self.url == other.url and self.login == other.login \
                and self.password == other.password

    def __gt__(self, other):
        return self.title > other.title

    def __lt__(self, other):
        return self.title < other.title


# Return a new set with elements common to the set and all others.
def common_elements(list1, list2):
    return list(set(list1) & set(list2))


# Return a new set with elements in the set that are not in the others.
def difference(list1, list2):
    return list(set(list1) - set(list2))


# Return a new set with elements in either the set or other but not both.
def symmetric_difference(list1, list2):
    return list(set(list1) ^ set(list2))


# Unify two lists into one (elements from both lists appear only once).
def unify(list1, list2):
    return common_elements(list1, list2) + difference(list1, list2) + difference(list2, list1)


def user_input():
    while True:
        path = input("Please write the csv file name\n")
        if path != "":
            try:
                filecontent = open(path, "r")
                break
            except (OSError, IOError) as e:
                print("No such file or directory! Please try again!")
        else:
            print("The file name was not set!")
            continue
    return path


def main():
    print("Welcome to YAPLU!")
    print("At first, we need to import Apple Keychain")
    apple_path = user_input()
    print("Secondly, we need to import 1Password database")
    p1ass_path = user_input()
    auth_apple = []
    auth_1p = []
    # Processing the first file
    with open(apple_path) as file_1:
        for line in file_1:
            line = line.replace("\n", "")
            parts = line.split(",")
            if parts[0] != "Title":
                auth_apple.append(Authenticator(parts[0], parts[1], parts[2], parts[3]))

    # Processing the second file
    with open(p1ass_path) as file_2:
        for line in file_2:
            line = line.replace("\n", "")
            parts = line.split(",")
            if "Welcome to 1Password!" not in parts[3]:
                auth_1p.append(Authenticator(parts[3][1:-1], parts[5][1:-1], parts[6][1:-1], parts[2][1:-1]))

    output = unify(auth_apple, auth_1p)
    output.sort()

    # Processing the result
    with open("result.csv", "w") as my_file:
        my_file.write("Title, Website, Username, Password\n")
        for i in range(len(output)):
            line = f"{output[i].title},{output[i].url},{output[i].login},{output[i].password}"
            my_file.write(line + "\n")
    print("Processed successfully! Enjoy!")


if __name__ == '__main__':
    main()
