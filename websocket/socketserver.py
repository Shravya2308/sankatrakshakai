import asyncio
import websockets
from gcp import transcribe_file,translate_text
from transformers import AutoTokenizer, AutoModelForTokenClassification
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client['sankatrakshak']
results = db.results
# create handler for each connection
language_code = ""
async def handler(websocket, path):
    while True:
        data = await websocket.recv()
        if data == 'hi':
            print(data)
            soundfile = open('mastercta.wav','rb')
            sound = soundfile.read()
            reply = f"Data recieved as:  {data}!"
            await websocket.send(sound)
        elif data =='start':
            print(data)
        elif data == '1':
            language_code = "en-US"
            print(type(data))
            english = open('english.wav','rb')
            engsound = english.read()
            print("hi")
            reply = f"Data recieved as:  {data}!"
            # await websocket.send(engsound)
        elif data == '2':
            language_code = "hi-IN"
            soundfile = open('hindi.wav','rb')
            sound = soundfile.read()
            reply = f"Data recieved as:  {data}!"
            # await websocket.send(sound)
        elif data == '3':
            language_code = "mr-IN"
            soundfile = open('marathi.wav','rb')
            sound = soundfile.read()
            reply = f"Data recieved as:  {data}!"
            # await websocket.send(sound)
        else:
            print(data)
            wavfile = open("s.mp3","wb")
            wavfile.write(data)
            def nlp():
                from transformers import pipeline
                text = transcribe_file("s.mp3","mr-IN")
                print(text)
                translation = translate_text("en-US",text)
                tokenizer = AutoTokenizer.from_pretrained("Davlan/distilbert-base-multilingual-cased-ner-hrl")
                model = AutoModelForTokenClassification.from_pretrained("Davlan/distilbert-base-multilingual-cased-ner-hrl")
                nlp = pipeline("ner", model=model, tokenizer=tokenizer)
                example = translation
                ner_results = nlp(example)
                print(ner_results)

                array = []
                for i in range(0, len(ner_results)):
                    if ner_results[i]['entity']=='B-LOC' or ner_results[i]['entity']=='I-LOC':
                        array.append((ner_results[i]['word']))
                    print(array)

                nlp_string = ""
                for i in range(0,len(array)):
                    nlp_string=nlp_string + array[i]
                    print(nlp_string)

                nlp_newstr = nlp_string.replace('#','')
                print(nlp_newstr)



                
                def classipy(text):
                        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
                        sequence_to_classify = text
                        candidate_labels = ['medical','fire','crime-in-progress']
                        return classifier(sequence_to_classify, candidate_labels)
                classipy_result = classipy(translation)
                class_result = (classipy_result['labels'][0])
                print(class_result)

                def priority(text):
                        classifier1 = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
                        sequence_to_classify = text
                        candidate_labels = ['low-emergency','high-emergency','medium-emergency']
                        return classifier1(sequence_to_classify, candidate_labels)
                priority_result = priority(translation)
                priority = (priority_result['labels'][0])
                print(priority)


                dict = {
                    "Translation": translation,
                    "Location": nlp_newstr,
                    "Priority": priority,
                    "Emergency": class_result
                    }
                id = results.insert_one(dict).inserted_id
                print(id)
                status = {
                    "status":"success"
                }
                return status
            nlp()
start_server = websockets.serve(handler, "localhost", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()