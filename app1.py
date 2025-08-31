import streamlit as st
import joblib
import re

# ===============================
# Load trained model + vectorizer
# ===============================
MODEL_PATH = "sms_spam_model.pkl"
model, vectorizer = joblib.load(MODEL_PATH)

# ===============================
# Whitelist rules
# ===============================
whitelisted_domains = ["trip.com", "icicibank.com", "hdfcbank.com"]
whitelisted_phrases = ["your otp is", "do not share this otp", "thank you for shopping with"]
whitelisted_senders = ["ICICIBANK", "HDFCBANK", "AMAZON"]

# ===============================
# Helper Functions
# ===============================
def clean_text(txt):
    txt = str(txt).lower()
    txt = re.sub(r'http\S+|www\.\S+', ' ', txt)
    txt = re.sub(r'[^a-z0-9\s]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

def check_whitelist(message, sender_id=None):
    msg = message.lower()
    for domain in whitelisted_domains:
        if domain in msg:
            return True, f"Domain: {domain}"
    for phrase in whitelisted_phrases:
        if phrase in msg:
            return True, f"Phrase: {phrase}"
    if sender_id and sender_id.upper() in whitelisted_senders:
        if any(k in msg for k in ["otp", "credited", "debited", "transaction", "alert"]):
            return True, f"Sender: {sender_id}"
    return False, None

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="AI-Powered SMS Spam Filter", page_icon="📩", layout="wide")
# ===============================
# Global CSS for font style
# ===============================
st.markdown(
    """
    <style>
    /* Apply Helvetica font globally */
    html, body, [class*="css"]  {
        font-family: 'Helvetica', 'Arial', sans-serif;
    }
    
    /* Optional: ensure headers and card content also use Helvetica */
    h1, h2, h3, h4, h5, h6, p, span, div {
        font-family: 'Helvetica', 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header & Branding
st.markdown(
    """
    <div style='text-align:center; padding:10px;'>
        <h1 style='font-weight:bold;'>📩 AI-Powered SMS Spam Filter</h1>
        <p style='color:gray;'>Detect spam messages and safely allow trusted SMS using AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# Input Section with columns
col1, col2 = st.columns([3, 1])
with col1:
    message = st.text_area("Enter SMS Message", height=150, placeholder="Type or paste your SMS here...")
with col2:
    sender_id = st.text_input(
        "Sender ID (optional) 💡",
        placeholder="Sender name or ID",
        help="Optional: Enter sender's name or ID for better whitelist detection"
    )

st.markdown("---")

# Button & Action
if st.button("Check SMS 📩", type="primary"):
    if not message.strip():
        st.warning("⚠ Please enter a message!")
    else:
        # Whitelist check
        is_white, reason = check_whitelist(message, sender_id)

        # ML Prediction
        cleaned = clean_text(message)
        X_vec = vectorizer.transform([cleaned])
        pred = model.predict(X_vec)[0]
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X_vec)[0]
            spam_prob = prob[1] if pred.lower() == "spam" else prob[0]
        else:
            spam_prob = None

        # Results Layout
        res_col1, res_col2 = st.columns([1,1])

       # Left Card: Whitelist Result (Dark Background for "Not Whitelisted")
        with res_col1:
         if is_white:
        # ✅ Whitelisted: light green card
            st.markdown(f"""
        <div style='background-color:#d4edda; padding:20px; border-radius:15px; 
                    box-shadow: 2px 2px 12px rgba(0,0,0,0.1); font-family: Helvetica, Arial, sans-serif;'>
            <h3 style='color: #155724; font-family: Helvetica, Arial, sans-serif;'>✅ Allowed (Whitelisted)</h3>
            <span style='background-color:#c3e6cb; padding:5px 12px; border-radius:10px; 
                         font-weight:bold; font-family: Helvetica, Arial, sans-serif;'>{reason}</span>
        </div>
        """, unsafe_allow_html=True)
         else:
        # ℹ Not Whitelisted: dark background with white text
          st.markdown(f"""
        <div style='background-color:#2f2f2f; padding:20px; border-radius:15px; 
                    box-shadow: 2px 2px 12px rgba(0,0,0,0.2); font-family: Helvetica, Arial, sans-serif;'>
            <h3 style='color:#ffffff; font-family: Helvetica,sans-serif;'>ℹ Not Whitelisted</h3>
            <span style='background-color:rgba(255,255,255,0.1); padding:5px 12px; border-radius:10px; 
                         font-weight:bold; font-family: Helvetica, Arial, sans-serif;'>No whitelist rules matched</span>
        </div>
        """, unsafe_allow_html=True)


        # Right Card: ML Prediction
        with res_col2:
            if pred.lower() == "spam":
                color_bg, color_text = "#5D5FC8", "#fcfcfc"
                reason_text = "ML model detected as Spam"
            else:
                color_bg, color_text = "#70D5CB", "#170486"
                reason_text = "ML model detected as Ham"

            st.markdown(f"""
                <div style='background-color:{color_bg}; padding:20px; border-radius:15px; box-shadow: 2px 2px 12px rgba(0,0,0,0.1);'>
                    <h3 style='color:{color_text};'>{"✅ Allowed" if pred.lower()=="ham" else "🚫 Blocked"} (AI Prediction: {pred})</h3>
                    <span style='background-color:rgba(0,0,0,0.05); padding:5px 12px; border-radius:10px; font-weight:bold;'>{reason_text}</span>
                    {f"<p style='margin-top:10px;'>Prediction Confidence: {spam_prob*100:.2f}%</p>" if spam_prob else ""}
                    {f"<progress value='{spam_prob*100:.2f}' max='100' style='width:100%; height:15px;'></progress>" if spam_prob else ""}
                </div>
            """, unsafe_allow_html=True)

        # Detailed Analysis Expander
        with st.expander("🔍 Show Detailed Analysis"):
            st.write("*Original Message:*", message)
            st.write("*Cleaned Message:*", cleaned)
            st.write("*Sender ID:*", sender_id if sender_id else "N/A")
            if spam_prob:
                st.write(f"*Prediction Confidence:* {spam_prob*100:.2f}%")

# Footer Section
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>⚡ Powered by AI | Developed with ❤ using Streamlit</p>",
    unsafe_allow_html=True
)