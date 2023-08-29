import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import email, password


insults = [
    "You're so dense, light bends around you.",
    "I'm not saying you're stupid, I'm just saying you have bad luck when thinking.",
    "Is your ass jealous of the amount of shit that comes out of your mouth?",
    "You're like a human version of a participation award.",
    "You must have been born on a highway because that's where most accidents happen.",
    "It's a shame you can't Photoshop your personality.",
    "You're not pretty enough to have such an ugly personality.",
    "I'd agree with you but then we'd both be wrong.",
    "You're a gray sprinkle on a rainbow cupcake.",
    "I'm trying to see things from your perspective, but I can't get my head that far up my ass.",
    "If laughter is the best medicine, your face must be curing the world.",
    "I'd slap you, but that would be animal abuse.",
    "You're so ugly, when you got robbed, the robbers made you wear their masks.",
    "Are you always so stupid or is today a special occasion?",
    "If I wanted to kill myself, I'd climb your ego and jump to your IQ.",
    "Mirrors can't talk. Lucky for you, they can't laugh either.",
    "The only thing you're good at is being a bad example.",
    "If your brain was dynamite, there wouldn't be enough to blow your hat off.",
    "You're the reason the gene pool needs a lifeguard.",
    "You're so fake, even China denied they made you.",
    "I'm not insulting you, I'm describing you.",
    "You're not even on my level, you're a different species.",
    "You're so boring, you make a dictionary seem like a cliffhanger.",
    "I'd call you a tool, but even they serve a purpose.",
    "You're not stupid; you just have bad luck when thinking.",
    "I'd tell you to go outside and get some fresh air, but your breath might kill all the plants.",
    "You're impossible to underestimate.",
    "If I had a face like yours, I'd sue my parents.",
    "I'm not arguing, I'm just explaining why I'm right.",
    "If you were any more inbred, you'd be a sandwich.",
    "You must be a software update because not now.",
    "You're like a penny: two-faced and practically worthless.",
    "I'm not insulting you; I'm describing you.",
    "I don't insult people; I just describe them.",
    "You're not stupid; you just have bad luck thinking.",
    "I'd say you're funny, but looks aren't everything.",
    "I thought of you today. It reminded me to take out the trash.",
    "You're the reason the gene pool needs a lifeguard.",
    "I'd agree with you but then we'd both be wrong.",
    "I'm not saying I hate you, but I'd unplug your life support to charge my phone.",
    "I can't put my finger on it, but I think you're an idiot.",
    "If laughter is the best medicine, your face must be curing the world.",
    "I envy people who haven't met you.",
    "You're about as useful as a screen door on a submarine.",
    "You bring everyone so much joy when you leave the room.",
    "You must have been born on a highway because that's where most accidents happen.",
    "It's impossible to underestimate you.",
    "You're like a human version of a participation award.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew.",
    "I would insult you, but Mother Nature already beat me to it.",
    "I'm not a proctologist, but I know an asshole when I see one.",
    "I would love to insult you, but I'm afraid I won't do as well as nature did.",
    "You're so dumb that you got hit by a parked car.",
    "I would agree with you, but then we would both be wrong.",
    "You're a gray sprinkle on a rainbow cupcake.",
    "It's not that you are weird. It's just that everyone else is normal.",
    "I'm not saying you're stupid; you just have bad luck thinking.",
    "Is your ass jealous of the amount of shit that just came out of your mouth?",
    "If your brain was made of chocolate, it wouldn't fill an M&M.",
    "You must have been born on a highway because that's where most accidents happen.",
    "You're so dumb, you think a quarterback is a refund.",
    "If you were twice as smart, you'd still be stupid.",
    "You're not stupid; you just have bad luck when thinking.",
    "You're so ugly that even a scarecrow wouldn't scare the crows away from you.",
    "I'd give you a nasty look, but you've already got one.",
    "You're so ugly, when you look in the mirror, your reflection looks away.",
    "If your brain was made of chocolate, it wouldn't fill an M&M.",
    "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
    "You're like a human version of a participation award.",
    "You're the reason I'm not religious.",
    "If I had a dollar for every brain you don't have, I'd have one dollar.",
    "I'm not insulting you; I'm describing you.",
    "Your face is just fine, but we'll have to put a bag over that personality.",
    "You're not stupid; you just have bad luck when thinking.",
    "You're not pretty enough to have such an ugly personality.",
    "You're so ugly, even a scarecrow wouldn't scare the crows away from you.",
    "I'm not saying you're stupid; you just have bad luck thinking.",
    "I'm trying to see things from your perspective, but I can't seem to get my head that far up my ass.",
    "You must have a very low opinion of people if you think they're your equals.",
    "If you were any more stupid, you'd have to be watered twice a week.",
    "You're so ugly, when you were born, the doctor slapped your mother.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "You're the reason God created the middle finger.",
    "If ignorance is bliss, you must be the happiest person on the planet.",
    "You're not stupid; you just have bad luck when thinking.",
    "I'd slap you, but I don't want to make your face look any better.",
    "You're so ugly, you make onions cry.",
    "I don't know what makes you so stupid, but it really works.",
    "It's a shame you can't Photoshop your personality.",
    "You're not stupid; you just have bad luck when you think.",
    "You're so ugly, when you got robbed, the robbers made you wear their masks.",
    "I'm not saying you're stupid; you just have bad luck thinking.",
    "I'm trying to see things from your perspective, but I can't seem to get my head that far up my ass.",
    "I'm not a proctologist, but I know an asshole when I see one.",
    "You're the reason the gene pool needs a lifeguard.",
    "I'm not saying I hate you, but I'd unplug your life support to charge my phone.",
    "You're like a penny: two-faced and practically worthless.",
    "I don't have the time or the crayons to explain this to you.",
    "You must be a software update because not now.",
    "It's a shame you can't Photoshop your personality.",
    "I'd agree with you but then we'd both be wrong.",
    "You're impossible to underestimate.",
    "I'm not arguing, I'm just explaining why I'm right.",
    "If you were any more inbred, you'd be a sandwich.",
    "You're so ugly that even a scarecrow wouldn't scare the crows away from you.",
    "You're like a human version of a participation award.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew.",
    "I would insult you, but Mother Nature already beat me to it.",
    "I'm not a proctologist, but I know an asshole when I see one.",
    "I would love to insult you, but I'm afraid I won't do as well as nature did.",
    "You're so dumb that you got hit by a parked car.",
    "I would agree with you, but then we would both be wrong.",
    "You're a gray sprinkle on a rainbow cupcake.",
    "It's not that you are weird. It's just that everyone else is normal.",
    "I'm not saying you're stupid; you just have bad luck thinking.",
    "Is your ass jealous of the amount of shit that just came out of your mouth?",
    "If your brain was made of chocolate, it wouldn't fill an M&M.",
    "You must have been born on a highway because that's where most accidents happen.",
    "You're so dumb, you think a quarterback is a refund.",
    "If you were twice as smart, you'd still be stupid.",
    "You're not stupid; you just have bad luck when thinking.",
    "You're so ugly that even a scarecrow wouldn't scare the crows away from you.",
    "I'd give you a nasty look, but you've already got one.",
    "You're so ugly, when you look in the mirror, your reflection looks away.",
    "If your brain was made of chocolate, it wouldn't fill an M&M.",
    "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
    "You're like a human version of a participation award.",
    "You're the reason I'm not religious.",
    "If I had a dollar for every brain you don't have, I'd have one dollar.",
    "I'm not insulting you; I'm describing you.",
    "Your face is just fine, but we'll have to put a bag over that personality.",
    "You're not stupid; you just have bad luck when thinking.",
    "You're not pretty enough to have such an ugly personality.",
    "You're so ugly, even a scarecrow wouldn't scare the crows away from you.",
    "I'm not saying you're stupid; you just have bad luck thinking.",
    "I'm trying to see things from your perspective, but I can't seem to get my head that far up my ass.",
    "You must have a very low opinion of people if you think they're your equals.",
    "If you were any more stupid, you'd have to be watered twice a week.",
    "You're so ugly, when you were born, the doctor slapped your mother.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "You're the reason God created the middle finger.",
    "If ignorance is bliss, you must be the happiest person on the planet.",
    "You're not stupid; you just have bad luck when thinking.",
    "I'd slap you, but I don't want to make your face look any better.",
    "You're so ugly, you make onions cry.",
    "I don't know what makes you so stupid, but it really works.",
    "It's a shame you can't Photoshop your personality.",
    "You're not stupid; you just have bad luck when you think.",
    "You're so ugly, when you got robbed, the robbers made you wear their masks.",
    "I'm not saying you're stupid; you just have bad luck thinking.",
    "I'm trying to see things from your perspective, but I can't seem to get my head that far up my ass.",
]



