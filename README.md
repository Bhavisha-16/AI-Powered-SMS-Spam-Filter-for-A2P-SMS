# AI-Powered-SMS-Spam-Filter-for-A2P-SMS

## Project Overview

The **AI-Powered SMS Spam Classifier** is an intelligent solution designed to automatically detect and filter unwanted SMS messages. With the rapid increase of promotional and fraudulent SMS campaigns, organizations face challenges in ensuring that critical transactional messages (such as OTPs, alerts, and confirmations) are delivered without interruption, while spam and promotional content are effectively filtered.

This project leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** techniques to analyze SMS content and classify it as either **Spam** or **Legitimate (Transactional)**. The model is trained using **TF-IDF (Term Frequency–Inverse Document Frequency)** for text vectorization and a **Logistic Regression classifier** for prediction, providing a balance of accuracy, interpretability, and efficiency.

The system is exposed through a **REST API built with FastAPI**, allowing seamless integration with applications and enterprise systems. A **Swagger UI interface** is also available at `http://127.0.0.1:8000/docs#/default/predict_get_predict_get` for easy testing and documentation.

Key Highlights:

*  **Real-time Classification** – Fast and lightweight model optimized for production use.
*  **Whitelist Feature** – Prevents false positives by allowing trusted keywords or senders.
*  **Containerized Deployment** – Delivered with Docker for consistent and portable deployment across environments.
*  **Business Impact** – Reduces spam exposure, protects customers from fraud, and ensures delivery of important messages.

This solution can be integrated into **telecom platforms, enterprise messaging systems, and customer engagement applications**, making communication more secure, efficient, and reliable.


## Steps to Run the Project

## Docker Deployment

1. Clone the Repository

 git clone https://github.com/Bhavisha-16/AI-Powered-SMS-Spam-Filter-for-A2P-SMS



2. Build the Docker Image

 docker build -t sms-filter:latest .


3. Run the Docker Container

 docker run -d --name sms-filter -p 8000:8000 sms-filter:latest


4. Access the API

 Open http://127.0.0.1:8000/docs#/default/predict_get_predict_get
 in your browser.

 You will see an interactive Swagger UI to test predictions.

5. Send a Sample Request

 curl -X POST "http://127.0.0.1:8000/predict" \
 -H "Content-Type: application/json" \
 -d '{"message": "Congratulations! You have won a free voucher"}'


 Response Example:

 {
   "message": "Congratulations! You have won a free voucher",
   "prediction": "Spam"
 }

## Render Deployment
Base URL: https://ai-powered-sms-spam-filter-for-a2p-sms.onrender.com

Docs: https://ai-powered-sms-spam-filter-for-a2p-sms.onrender.com/docs#/default/predict_get_predict_get

## Streamlit Deployment

App URL: https://ai-powered-sms-spam-filter-for-a2p-sms-frpmgqjnnux2vt3mqtshxt.streamlit.app/
