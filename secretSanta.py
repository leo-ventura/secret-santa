import smtplib
import random
import time

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def getInfo(filename):
    """
        Returns names and emails stored in a csv file specified by filename
    """

    names  = []
    emails = []

    with open(filename, mode='r', encoding='utf-8') as contactsFile:
        for contact in contactsFile:
            info = contact.split(',')
            names.append(info[0])           # name
            emails.append(info[1])          # email
    return names, emails

def parseTemplate(filename):
    """
        Returns a Template object using the file specified by filename
    """

    with open(filename, 'r', encoding='utf-8') as templateFile:
        content = templateFile.read()
    return Template(content)


def getSecretFriend(names, currentName, taken):
    """
        Returns a random secret friend
        Recursively iterate until it finds a good match
    """

    # getting a list with those who haven't been chosen yet
    possibleCandidates = []
    for _name in names:
        if _name not in taken:
            possibleCandidates.append(_name)

    secretID = random.randint(0,len(possibleCandidates)-1)

    if possibleCandidates[secretID] == currentName:
        return getSecretFriend(names, currentName, taken)
    return possibleCandidates[secretID]


def main():

    MYADDRESS = ""
    PASSWORD  = ""

    # set up the SMTP server
    s = smtplib.SMTP(host=insertHostHere, port=insertPortHere)
    s.starttls()
    s.login(MYADDRESS, PASSWORD)

    names, emails = getInfo("contacts.csv")

    template = parseTemplate("templateMessage.txt")

    alreadyChosen = []
    taken = []

    for _ in range(len(names)-1):
        # draws a randomID
        randomID = random.randint(0,len(names)-1)

        # trying to find an unchosen name
        # (a little inneficient I know, but it does the trick and it's randomized)
        while names[randomID] in alreadyChosen:
            randomID = random.randint(0,len(names)-1)

        # assigning name and email
        name  = names[randomID]
        email = emails[randomID]

        # then adds it to the list of already chosen names
        alreadyChosen.append(name)

        # finds a secret friend to that person
        secretFriendName = getSecretFriend(names, name, taken)

        # then adds it to the list of already taken names
        taken.append(secretFriendName)

        # creates a message
        msg = MIMEMultipart()

        # uses the template to assemble our message together
        message = template.substitute(Name=name.title(), SecretFriend=secretFriendName)

        # setup the parameters of the message
        msg['From']    = MYADDRESS
        msg['To']      = email
        msg['Subject'] = "Secret Santa"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # sends the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # terminates the SMTP session and closes the connection
    s.quit()


if __name__ == '__main__':
    main()
