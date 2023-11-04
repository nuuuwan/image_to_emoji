import os
import unittest

from image_to_emoji import ImageToEmoji

DIR_TEST_INPUT = os.path.join('tests', 'test-input')
DIR_TEST_OUTPUT = os.path.join('examples')
# ⬛⚫🟤🟫🔴🟥🟠🟧🟡🟨🟢🟩🔵🟦🟣🟪⚪⬜
# ⚫🟤🔴🟠🟡🟢🔵🟣⚪


class TestCase(unittest.TestCase):
    def test_get_emoji(self):
        for file_name, emojis, max_dim in [
            ('sri-lanka-provinces.png', '🔴🟠🟡🟢🔵🟣', None),
            # ('sri-lanka-provinces.png', '🐚⬜🥥🌊🌿🌾🌴🟧🟡🌄🏭💎🌴🟦🟣🟪⚪⬜', None),
            # (
            #     'sri-lanka-climate.jpg',
            #     ('⛈️', '⬜', '☀️', '🌦️', '🟡', '⬜', '🔵', '☀️', '⚪'),
            #     None,
            # ),
            # ('sri-lanka-geography.png', '🔴⬜🌳⬜🌴🗻', None),
            # ('sri-lanka-pres-poll-2019.png', '🔴⬜🟢🟢🔵🟣', None),
            # ('sri-lanka-pres-poll-2015.png', '⬜🔴🔵🟢🔵🟣', None),
            # ('nuuuwan.png', '⚫🔴🟤🔴⚪🔴⚫⬛⚪', 15),
        ]:
            image_path = os.path.join(DIR_TEST_INPUT, file_name)
            image_to_emoji = ImageToEmoji(image_path, emojis, max_dim)
            actual = image_to_emoji.get_emoji()
            self.assertIsInstance(actual, str)

            emoji_path = os.path.join(
                DIR_TEST_OUTPUT, file_name + '.emoji.txt'
            )
            image_to_emoji.write(emoji_path)
