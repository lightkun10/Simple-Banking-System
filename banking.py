import random


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


bank_ = Bank()

while True:
    logged_in = False
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    input_ = int(input())

    if input_ == 1:
        mii = 400000
        valid_number = ""
        # Generate new number until luhn algo generator make a valid num
        while True:
            account_identifier = random.randrange(0000000000, 9999999999)
            new_number = str(f"{mii}{account_identifier}")
            if luhn_algo(new_number):
                valid_number = new_number
                break

        new_pin = random.randint(1000, 9999)
        new_card = CreditCard(valid_number, new_pin)
        bank_.add_card(new_card)
        print("\nYour card has been created")
        print(f"Your card number: \n{new_number}\nYour card PIN:\n{new_pin}\n")

    elif input_ == 2:
        print("\nEnter your card number:")
        cn = input()
        print("Enter your PIN:")
        p = int(input())

        # Iterate through all cards
        count = 0  # Counting the number of different cards from user input
        for c in bank_.cards:
            if c.number == cn and c.pin == p:
                print("\nYou have successfully logged in!\n")
                logged_in = True

                while logged_in:
                    print("1. Balance")
                    print("2. Log out")
                    print("0. Exit")
                    input_for_login = int(input())

                    if input_for_login == 1:
                        print(f"\nBalance: {c.balance}\n")

                    if input_for_login == 2:
                        logged_in = False
                        print("\nYou have successfully logged out!\n")
                        break
                    if input_for_login == 0:
                        print("\nBye!")
                        exit()
            else:
                count += 1

        if count > 0:
            print("Wrong card number or PIN!")

    elif input_ == 0:
        print("\nBye!")
        exit()
