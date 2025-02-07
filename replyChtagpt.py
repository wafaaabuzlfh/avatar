import openai
import os
import openai.error
import pdfplumber # to open pdf 
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY2")

# تحديد المسار الكامل للملف
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # مجلد المشروع الرئيسي
pdf_path = os.path.join(BASE_DIR, 'sounds', 'file_name.extension') 



def speachRecognition(audio_file):
    #audio_file = open("./welcome.mp3", "rb")
    transcription = openai.Audio.transcribe(
          model="whisper-1", 
          file=audio_file, 
          response_format="text"
      )
    print(transcription)
    return transcription
      
    

content = """
أنت عالم تفاعلي يتمثل في صورة أفاتار لطيف مصمم للتواصل مع الأطفال. مهمتك هي تعليم الأطفال عن الطقس بأسلوب بسيط وسلس،
 باستخدام قصص قصيرة ومفاهيم سهلة الفهم. عندما يبدأ الطفل بالتحدث معك، حافظ على الحوار طويلًا وممتعًا قدر الإمكان.
   اجعل إجاباتك محفزة للتفاعل من خلال تضمين أسئلة وأفكار تدفع الطفل للاستمرار في التواصل معك والتفاعل مع الموضوع بشكل أكبر.
   وايضا تواصل مع الطفل باسمه سيتم اعطاءك الاسم ببدايةالدردشة
"""


def extract_text_with_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text
pdf_text = extract_text_with_pdfplumber("./instruction.pdf")

def chatText(prompt, history, question, username):
    sys = f"""انت عالم مجيب متشكل بشكل افاتر يحاور الاطفال
      لتعليمهم حول الطقس بطريقة تعليمية مبهجة اتبع الخطوات بهذا الكتاب \n 
    {pdf_text} عليك التحاور مع الطفل باستخدام اسمه وجعل الحوار تسائلي 
    لتعليم الطفل مهارات 
    سيكون عليك بدء الحديث مع الطفل عند ارسال لك كلمة (start) تبدأ معه بمثل الاسئلة في الكتاب \n
    \n عند ارسال كلمة (timout) تخبر الطفل انه الوقت للحوار اليوم انتهى حيث انه اوقات الانشطة المحددة كل يوم هي ربع ساعة كحد افصى
    \n عند ارسال كلمة (end) يجب ان تعطيني ملخص كامل عن المحادثة التي اجريتها مع الطفل بشكل مختصر يعبر عن المحادثة بالتفصيل ايضا.
    \n عند ارسال كلمة (achievmentPercentage) سأعطيك كامل المحادثة التي اجريتها مع الطفل لتخطي مهارة معينة سيكون عليك تقدير النسبة التي يستخقها الطفل لحصوله على المهارة حيث ستعطيني فقط النسبة فقط مثلا (ex. 90%, 80%, 100%) 
     ستحصل على تفاصيل تحديد النسبة من المعلم تأكد من امر المعلم جيداً كما ستحصل على نسبة الطفل السابقة التي حصل عليها اخر مرة عند محاولته تنفيذ النشاط قم بمقارنة النتائج وتحليلها بشكل احترافي لتعطي نسبة حقيقية بناء على كل المعايير التي يوفرها المعلم والمهارة والكتاب.
      هذا الامر المخصص من المعلم لتعلم الطفل النشاط المراد \n 
      'امر المعلم': {prompt}"""
    mesg = [{"role":"system", "content": sys},]
    if history != []:
        for h in history:
            mesg.append(h)
    mesg.append({"role": "user","content":f"اسمي: {username} , الحديث: {question}"})

    try:
        response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=mesg,
        )
        return response["choices"][0]["message"]["content"]
    except:
        return "هناك خطأ ما الرجاء المحاولة لاحقا"



#r = chatText(prompt=content, history=[], question="start", username="ahmed")
#print(r)
#mesg = [{"role":"system", "content":content},]
#mesg.append({"role": "user","content":"مرحبا"},)

#resp = chatText(mesg)
#mesg.append({"role": "assistant","content":resp},)
#print(resp)

#audio_file = open("./welcome.mp3", "rb")
#speachRecognition(audio_file)