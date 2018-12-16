## Purpose
I was asked to draw the names for my family's secret santa and I thought: well, I can develop a program to do this. So I did.

## Getting Started

### Prerequisites
- Python 3

### Template Message
The standard templateMessage found [here](./templateMessage.txt) can be easily changed according to your will.
> Hello, ${Name}!
>
> In this year's Secret Santa gift exchange you drew ${SecretFriend}.

On line 137:
```python
        message = template.substitute(Name=name.title(), SecretFriend=secretFriendName)
```

This line is actually replacing ${Name} with name.title() and ${SecretFriend} with secretFriendName. If you want to change the standard message, you *probably* will only need to change the templateMessage.txt and this line.

You can read more about templates [here](https://www.geeksforgeeks.org/template-class-in-python/).

### Instructions
- Make sure you use an appropriate template message, you can change the `templateMessage.txt` if you want.
- Put your contacts and their e-mail in `contacts.csv` and let the program deal with it.
- Simply run ```python secretSanta.py```.

## Acknowledgments
- I used [this link](https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f) to get started with the e-mail part.
