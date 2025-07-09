def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            # default
            return "Something's wrong with the internet"
        
print(http_status(200))
# print(http_status(404))
# print(http_status(500))