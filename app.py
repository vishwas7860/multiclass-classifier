from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

app = Flask(__name__)

# Load the saved model
model = load_model("my_model.h5")

# Load the LabelEncoder object
max_len = joblib.load("max_len.pkl")
label_mapping_sub_product = joblib.load("label_mapping_sub_product.pkl")
label_mapping_product = joblib.load("label_mapping_product.pkl")
label_mapping_issue = joblib.load("label_mapping_issue.pkl")
label_mapping_sub_issue = joblib.load("label_mapping_sub_issue.pkl")
tokenizer = joblib.load("tokenizer.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_text = data['text']

        # Tokenize and preprocess the text
        sample_sequences = tokenizer.texts_to_sequences([input_text])
        sample_padded = pad_sequences(sample_sequences, maxlen=max_len)

        # Make predictions
        predicted_probs = model.predict(sample_padded)

        # Get the predicted labels
        predicted_product = label_mapping_product[np.argmax(predicted_probs[0])]
        predicted_sub_product = label_mapping_sub_product[np.argmax(predicted_probs[1])]
        predicted_issue = label_mapping_issue[np.argmax(predicted_probs[2])]
        predicted_sub_issue = label_mapping_sub_issue[np.argmax(predicted_probs[3])]


        # Prepare the response
        response = {"description": input_text,"product": predicted_product,"sub_product": predicted_sub_product,"issue": predicted_issue,"sub_issue": predicted_sub_issue          
                    }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True)
