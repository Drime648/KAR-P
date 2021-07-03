from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
app = Flask(__name__)

model = tf.keras.models.load_model("CNN_model")
class_names = ["hate speech", "offensive language", "clean"]

@app.route('/predict/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    text = request.args.get("text", None)

    # For debugging
    # print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not text:
        response["ERROR"] = "no text found, please send a name."
    # Check if the user entered a number not a name
    elif str(text).isdigit():
        response["ERROR"] = "text can't be numeric."
    # Now the user entered a valid name
    else:
        # response["MESSAGE"] = f"Welcome {text} to our awesome platform!!"
        data = model.predict([text])
        pred = class_names[np.argmax(data)]
        response["VERDICT"] = pred
        


    # Return the response in json format
    return jsonify(response)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)