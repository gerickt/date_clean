import unittest
from date_clean import homogenize_date


class TestDateParser(unittest.TestCase):
    def test_homogenize_date(self):
        test_cases = [
            ("1 hora", "05/08/2024 15:00"),
            ("4 horas", "05/08/2024 12:00"),
            ("1 día", "04/08/2024 16:00"),
            ("12 días", "24/07/2024 16:00"),
            ("5 de agosto, 2024 - 13:59", "05/08/2024 13:59"),
            ("05/08/2024 12:41", "05/08/2024 12:41"),
            ("05 Ago 2024, 15:14", "05/08/2024 15:14"),
            ("5 de agosto de 2024", "05/08/2024 16:00"),
            ("2024-08-05T15:57:52-04:00", "05/08/2024 15:57"),
            ("Lunes, 5 de agosto de 2024", "05/08/2024 16:00"),
            ("lun, 5 de agosto de 2024", "05/08/2024 16:00"),
        ]
        for date_str, expected in test_cases:
            with self.subTest(date_str=date_str):
                self.assertEqual(homogenize_date(
                    date_str, include_time=True, timezone="America/La_Paz"), expected)


if __name__ == '__main__':
    unittest.main()
