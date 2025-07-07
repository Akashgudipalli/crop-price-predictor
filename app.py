
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import csv, os, requests, json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_KEY = '64ef503ff505ea951647376cc2512e21'
USERS_CSV = 'users.csv'

# Load full state-district map from file
with open('state_district_map_full.json', 'r', encoding='utf-8') as f:
    STATE_DISTRICT_MAP = json.load(f)

CROP_DATA = {
    'Rice': {'min_price': 1500, 'sowing_month': 'June'},
    'Wheat': {'min_price': 1700, 'sowing_month': 'November'},
    'Maize': {'min_price': 1400, 'sowing_month': 'July'},
    'Cotton': {'min_price': 5000, 'sowing_month': 'May'},
    'Sugarcane': {'min_price': 3000, 'sowing_month': 'March'},
    'Bajra': {'min_price': 1200, 'sowing_month': 'June'},
    'Jowar': {'min_price': 1300, 'sowing_month': 'June'},
    'Barley': {'min_price': 1600, 'sowing_month': 'October'},
    'Groundnut': {'min_price': 4000, 'sowing_month': 'June'},
    'Soybean': {'min_price': 3500, 'sowing_month': 'June'},
    'Mustard': {'min_price': 4200, 'sowing_month': 'October'},
    'Tur (Arhar)': {'min_price': 5500, 'sowing_month': 'June'},
    'Urad': {'min_price': 5400, 'sowing_month': 'June'},
    'Moong': {'min_price': 7000, 'sowing_month': 'June'},
    'Masoor': {'min_price': 5100, 'sowing_month': 'October'}
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        state = request.form.get('state')
        phone = request.form.get('phone')
        password = request.form.get('password')

        file_exists = os.path.isfile(USERS_CSV)
        with open(USERS_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['name', 'age', 'state', 'phone', 'password'])
            writer.writerow([name, age, state, phone, password])

        return redirect(url_for('login'))

    return render_template('register.html', states=STATE_DISTRICT_MAP.keys())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')

        if not os.path.isfile(USERS_CSV):
            return 'No users registered yet. <a href="/register">Register first</a>'

        with open(USERS_CSV, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['phone'] == phone and row['password'] == password:
                    session['user'] = row['name']
                    return redirect(url_for('predict'))

        return 'Invalid credentials. <a href="/login">Try again</a>'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        crop = request.form['crop']
        state = request.form['state']
        district = request.form['district']
        city = f"{district},{state}"

        # Weather and rainfall prediction
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url).json()
        rainfall_list = [entry.get('rain', {}).get('3h', 0) for entry in response.get('list', [])]
        total_rainfall = round(sum(rainfall_list), 2)

        # Simulated price (replace this with actual logic or API if needed)
        price = CROP_DATA[crop]['min_price'] - 200  # force lower price for testing suggestion

        # Suggestion logic based on crop's min price
        import random

        min_price = CROP_DATA[crop]['min_price']
        price = random.randint(min_price - 300, min_price + 500)

        # Suggestion logic based on price
        if price < min_price:
            suggested_crops = [
                alt_crop for alt_crop, data in CROP_DATA.items()
                if alt_crop.lower() != crop.lower() and data['min_price'] > price
            ][:3]
            suggestion_message = f"The price for {crop} is currently low. Consider growing: {', '.join(suggested_crops)}"
        else:
            suggestion_message = f"The price for {crop} is currently good. You can proceed to grow it."


        return render_template('result.html', crop=crop, price=price, rainfall=total_rainfall, suggestion=suggestion_message)

    return render_template('predict.html', crops=CROP_DATA.keys(), states=STATE_DISTRICT_MAP)

@app.route('/get_districts', methods=['POST'])
def get_districts():
    state = request.json.get('state')
    districts = STATE_DISTRICT_MAP.get(state, [])
    return jsonify({'districts': districts})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # ✅ 4 spaces before this line


