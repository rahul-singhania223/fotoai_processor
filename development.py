def printHII():
    print("HII")

def printHello():
    print("Hello")

prcess_dict = {
    "test": printHII,
    "test2": printHello
}

if __name__ == "__main__":
    agent = prcess_dict["test"]
    agent()