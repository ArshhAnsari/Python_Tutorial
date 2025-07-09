def main():
    try:
        a=int(input("Enter a number: "))
        print("You have entered {}".format(a))
        return
    
    except Exception as e:
        print(e)
        return

    # finally:
        print("Using finally block") # This block is always executed regardless of whether an exception occurred or not

main()
