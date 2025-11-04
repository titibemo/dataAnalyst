def stuck_user():
    while True:
        user_input_login = input("écrivez en login: 'login':")
        user_input_password = input("écrivez en password: 'passsword':")
        if user_input_login == "login" and user_input_password == "password":
            exit()
        else:
            print("===== Erreur ! recommencez les saisis ! =====")
print("===== Vous êtes bien connecté =====")

if __name__ == "__main__":
    stuck_user()