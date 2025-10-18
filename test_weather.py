import unittest
from unittest.mock import patch, MagicMock
import sys
import io

# Import functions from weather.py module
from weather import kelvin_to_celsius, fetch_weather, print_daily_summary


class TestWeatherApp(unittest.TestCase):
    
    def test_kelvin_to_celsius(self):
        """Test temperature conversion from Kelvin to Celsius"""
        self.assertEqual(kelvin_to_celsius(273.15), 0.0)
        self.assertEqual(kelvin_to_celsius(300), 26.9)
        self.assertEqual(kelvin_to_celsius(0), -273.1)
        self.assertEqual(kelvin_to_celsius(373.15), 100.0)
    
    @patch('weather.requests.get')
    def test_fetch_weather_success(self, mock_get):
        """Test successful weather data fetch"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "list": [
                {
                    "dt_txt": "2025-10-18 12:00:00",
                    "main": {"temp": 293.15},
                    "weather": [{"description": "clear sky"}]
                }
            ]
        }
        mock_get.return_value = mock_response
        
        result = fetch_weather("Toronto")
        
        self.assertIsNotNone(result)
        self.assertIn("list", result)
    
    @patch('weather.requests.get')
    def test_fetch_weather_failure(self, mock_get):
        """Test failed weather data fetch (404)"""
        # Mock failed API response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = fetch_weather("InvalidCity")
        
        self.assertIsNone(result)
    
    @patch('weather.requests.get')
    def test_fetch_weather_unauthorized(self, mock_get):
        """Test unauthorized API access (401)"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        result = fetch_weather("Toronto")
        
        self.assertIsNone(result)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_daily_summary(self, mock_stdout):
        """Test daily summary printing"""
        test_data = {
            "list": [
                {
                    "dt_txt": "2025-10-18 12:00:00",
                    "main": {"temp": 293.15},
                    "weather": [{"description": "clear sky"}]
                },
                {
                    "dt_txt": "2025-10-18 15:00:00",
                    "main": {"temp": 295.15},
                    "weather": [{"description": "partly cloudy"}]
                },
                {
                    "dt_txt": "2025-10-19 12:00:00",
                    "main": {"temp": 290.15},
                    "weather": [{"description": "rainy"}]
                }
            ]
        }
        
        print_daily_summary("Toronto", test_data)
        output = mock_stdout.getvalue()
        
        self.assertIn("Weather forecast for Toronto", output)
        self.assertIn("2025-10-18", output)
        self.assertIn("20.0°C", output)
        self.assertIn("Clear sky", output)
        self.assertIn("2025-10-19", output)
        self.assertIn("17.0°C", output)
        self.assertIn("Rainy", output)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_daily_summary_filters_non_noon(self, mock_stdout):
        """Test that only 12:00:00 entries are printed"""
        test_data = {
            "list": [
                {
                    "dt_txt": "2025-10-18 09:00:00",
                    "main": {"temp": 290.15},
                    "weather": [{"description": "morning"}]
                },
                {
                    "dt_txt": "2025-10-18 12:00:00",
                    "main": {"temp": 293.15},
                    "weather": [{"description": "noon"}]
                },
                {
                    "dt_txt": "2025-10-18 18:00:00",
                    "main": {"temp": 295.15},
                    "weather": [{"description": "evening"}]
                }
            ]
        }
        
        print_daily_summary("Toronto", test_data)
        output = mock_stdout.getvalue()
        
        self.assertIn("noon", output.lower())
        self.assertNotIn("morning", output.lower())
        self.assertNotIn("evening", output.lower())
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_daily_summary_no_duplicate_dates(self, mock_stdout):
        """Test that duplicate dates are not printed"""
        test_data = {
            "list": [
                {
                    "dt_txt": "2025-10-18 12:00:00",
                    "main": {"temp": 293.15},
                    "weather": [{"description": "first"}]
                },
                {
                    "dt_txt": "2025-10-18 12:00:00",
                    "main": {"temp": 295.15},
                    "weather": [{"description": "second"}]
                }
            ]
        }
        
        print_daily_summary("Toronto", test_data)
        output = mock_stdout.getvalue()
        
        # Should only appear once
        self.assertEqual(output.count("2025-10-18"), 1)


if __name__ == '__main__':
    unittest.main()