server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo('Gmail')
server.starttls()
server.login(email,password)

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}



if(int(input("1. Email. 2. Phone.\n")) == 1):
    info = {
        "fromaddr": input("From Who (name)?\n"),
        "toaddrs": input("To Who (email)?\n"),
        "messageTo": input("To Who (name)?\n"),
        "messageSubject": input("Subject:\n"),
    }
    for i in range(0, int(input("How many Emails?\n"))):
        message = MIMEMultipart()
        fromaddr = info["fromaddr"]
        toaddrs = info["toaddrs"]
        message["To"] = info["messageTo"]
        message["From"] = fromaddr
        message["Subject"] = info["messageSubject"]
        title = f'<b> {message["Subject"]} </b>'
        messageText = MIMEText(f"{insults[i]}",'html')
        message.attach(messageText)
        server.sendmail(fromaddr,toaddrs,message.as_string())
else:
    info = {
        "fromaddr": "",
        "toaddrs": str(input("To Who (Phone Number)?\n")),
        "messageTo": "",
        "messageSubject": "",
        "carrier": input("What is their carrier? att, tmobile, verizon, or sprint?\n")
    }
    for i in range(0, int(input("How many Messages?\n"))):
        message = MIMEMultipart()
        fromaddr = info["fromaddr"]
        toaddrs = info["toaddrs"] + CARRIERS[info["carrier"]]
        message["To"] = info["messageTo"]
        message["From"] = fromaddr
        message["Subject"] = info["messageSubject"]
        title = f'<b> {message["Subject"]} </b>'
        messageText = MIMEText(f"{insults[i]}",'html')
        message.attach(messageText)
        server.sendmail(fromaddr,toaddrs,message.as_string())
	
server.quit()