# Customer Churn Prediction

## 📌 Project Overview
This project aims to predict customer churn for a subscription-based company. Churn is when a customer stops using the company's service. Predicting churn helps the company retain customers and reduce revenue loss.

---

## 🎯 Objective
- Identify customers who are likely to churn.
- Understand the key factors contributing to churn.
- Provide insights for business decisions and customer retention strategies.

---

## 🛠 Tools & Libraries
- Python
- Pandas, NumPy (Data Manipulation)
- Matplotlib, Seaborn (Visualization)
- Scikit-learn (Machine Learning)
- Jupyter / Google Colab (Notebook Execution)

---

## 📝 Dataset
- The dataset includes customer information such as:
  - `customer_id`
  - `gender`
  - `tenure` (months)
  - `monthly_charges`
  - `total_charges`
  - `contract_type`
  - `payment_method`
  - `churn` (0 = No churn, 1 = Churn)

> Note: For privacy, only a sample dataset or synthetic data can be included in GitHub.

---

## ⚙️ Project Steps

1. **Data Loading**  
   Load the dataset using `pandas`.

2. **Data Cleaning**  
   - Remove duplicates  
   - Handle missing values  
   - Convert numeric columns  

3. **Exploratory Data Analysis (EDA)**  
   - Visualize churn distribution  
   - Analyze correlations between features and churn  
   - Boxplots, histograms, and bar charts  

4. **Feature Engineering**  
   - Encode categorical variables using LabelEncoder  
   - Create new features like:
     - `avg_monthly = total_charges / tenure`
     - `is_long_term_contract`  

5. **Train/Test Split**  
   - Split data into 70% training and 30% testing sets  

6. **Model Building**  
   - Random Forest Classifier  
   - Train the model on training data  

7. **Evaluation**  
   - Confusion Matrix  
   - Classification Report  
   - ROC-AUC Score  

8. **Feature Importance**  
   - Identify which factors have the most influence on churn  

9. **Dashboard & Visualization**  
   - Churn Rate by Contract Type  
   - Churn Rate by Payment Method  
   - Other key visualizations to support business insights  

---

## 📊 Insights
- Customers with month-to-month contracts and shorter tenure are more likely to churn.  
- High monthly charges are correlated with higher churn risk.  
- Long-term contracts reduce churn probability.

---


