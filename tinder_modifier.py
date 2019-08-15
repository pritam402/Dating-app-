import mysql.connector
class Tinder:
    def __init__(self):
        self.conn=mysql.connector.connect(host='localhost',user='root',password='',database='tinder')
        self.mycursor=self.conn.cursor()
        print('connected')
        self.program_menu()
    def program_menu(self):
        program_input=input('''hi what would u like to do??
        1. Register
        2. Login
        3. Exit''')
        if program_input=='1':
            self.register()
        elif program_input=='2':
            self.login()
        else:
            print('bbye')
    def register(self):

        email=input('enter your email : ')
        check = self.email_check(email)
        if check:
            print('email already present')
            self.program_menu()
        password=input('password : ')
        name = input('enter your name : ')
        gender=input('what is your gender')
        age=input('whats your age? ')
        city=input('in which city do you reside : ')


        self.mycursor.execute('''INSERT INTO `users` (`user_id`,`name`,`email`,`password`,`gender`,`age`,`city`) VALUES       
        (NULL,'{}','{}','{}','{}','{}','{}')'''.format(name, email, password, gender, age, city))
        self.conn.commit()
        print('reg sucesful')
        self.program_menu()
    def email_check(self,email):
        self.mycursor.execute("""SELECT `user_id` FROM `users` WHERE `email` LIKE '{}'""".format(email))
        flag=self.mycursor.fetchall()
        if flag[0][0]>0:
            return True
        else:
            return False



    def login(self):
        email=input('enter email')
        password=input('enter password')
        self.mycursor.execute('''SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' '''.format(email,password))
        user_list=self.mycursor.fetchall()
        #it will retrieve the data from a succesful call
        counter=0
        for i in user_list:
            counter+=1
            current_user=i
        if counter>0:
            print('welcome')
            self.current_user_id=current_user[0]
            self.user_menu()

        else:
            print('incorrect credentials')
    def user_menu(self):
        user_input=input('''how wuold you like to proceed 
        1. view all users
        2. view your proposals
        3.view your requst
        4.view maches
        5.logout''')
        if user_input=='1':
            self.view_users()
        elif user_input=='2':
            self.view_proposals()
        elif user_input=='3':
            self.view_requests()
        elif user_input=='4':
            self.view_matches()
        elif user_input=='5':
            self.logout()
        else:
            print("incorrect entry")
            self.user_menu()
    def view_users(self):

        self.mycursor.execute('''SELECT * FROM `users` WHERE `user_id` NOT LIKE '{}' '''.format(self.current_user_id))
        all_users=self.mycursor.fetchall()
        for i in all_users:
            print(i[0],'|',i[1],'|',i[4],'|',i[5],'|',i[6])
            print('----------------------------------------')
        juliet_id=input('enter the id of the user id u want to propose')
        self.propose(juliet_id=juliet_id,romeo_id=self.current_user_id)
        #self.user_menu()
    def propose(self,juliet_id,romeo_id):
        self.mycursor.execute("""SELECT `proposal_id` FROM `proposals` WHERE `juliet_id`='{}' AND 
        `romeo_id`='{}'""".format(juliet_id,romeo_id))
        check=self.mycursor.fetchall()
        if check[0][0]>0:
            print('already proposed')
            self.user_menu()
        self.mycursor.execute("""INSERT INTO `proposals` (`proposal_id`,`romeo_id`,`juliet_id`)
         VALUES (NULL,'{}','{}')""".format(romeo_id,juliet_id))
        self.conn.commit()
        print('proposals sent succesfully. Fingers Crossed')
        self.user_menu()
    def view_proposals(self):
        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN
        `users` u ON u.`user_id`=p.`juliet_id` WHERE p.`romeo_id` LIKE '{}'""".format(self.current_user_id))
        self.proposed_user_list=self.mycursor.fetchall()
        for i in self.proposed_user_list:
            print(i[4],'|',i[7],'|',i[8],'|',i[9])
            print('------------------------------')
        self.user_menu()
    def view_requests(self):
        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN
                `users` u ON u.`user_id`=p.`romeo_id` WHERE p.`juliet_id` LIKE '{}'""".format(self.current_user_id))
        self.request_user_list = self.mycursor.fetchall()
        for i in self.request_user_list:
            print(i[4], '|', i[7], '|', i[8], '|', i[9])
            print('------------------------------')
        choice=input('''1. propose
        2. back to the menu''')
        if choice=='1':
            juliet_id = input('enter id for the request')
            self.propose(juliet_id=juliet_id, romeo_id=self.current_user_id)
        else:
            self.user_menu()


        self.user_menu()
    def view_matches(self):
        self.mycursor.execute("""SELECT * from `proposals` p join `users` u ON u.`user_id`=p.`juliet_id` where `juliet_id` in 
        (SELECT `romeo_id` FROM `proposals` WHERE `juliet_id` LIKE '{}') 
        and `romeo_id` LIKE '{}'""".format(self.current_user_id,self.current_user_id))
        matched_user_list=self.mycursor.fetchall()
        for i in matched_user_list:
            print(i[4], '|', i[7], '|', i[8], '|', i[9])
            print('------------------------------')
        self.user_menu()
    def logout(self):
        self.current_user_id=0


user=Tinder()

