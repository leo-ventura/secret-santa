import smtplib
import random
import time
import sys

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

def getHost():
    """
        Returns the host chosen by user
        gmail: smtp.gmail.com
        outlook: smtp-mail.outlook.com
        yahoo: smtp.mail.yahoo.com
    """
    hosts = ['smtp.gmail.com', 'smtp-mail.outlook.com', 'smtp.mail.yahoo.com']
    print("Select which e-mail provider you are using.")
    print("1) Gmail")
    print("2) Outlook")
    print("3) Yahoo")
    print("4) Other")

    answer = input()
    try:
        answer  = int(answer)

        # handling "Other" option
        if answer == 4:
            print("Enter your e-mail provider.")
            return input()

        # checking if it's in range
        elif answer > 0:
            # being user-friendly sometimes makes your code looks uglier
            # maybe I should just start at 0? I don't know.
            return hosts[answer-1]

        # if it's not in range, recursively try again
        else:
            return getHost()
    except:
        print("Please, enter a valid number!", file=sys.stderr)
        sys.exit(1)


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

def test():
    MYADDRESS = input("Your email address: ")
    PASSWORD  = input("Your password: ")

    print(MYADDRESS)
    print(PASSWORD)

    host = getHost()
    print(host)

def main():

    MYADDRESS = input("Your email address: ")
    PASSWORD  = input("Your password: ")

    host = getHost()

    # set up the SMTP server
    s = smtplib.SMTP(host=host, port=587)
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
    # main()
    test()
