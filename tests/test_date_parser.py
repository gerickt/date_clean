import unittest
from datetime import datetime, timedelta
from date_clean import homogenize_date
import pytz


class TestDateParser(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(pytz.timezone(
            "America/La_Paz")).replace(second=0, microsecond=0)

    def test_homogenize_date(self):
        # Formato: ("Entrada", "Salida esperada")
        test_cases = [
            ("1 hora", (self.now - timedelta(hours=1)).isoformat()),
            ("4 horas", (self.now - timedelta(hours=4)).isoformat()),
            ("1 día", (self.now - timedelta(days=1)).isoformat()),
            ("12 días", (self.now - timedelta(days=12)).isoformat()),
            ("5 de agosto, 2024 - 13:59", "2024-08-05T13:59:00-04:00"),
            ("05/08/2024 12:41", "2024-08-05T12:41:00-04:00"),
            ("05 Ago 2024, 15:14", "2024-08-05T15:14:00-04:00"),
            ("5 de agosto de 2024", "2024-08-05T" +
             self.now.strftime("%H:%M:00") + "-04:00"),
            ("2024-08-05T15:57:52-04:00", "2024-08-05T15:57:00-04:00"),
            ("Lunes, 5 de agosto de 2024", "2024-08-05T" +
             self.now.strftime("%H:%M:00") + "-04:00"),
            ("lun, 5 de agosto de 2024", "2024-08-05T" +
             self.now.strftime("%H:%M:00") + "-04:00"),
        ]

        for date_str, expected in test_cases:
            with self.subTest(date_str=date_str):
                result = homogenize_date(
                    date_str, include_time=True, timezone="America/La_Paz")
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
