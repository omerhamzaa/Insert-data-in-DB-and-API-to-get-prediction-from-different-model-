import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.svm import SVC
from fastapi import FastAPI
from sklearn.metrics import mean_squared_error
import sqlite3
import csv

app = FastAPI()

conn = sqlite3.connect('Insurance.db')
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS TravelInsurance
             (ID INTEGER PRIMARY KEY,Age INTEGER, AnnualIncome INTEGER, FrequentFlyer INTEGER, TravelInsurance INTEGER)''')
# Create second table
c.execute('''CREATE TABLE IF NOT EXISTS Sales
             (ID INTEGER PRIMARY KEY,sale int)''')


with open(r'C:\Users\razza\Desktop\travel\travel_insurance.csv', 'r') as file:
    # Your code to read the CSV file

    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        c.execute("INSERT INTO TravelInsurance (Age, AnnualIncome, FrequentFlyer, TravelInsurance ) VALUES (?, ?,?, ?)", row)

with open(r'C:\Users\razza\Desktop\travel\Sales.csv', 'r') as file:
    # Your code to read the CSV file

    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        c.execute("INSERT INTO Sales (sale) VALUES (?)", row)

sql = """
    SELECT * 
    FROM TravelInsurance AS c 
    INNER JOIN Sales AS p ON c.ID = p.ID
"""

c.execute(sql)
data = c.fetchall()
# print(data)

columns = ["ID", "ID", "sale", "Age", "AnnualIncome", "FrequentFlyer", "TravelInsurance"]
df = pd.DataFrame(data, columns=columns)

x = df[['Age', 'AnnualIncome', 'FrequentFlyer','sale']]
y = df['TravelInsurance']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

gnb = GaussianNB()
gnb.fit(x_train, y_train)
y_pred = gnb.predict(x_test)
accuracy = metrics.accuracy_score(y_test, y_pred)


svc_model = SVC(kernel='linear')
svc_model.fit(x_train, y_train)
y_pred= svc_model.predict(x_test)
acc_score= accuracy_score(y_test,y_pred)


num_trees = 150
model_rf = RandomForestRegressor(n_estimators=num_trees, max_depth=4)
model_rf.fit(x_train,y_train)
y_pred= model_rf.predict(x_train)
y_pred = model_rf.predict(x_train)
# Calculate Mean Squared Error
mse = mean_squared_error(y_train, y_pred)


num_trees = 150
model_rf = RandomForestClassifier(n_estimators=num_trees, max_depth=4, class_weight="balanced")
model_rf.fit(x_train,y_train)
y_pred= model_rf.predict(x_train)
accuracy_rf = accuracy_score(y_train, y_pred)

@app.get("/accuracy_results")
async def get_all_data():
    results = {
        "Accuracy_GaussianNB": accuracy,
        "Accuracy_SVM": acc_score,
        "Mean Squared Error": mse,
        "Accuracy with RandomForest Model is : ": accuracy_rf
         }
    return results