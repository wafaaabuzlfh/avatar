from flask import Flask, jsonify, request, send_file
import os
import replyChtagpt
from SpeachEleven import audioGenerating
app = Flask(__name__)

global HISTORY
HISTORY = {}
# تحديد مسار المجلد المخصص لحفظ الملفات
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'sounds')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/flaskpy")
def home():
    return """
    <html>
        <body><h1> API is a working </h1> </body>
    </html>
    """

@app.route("/flaskpy/teacher", methods=["POST"])
def teacherAI():
    global HISTORY
    data = request.json
    prompt = data.get('command') #prompt gpt4 as text
    username = data.get('user') #text 
    status = data.get('status') # start | end | talk  | timeout
    achP = data.get('achievmentPercentage') # char ex."90%" or null     
    if status == "start":  
        HISTORY[username] = []
        reply = replyChtagpt.chatText(prompt= prompt,
                                        history=[], question= status, username=username)
        HISTORY[username].append({"role": "user","content":status})
        HISTORY[username].append({"role": "assistant","content": reply})
        encoded_audio, status_code = audioGenerating(reply)
        if status_code == 200:
            result = {"audio": encoded_audio, "summary": None,
                    "achievmentPercentage" : None}
            return jsonify(result),200
        else:
            return jsonify({"error":encoded_audio}), 400
    elif status == "talk":
        file = request.files['question'] #audio record or null
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            audio_file = open(file_path, "rb")   
            question = replyChtagpt.speachRecognition(audio_file)
            history = HISTORY[username]
            reply = replyChtagpt.chatText(prompt, history, question, username)
            HISTORY[username].append({"role": "user","content":question})
            HISTORY[username].append({"role": "assistant","content": reply})
            encoded_audio, status_code = audioGenerating(reply)
            if status_code == 200:
                result = {"audio": encoded_audio, "summary": None,
                        "achievmentPercentage" : None}
                return jsonify(result),200
            else:
                return jsonify({"error":encoded_audio}), 400
        else:
            return jsonify({"error":"Invalid file record"}), 400
    elif status == "timOut":
        HISTORY[username] = []
        reply = replyChtagpt.chatText(prompt= prompt,
                                        history=[], question= status, username=username)
        HISTORY[username].append({"role": "user","content":status})
        HISTORY[username].append({"role": "assistant","content": reply})
        encoded_audio, status_code = audioGenerating(reply)
        if status_code == 200:
            result = {"audio": encoded_audio, "summary": None, 
                    "achievmentPercentage" : None}
            return jsonify(result),200
        else:
            return jsonify({"error":encoded_audio}), 400
    elif status == "end":
        
        history = HISTORY[username] 
        reply = replyChtagpt.chatText(prompt= prompt,
                                        history=history, question= status, username=username)

        new_achp = replyChtagpt.chatText(prompt= prompt,
                                        history=history, question= f"achievmentPercentage, old: {achP}", username=username)

        del HISTORY[username]
        return jsonify({"audio": None, "summary": reply,
                    "achievmentPercentage" : new_achp})
    else:
        return jsonify({"error":"Ivalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)