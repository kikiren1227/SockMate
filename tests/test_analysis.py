from core.analysis import map_user_to_socks

def test_map_user_to_socks():
    user_tags = {
        'gender': 'male',
        'style': '运动',
        'vibe': '活力四射',
        'color_palette': 'red, yellow, green, lavender'
    }

    socks_tags = map_user_to_socks(user_tags)
    print(socks_tags)