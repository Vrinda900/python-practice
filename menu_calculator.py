#Menu-based calculator
hist=[]
while True:
    print("Operations:\n 1.ADD\t2.SUBTRACT\t3.MULTIPLY\t4.DIVIDE\t5.POWER\t6.MODULAS\t7.EXIT")
    ch=int(input("enter your choice:"))
    if ch == 7:
        print("exit!")
        break
    if ch<1 | ch>7:
        print("Invalid choice, try again.")
        continue
    a=int(input("enter first number for calculation:"))
    b=int(input("enter second number for calculation:"))
    match ch:
        case 1:
            res=a + b
            symbol="+"
        case 2:
            res=a - b
            symbol="-"
        case 3:
            res=a * b
            symbol="*"
        case 4:
            if b==0:
                print("Error: division by zero!")
                continue
            res=a / b
            symbol="/"
        case 5:
            res=a ** b
            symbol="**"
        case 6:
            if b==0:
                print("Error: modulus by zero!")
                continue
            res=a% b
            symbol="%"
    print("Result:", res)
    hist.append(f"{a} {symbol} {b} = {res}")
    print("history of calculations:")
    for x in hist:
        print(x)