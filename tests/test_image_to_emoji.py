import os
import unittest

from utils import File

from image_to_emoji import ImageToEmoji, pixel_to_emoji

DIR_TEST_INPUT = os.path.join('tests', 'test-input')
DIR_TEST_OUTPUT = os.path.join('examples')


class TestCase(unittest.TestCase):
    def test_get_emoji(self):
        content_list = []
        for file_name, custom_pixel_to_emoji in [
            (
                'sri-lanka-climate.jpg',
                pixel_to_emoji.for_color_groups(
                    ('🌤️', '☀️', '🌦️', '🌦️', '⛈️', '⛈️'), '⬜'
                ),
            ),
            ('sri-lanka-geography.png', pixel_to_emoji.default),
            ('sri-lanka-provinces.png', pixel_to_emoji.default),
        ]:
            image_path = os.path.join(DIR_TEST_INPUT, file_name)
            image_to_emoji = ImageToEmoji(
                image_path, custom_pixel_to_emoji=custom_pixel_to_emoji
            )
            actual = image_to_emoji.get_emoji()
            self.assertIsInstance(actual, str)
            content_list.append(actual)

            emoji_path = os.path.join(
                DIR_TEST_OUTPUT, file_name + '.emoji.txt'
            )
            image_to_emoji.write(emoji_path)

        lines = ['# Image To Emoji'] + content_list
        File('README.txt').write_lines(lines)
