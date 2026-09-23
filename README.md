# 🌱 Smart Agriculture System

An AI/ML-based Smart Agriculture System that recommends the most suitable crop based on soil nutrients and environmental conditions.

The system uses Machine Learning to analyze **Nitrogen (N), Phosphorus (P), Potassium (K), temperature, and humidity** and predicts the crop that is most suitable for the given conditions.

## 🚀 Features

* 🌾 AI-based crop recommendation
* 🧪 Soil nutrient analysis
* 🌡️ Temperature and humidity-based prediction
* 🤖 Machine Learning model using Support Vector Classifier (SVC)
* 🖥️ Interactive Streamlit web application
* 📊 Simple and user-friendly interface
* 📱 Responsive application interface
* 🔐 Login functionality
* 🌐 Multi-language support

## 🛠️ Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-learn
* Support Vector Classifier (SVC)
* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### Web Application

* Streamlit

### Development Tools

* Jupyter Notebook
* Git
* GitHub

## 📂 Project Structure

```text
Smart-Agriculture-System/
│
├── .streamlit/
│   └── config.toml
│
├── app.py
├── Crop_recommendation.csv
├── crop_model.pkl
├── smart_agri_sys.ipynb
├── .gitignore
└── README.md
```

## 📊 Dataset

The project uses a crop recommendation dataset containing agricultural and environmental parameters such as:

| Feature     | Description                |
| ----------- | -------------------------- |
| N           | Nitrogen content in soil   |
| P           | Phosphorus content in soil |
| K           | Potassium content in soil  |
| Temperature | Environmental temperature  |
| Humidity    | Environmental humidity     |
| Label       | Recommended crop           |

The dataset contains multiple crop classes including rice, maize, chickpea, kidney beans, pigeon peas, mung bean, banana, mango, grapes, watermelon, apple, orange, papaya, coconut, cotton, jute, and coffee.

## 🧠 Machine Learning Workflow

The project follows a typical Machine Learning pipeline:

```text
Dataset
   ↓
Data Preprocessing
   ↓
Exploratory Data Analysis
   ↓
Feature Selection
   ↓
Train-Test Split
   ↓
Feature Scaling
   ↓
SVC Model Training
   ↓
Model Evaluation
   ↓
Model Serialization
   ↓
Streamlit Web Application
   ↓
Crop Recommendation
```

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/TechKirtisingh/Smart-Agriculture-System.git
```

Navigate to the project:

```bash
cd Smart-Agriculture-System
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## 🔮 Future Improvements

* 🌦️ Integration with real-time weather APIs
* 🌱 Soil moisture monitoring
* 📡 IoT-based sensor integration
* 💧 Smart irrigation recommendations
* 🐛 Crop disease detection
* 📈 Crop yield prediction
* ☁️ Cloud deployment
* 📱 Mobile application support
* 🤖 AI-powered agriculture assistant

## 👩‍💻 Author

**Kirti Singh**

Computer Science Engineering Student

GitHub: https://github.com/TechKirtisingh

---

⭐ If you find this project useful, consider giving it a star!
