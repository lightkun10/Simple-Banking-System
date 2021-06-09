import random
import sqlite3

# Represent the database
conn = sqlite3.connect('card.s3db')

# Cursor object to perform SQL queries
cur = conn.cursor()  # execute() to perform SQL queries


class CreditCard:
    def __init__(self, number="", pin=0, balance=0):
        self.number = number
        self.pin = pin
        self.balance = balance


class Bank:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)


def number_to_arr(card_number):
    nums = [int(x) for x in card_number]
    new_nums = []
    # Drop the last digit
    last_digit = nums[-1]
    del nums[-1]
    for index, n in enumerate(nums):
        # print(f"current num: {n}, index: {index+1}")
        cur_num = n
        # Multiply odd digits by 2
        if (index + 1) % 2 != 0:
            cur_num = cur_num * 2
        # Subtract 9 from numbers over 9
        if cur_num > 9:
            cur_num -= 9
        new_nums.append(cur_num)
    new_nums.append(last_digit)
    return new_nums


def luhn_algo(new_num):
    number_arr = number_to_arr(new_num)
    # Take the sum of all the digits
    sums = 0
    for i in range(0, len(number_arr)):
        sums += number_arr[i]
    # If the received number is divisible by 10
    # with the remainder equal to zero, then this
    # number is valid; otherwise, the card number
    # is not valid.
    if sums % 10 == 0:
        return True
    else:
        return False


def find_checksum(account_identifiers):
    ai = [int(x) for x in account_identifiers]
    sums = 0
    for i in range(0, len(ai)):
        sums += ai[i]
    i = 1
    while True:
        if sums + i % 10 != 0:
            i += 1
        return i


# Generate new number until luhn algo generator make a valid num
def generate_nums():
    mii = 400000
    while True:
        account_identifier = random.randrange(0000000000, 9999999999)
        checksum = ""
        if len(str(account_identifier)) < 10:
            checksum = find_checksum(str(account_identifier))
        new_number = str(f"{mii}{account_identifier}{checksum}")
        if luhn_algo(new_number):
            valid_num = new_number
            return valid_num


def print_loggedin_choices():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


bank_ = Bank()

while True:
    logged_in = False
    print("1. Create an account")
    print("2. Log into account")
    # print("999. Show all cards")  # Only for testing. Delete on production.
    print("0. Exit")

    input_ = int(input())

    # Make new table if "card" table not exist yet
    try:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
    finally:
        conn.commit()

    if input_ == 1:
        valid_number = generate_nums()

        new_pin = random.randint(1000, 9999)
        new_card = CreditCard(valid_number, new_pin)
        cur.execute(f'INSERT INTO card(number, pin) VALUES("{valid_number}", "{str(new_pin)}");')
        conn.commit()
        # bank_.add_card(new_card)
        print("\nYour card has been created")
        print(f"Your card number: \n{valid_number}\nYour card PIN:\n{new_pin}\n")

    elif input_ == 2:
        print("\nEnter your card number:")
        cn = input()
        print("Enter your PIN:")
        p = int(input())

        # Iterate through all cards
        db_cards = cur.execute('SELECT * FROM card').fetchall()
        count = 0  # Counting the number of different cards from user input
        for c in db_cards:
            if c[1] == cn and int(c[2]) == p:
                print("\nYou have successfully logged in!\n")
                logged_in = True

                while logged_in:
                    cur_balance = cur.execute(f'SELECT balance FROM card WHERE number = {cn} AND pin = {p}').fetchone()[0]
                    print_loggedin_choices()
                    input_for_logged_user = int(input())

                    if input_for_logged_user == 1:
                        # print(f"\nBalance: {c[-1]}\n")
                        try:
                            print(f"\nBalance: {cur_balance}\n")
                        except:
                            print("No such user...")

                    elif input_for_logged_user == 2:
                        print("\nEnter income:")
                        add_balance = int(input())
                        try:
                            cur.execute(f'UPDATE card SET balance = {cur_balance + add_balance} WHERE number = {c[1]} AND pin = {p};')
                            conn.commit()
                        except:
                            print("\nAn exception occured. Try again.\n")
                        else:
                            print("\nIncome was added!\n")

                    elif input_for_logged_user == 3:
                        print("\nTransfer\nEnter card number:")
                        target_card = input()

                        # Fetch input number in db
                        fetch_cards = cur.execute(f'SELECT * FROM card WHERE number = {int(target_card)}').fetchall()

                        # user tries to transfer money to the same account
                        if int(cn) == int(target_card):
                            print("You can't transfer money to the same account!\n")

                        # receiver's card number doesn’t pass the Luhn algorithm
                        elif not luhn_algo(target_card):
                            print("Probably you made a mistake in the card number. Please try again!")

                        # If the receiver's card number doesn’t exist
                        elif len(fetch_cards) == 0:
                            print(len(fetch_cards))
                            print("\nSuch a card does not exist.\n")

                        # If there is no error
                        else:
                            print("Enter how much money you want to transfer:")
                            trf_amt = int(input())
                            # print(cur_balance)
                            if cur_balance - trf_amt <= 0:
                                print("Not enough money!\n")

                            else:
                                try:
                                    # Cut the source balance
                                    cur.execute(f'UPDATE card SET balance = {cur_balance - trf_amt} WHERE number = {c[1]} AND pin = {p};')
                                    conn.commit()
                                    # Add the cut amount to the target
                                    target = cur.execute(f'SELECT * FROM card WHERE number = {int(target_card)}').fetchone()
                                    cur.execute(f'UPDATE card SET balance = {target[3] + trf_amt} WHERE number = {target_card};')
                                    conn.commit()
                                    print("Success!")
                                except Exception as e:
                                    print(f"An exception has occured: {e}")

                    elif input_for_logged_user == 4:
                        cur.execute(f'DELETE FROM card WHERE number = {cn} AND pin = {p}')
                        conn.commit()
                        print("\nThe account has been closed!\n")
                        break

                    elif input_for_logged_user == 5:
                        logged_in = False
                        print("\nYou have successfully logged out!\n")
                        break
                    elif input_for_logged_user == 0:
                        print("\nBye!")
                        exit()
            else:
                count += 1

        if count > 0 and logged_in is False:
            print("Wrong card number or PIN!")
    elif input_ == 999:
        print(cur.execute('SELECT * FROM card').fetchall())
    elif input_ == 0:
        print("\nBye!")
        exit()
