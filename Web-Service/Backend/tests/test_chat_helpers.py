from models.pydantic_models import Message
from chat.chat_helper_functions import find_followup_or_not
def test_followup():
    m1 = Message(role="user",content = "show blue jeans")

    m2 =  Message(role = "user", content = "which of the above blue jeans looks good for hiking?")

    messages = [m1,m2]
    res = find_followup_or_not(messages=messages)
    assert res['fetch_products'] == 'No'

def test_not_followup():
    m1 = Message(role="user",content = "show blue jeans")

    messages = [m1]
    res = find_followup_or_not(messages=messages)
    assert res['fetch_products'] == 'Yes'