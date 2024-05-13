import re
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
contract = w3.eth.contract(address=address_contract, abi=abi)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def login():
    try:
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None



def registration():
    try:
        while True:
            password = input("Введите пароль: ")
            if re.search(r"password|qwerty", password):
                print("Пароль не должен быть простым шаблоном.")
                continue
            if len(password) < 12:
                print("Пароль должен содержать не менее 12 символов.")
                continue
            elif not re.search(r"[A-Z]", password):
                print("Пароль должен содержать хотя бы одну заглавную букву.")
                continue
            elif not re.search(r"[a-z]", password):
                print("Пароль должен содержать хотя бы одну строчную букву.")
                continue
            elif not re.search(r"\d", password):
                print("Пароль должен содержать хотя бы одну цифру.")
                continue
            if not re.search(r"[!@#\$%\^&\*\(\)_\-\+=\{\};:,<\.>]", password):
                print("Пароль должен содержать хотя бы один специальный символ.")
                continue

            account = w3.geth.personal.new_account(password)
            print(f"Ваш аккаунт: {account}")
            break 

    except Exception as e:
        print(f"Ошибка авторизации: {e}")



def create_estate(account):
    try:
        size = int(input("Введите размер недвижимости: "))
        addressEstate = input("Введите адрес недвижимости: ")
        estateType = int(input("Выберите тип недвижимости (0 - House, 1 - Flat, 2 - Loft): "))
        contract.functions.createEstate(size, addressEstate, estateType).transact({'from': account})
        print("Недвижимость успешно создана")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def create_advertisement(account):
    try:
        idEstate = int(input("Введите ID недвижимости для создания объявления: "))
        price = int(input("Введите цену недвижимости в WEI: "))
        contract.functions.createAd(idEstate, price).transact({'from': account})
        print("Объявление успешно создано")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def change_estate_status(account):
    try:
        idEstate = int(input("Введите ID недвижимости для изменения статуса: "))
        isActive = input("Установить статус активности (True/False): ").lower()
        isActive = True if isActive == "true" else False
        contract.functions.updateEstateStatus(idEstate, isActive).transact({'from': account})
        print("Статус недвижимости успешно изменен")
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def change_advertisement_status(account):
    try:
        idAd = int(input("Введите ID объявления для изменения статуса: "))
        adStatus = int(input("Установить статус объявления (0 - Opened, 1 - Closed): "))
        contract.functions.updateAdStatus(idAd, adStatus).transact({'from': account})
        print("Статус объявления успешно изменен")
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def purchase_estate(account):
    try:
        idAd = int(input("Введите ID объявления для покупки недвижимости: "))
        value = int(input("Введите сумму для покупки недвижимости: "))
        tx_hash = contract.functions.buyEstate(idAd).transact({'from': account, 'value': value})
        print(f"Транзакция успешно отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка при покупке недвижимости: {e}")


def withdraw_funds(account):
    try:
        amount = int(input("Введите сумму для вывода средств: "))
        contract.functions.withDraw(amount).transact({'from': account})
        print("Средства успешно выведены")
    except Exception as e:
        print(f"Ошибка при выводе средств: {e}")

def get_balance(account):
    try:
        balance = contract.functions.getBalance().call({'from': account})
        print(f"Баланс на смарт-контракте: {balance}")
    except Exception as e:
        print(f"Ошибка при получении баланса: {e}")

def get_estates():
    try:
        print("Информация о доступных недвижимостях:")
        estates = contract.functions.getEstates().call()
        for estate in estates:
            print(f"ID: {estate[5]}, Размер: {estate[0]}, Адрес: {estate[1]}, Владелец: {estate[2]}, Тип: {estate[3]}, Активность: {estate[4]}")
    except Exception as e:
        print(f"Ошибка при получении информации о недвижимости: {e}")

def get_ads():
    try:
        print("Информация о текущих объявлениях:")
        ads = contract.functions.getAds().call()
        for ad in ads:
            print(f"ID объявления: {ad[5]}, ID недвижимости: {ad[3]}, Цена: {ad[2]}, Владелец: {ad[0]}, Покупатель: {ad[1]}, Статус: {ad[6]}")
    except Exception as e:
        print(f"Ошибка при получении информации о объявлениях: {e}")

def get_account_balance(account):
    try:
        balance = w3.eth.get_balance(account)
        print(f"Баланс вашего аккаунта: {balance} WEI")
    except Exception as e:
        print(f"Ошибка при получении баланса аккаунта: {e}")


def main():
    account = ""
    while True:
        if account == "" or account is None:
            print("Добро пожаловать в агенство по недвижимости 'Solidity Company:)'")
            print("\n1.Авторизация \n2.Регистрация \n3.Выход ")
            try:
                choice = int(input("Введите цифру: "))
            except ValueError:
                print("Ошибка: Введите число от 1 до 3")
                continue
            
            if choice == 1:
                account = login()
            elif choice == 2:
                registration()
            elif choice == 3:
                break
            else:
                print("Ошибка: Введите число от 1 до 3")
        else:
            print(f"Добро пожаловать, {account}")
            print("Меню: \n1. Создать недвижимость \n2. Создать объявление \n3. Изменить статус недвижимости \n4. Изменить статус объявления \n5. Приобрести недвижимость \n6. Вывести средства \n7. Баланс аккаунта \n8. Недвижимость \n9. Текущие объявления \n10. Текущий баланс вашего аккаунта \n11.Выход ")
            
            try:
                choice = int(input("Введите цифру: "))
            except ValueError:
                print("Ошибка: Введите число от 1 до 11")
                continue

            if choice == 1:
                create_estate(account)
            elif choice == 2:
                create_advertisement(account)
            elif choice == 3:
                change_estate_status(account)
            elif choice == 4:
                change_advertisement_status(account)
            elif choice == 5:
                purchase_estate(account)
            elif choice == 6:
                withdraw_funds(account)
            elif choice == 7:
                get_balance(account)
            elif choice == 8:
                get_estates()
            elif choice == 9:
                get_ads()
            elif choice == 10:     
                get_account_balance(account)
            elif choice == 11:       
                account = None
            else:
                print("Ошибка: Введите число от 1 до 11")


if __name__ == "__main__":
    main()
