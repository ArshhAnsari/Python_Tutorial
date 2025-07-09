def myFunc():
    print("Hello World")


if __name__ == "__main__":
    # This will only be executed if the script runs directly itself (as opposed to being imported into another module) 
    myFunc()
    print(__name__)