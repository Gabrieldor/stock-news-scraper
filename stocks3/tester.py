import pandas as pd

#2% pra cima
#3% pra baixo

def simulate(csv ,final_money):

    df = pd.read_csv(csv)
    df['date'] = pd.to_datetime(df['date'])

    df['day'] = df['date'].dt.date

    grouped = df.groupby('day')
    filtered_df = df[df["date"].dt.strftime("%H:%M") < "13"]
    filtered_df.to_csv("aa.csv")

    input()


    money = 0
    stock = df.iloc[-1, 2]
    money -= stock
    last_sell = 0
    sell = False
    buy = False
    last_stock = 99999
    last_stock_buy = 0
    print(df.iloc[-1, 2])


    for day, group in grouped:
        #print(group)
        for t in group.values[::-1]:
            op_hour = t[2]

            if sell == True:
                stock = None
                money += op_hour
                last_sell = op_hour
                sell = False

            if buy == True:
                stock = op_hour
                money -= op_hour
                buy = False

            if (t[0].hour > 10) and stock != None:
                continue

            if stock != None and op_hour > stock * (1 + 50/1000):
                sell = True
            if stock == None and op_hour < last_sell * (1 - 5/1000):
                buy = True

            if (t[0].hour > 10) and stock == None:
                buy = True

    final_money += money
    
    return final_money

money = 0
money = simulate("data.csv", money)
print(money)
