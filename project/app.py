
from flask import Flask, url_for, render_template, request
import joblib
import numpy as np
import sqlite3
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
filename = 'calories_burnt.sav'
model = joblib.load(filename=filename)

# Function to insert prediction into the database
def insert_prediction(gender, age, height, weight, duration, heart_rate, body_temp, prediction):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        duration REAL,
        heart_rate REAL,
        body_temp REAL,
        prediction floatS
    )
    ''')
    cursor.execute('''
    INSERT INTO predictions (gender, age, height, weight, duration, heart_rate, body_temp, prediction)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (gender, age, height, weight, duration, heart_rate, body_temp, float(prediction)))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            gender = request.form['gender']
            age = int(request.form['age'])
            height = int(request.form['height'])
            weight = int(request.form['weight'])
            duration = int(request.form['duration'])
            heartRate = int(request.form['heartRate'])
            bodyTemp = float(request.form['bodyTemp'])
        except ValueError:
            error_message = "Please Ensure All Values Are Numerical"
            return render_template('index.html', prediction_text=error_message)

        gender_value = 0 if gender[0].lower() == 'm' else 1

        prediction = model.predict(np.array([gender_value, age, height, weight, duration, heartRate, bodyTemp]).reshape(1, -1))
        output = round(prediction[0], 2)

        # Insert the prediction into the database
        insert_prediction(gender, age, height, weight, duration, heartRate, bodyTemp, output)

        return render_template('index.html', prediction_text=f'You burned {output:.2f} calories today')
    else:
        return render_template('index.html', prediction_text='')

@app.route('/view_predictions')
def view_predictions():
    conn = sqlite3.connect('my_database.db')
    query = "SELECT * FROM predictions"
    df = pd.read_sql_query(query, conn)
    conn.close()

    return render_template('view_predictions.html', tables=[df.to_html(classes='data', header="true")])

if __name__ == "__main__":
    app.run(debug=True)

