from cart.user_cart_handler import get_user_cart_products
from models.pydantic_models import Message, Product,CartBotReq
from cart.cart_chat_handler import answer_questions_for_cart
def test_non_empty_cart():
    products = get_user_cart_products(1)
    assert len(products) > 0

def test_cart_response():
    m1 = Message(role="user",content = "does jeans suit my shirt?")
    messages = [m1]
    p1 = Product(title= "jeans", imageURLHighRes= "str", category= "men_clothing", asin = "a1", summary= "men blue jeans")
    p2 = Product(title= "shirts", imageURLHighRes= "str", category= "men_clothing", asin = "a1", summary= "men white shirts")

    products = [p1,p2]
    req = CartBotReq(messages = messages, products = products)
    res = answer_questions_for_cart(cartReq=req)
    assert len(res['response']['bot']) > 0
