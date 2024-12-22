# Inputs
Principle = int(input('Enter The Principle Amount :- '))
Rate = int(input('Enter Rate Of Interest :- '))
Time = int(input('For How Many Years Money Is Deposited For:- '))
n = int(input('How Many Times Amount Is Compounded Per Year :- '))

# Main Calculation
compRate = Rate/(100*n)
SI = (Principle*Rate*Time)/100
CI = Principle*(1 + compRate)**(Time*n) - Principle

print(f'Simple Interest On Rs.{Principle} For {Time} months When Compounded :- {SI}\n'
      f'Compound Interest On Rs.{Principle} For {Time} months :- {round(CI, 2)}\n'
      f'Amount With Compound Interest:- {round(Principle+CI, 2)}')
