# Crop Price Predictor Website - README

## 📄 Project Overview
This is a **Crop Price Prediction and Farmer Support System** built using **Machine Learning** and **Web Technologies**. The system predicts the expected price of crops based on historical data and also provides crop suggestions when prices are unfavorable.

---

## 🚀 Features
- Predicts crop prices using ML algorithms (Random Forest, KNN, Decision Trees).
- Displays real-time rainfall predictions based on crop requirements.
- Suggests alternative crops when current crop prices are too low.
- Provides information about government schemes and farmer benefits.
- User-friendly, responsive web interface.

---

## 🛠 Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, Pandas, Numpy
- **Visualization:** Matplotlib, Plotly

---

## 💾 Installation & Setup
1. Clone this repository or extract the provided zip.
2. Install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```bash
   python app.py
   ```
4. Open your browser and go to:
   ```
   http://127.0.0.1:8080
   ```

---

## 📊 How It Works
- Users select a **state**, **district**, and **crop**.
- The system uses trained models to predict:
  - Expected crop price
  - Expected rainfall needed
  - Profitability of the selected crop
- If the price is low, the system suggests better alternative crops.

---

## 🌾 Future Enhancements
- Add real-time weather API for live rainfall data.
- Integrate live market price APIs for more accurate predictions.
- Multi-language support for regional accessibility.

---

## 🙏 Credits
Developed by: **Akash Gudipalli**  
For any queries: akashgudipalli0@gmail.com

---

## 📌 License
This project is licensed under the MIT License.
