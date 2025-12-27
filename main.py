import app.core.auth as auth

def main():
    #user = auth.register_user("tanay@gmail.com", "def456", "def456", "tanay", "ranjan")
    
    inp_email = str(input("Enter email : "))
    inp_pass = str(input("Enter password : "))

    if(auth.authenticate_user(inp_email, inp_pass)):
        print("Logged in!")
    else:
        print("Not Logged in...")

if __name__ == "__main__":
    main()