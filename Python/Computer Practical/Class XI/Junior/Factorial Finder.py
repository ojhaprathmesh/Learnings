Num = int(input('Enter The Number: '))
Multiplier = Num
Answer = Num

while Multiplier > 1:
    Multiplier -= 1
    Answer *= Multiplier
print(f"{Num}! = {Answer} Using While Loop")

Answer = Num
for i in range(1, Num):
    Answer *= i
print(f"{Num}! = {Answer} Using For Loop")
