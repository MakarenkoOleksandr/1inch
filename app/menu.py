from modules.get_chain_and_rpc import user_input_chain
from app.check_balance import TokenBalanceChecker
from app.swapper import main
import asyncio

def menu():
    #Выбираем сеть
    user_input_chain
    while True:
        #Выбираем действия с кошельком
        print('Choose option like 1, 2, 3 etc: ')
        print('1. Check balance')
        print('2. Make swap')
        print('3. Exit')
            
        choises = input('Option: ')
        if choises == '1':
            asyncio.run(TokenBalanceChecker.main())
        if choises == '2':
            main()
        if choises == '3':
            break
