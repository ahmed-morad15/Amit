def std_info(name:str, age:int):
    """
    this function take student information
    param_1 : user name
    type param_1 : str
    param_2 : user age
    type param_2 : int

    return : print student information
    type return : str , int

    """
    return f"my name is {name}, and my age is {age}"






def main ():
    """
    this function take two number and operation from user and do this operation on numbers
    num1 : first number
    type num1 : float
    num2 : second number
    type num2 : float
    operation : 
    """
    print("choose operation")
    print("1-sum")
    print("2-sub")
    print("3-mul")
    print("4-div")

    choice =input("enter operation")
    num1 = float(input("enter first number"))
    num2 = float(input("enter first number"))

    if choice == '1':
        result = num1+num2
    elif choice == '2':
        result = num1-num2
    elif choice == '3':
        result = num1*num2
    elif choice == '4':
        result = num1/num2
    else:
        print("invalled")
        return
    print("result",result)

if __name__ == "__main__":
    main()
