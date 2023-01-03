import utils 

def test_convert24():
    assert "22:40" in utils.convert24("10:40 PM")
