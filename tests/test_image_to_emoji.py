import os
import unittest

from utils import File

from image_to_emoji import ImageToEmoji

DIR_TEST_INPUT = os.path.join('tests', 'test-input')
DIR_TEST_OUTPUT = os.path.join('examples')
EMOJIS = '⬛⚫🟤🟫🔴🟥🟠🟧🟡🟨🟢🟩🔵🟦🟣🟪⚪⬜'
EMOJIS_SHORT = '⚫🟤🔴🟠🟡🟢🔵🟣⚪'


class TestCase(unittest.TestCase):
    def test_get_emoji(self):
        content_list = []
        for file_name, emojis in [
            ('sri-lanka-provinces.png', '🐚⬜🥥🌊🌿🌾🌴🟧🟡🌄🏭💎🌴🟦🟣🟪⚪⬜'),
            (
                'sri-lanka-climate.jpg',
                ('⛈️', '⬜', '☀️', '🌦️', '🟡', '⬜', '🔵', '☀️', '⚪'),
            ),
            ('sri-lanka-geography.png', '🔴⬜🌳⬜🌴🗻'),
            ('sri-lanka-pres-poll-2019.png', '🔴⬜🟢🟢🔵🟣'),
            ('sri-lanka-pres-poll-2015.png', '⬜🔴🔵🟢🔵🟣'),
            ('nuuuwan.png', '⚫🔴🟤🔴⚪🔴⚫⬛⚪'),
        ]:
            image_path = os.path.join(DIR_TEST_INPUT, file_name)
            image_to_emoji = ImageToEmoji(image_path, emojis)
            actual = image_to_emoji.get_emoji()
            self.assertIsInstance(actual, str)
            content_list.append(actual)

            emoji_path = os.path.join(
                DIR_TEST_OUTPUT, file_name + '.emoji.txt'
            )
            image_to_emoji.write(emoji_path)

        lines = ['# Image To Emoji'] + content_list
        File('README.txt').write_lines(lines)
