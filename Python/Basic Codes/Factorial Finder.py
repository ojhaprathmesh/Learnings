Num = int(input('Enter The Number :- '))
Multiplier = Num
Answer = Num
# ==== Use Any One While Or For, Both Works ====
# while Multiplier>1:
#     Multiplier-=1
#     Num*=Multiplier
for i in range(1, Num):
    Answer *= i
print(Num, Answer, end='')
