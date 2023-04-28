import sqlite3
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    print("OUR REQUEST IS", request.values)
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    whatsapId = request.values.get('WaId').lower()
    ProfileName = request.values.get('ProfileName')
    accauntSid = request.values.get('AccountSid')
    
    con = sqlite3.connect("WhatsappUsers.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS `WhatsapUsers` (
            `WhatsapId` INT(32) NOT NULL,
            `Profile_name` TEXT(124),
            `Verification_Level` TEXT(124),
            `User_Name` TEXT(124),
            `User_Messages` INT(124),
            PRIMARY KEY (`WhatsapId`)
        );
        '''
    )
    
    selectQuery = "SELECT * from WhatsapUsers WHERE (WhatsapId=?);"
    selectValue = [whatsapId]
    
    user = cur.execute(selectQuery, selectValue).fetchone()
    
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    
    if user:
        print(user)
        msg.body(f'Hello user: {ProfileName}, We have your information in our database')
    else:
        msg.body(f'Hello, seems like you are a new user. Welcome!!!\n\nProfile name: {ProfileName},\n Whatsapp Id: {whatsapId},\n Accaunt Sid: {accauntSid}\n, Message: "SENDING" \n')
        query = "INSERT INTO WhatsapUsers (Profile_name, WhatsapId) VALUES (?, ?);"
        val = [ProfileName, whatsapId]
        cur.execute(query, val)
        con.commit()

    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
