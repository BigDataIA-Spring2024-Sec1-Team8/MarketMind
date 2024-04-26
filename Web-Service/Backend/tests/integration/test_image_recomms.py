from image_search.search_image import retrieve_products_by_image

def test_products_retreival():
    pro_res = retrieve_products_by_image('resources/img.jpg')
    assert len(pro_res['response']) > 0