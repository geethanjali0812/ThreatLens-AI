from social_monitor import monitor_social_profiles
import json
import unittest
from pathlib import Path

from app_monitor import monitor_apps


data_path = Path(__file__).resolve().parents[1] / "data" / "sample_data.json"
with data_path.open(encoding="utf-8") as file:
    sample_data = json.load(file)


class AppMonitorTests(unittest.TestCase):
    def setUp(self):
        self.brand_profile = sample_data["brands"][0]

        
        self.app_listings = [
            {
                "name": "NovaKart Shopping",
                "developer": "NovaKart Technologies",
                "description": "Shopping app",
                "store": "Google Play",
                "url": "https://example.com/official"
            },
            {
                "name": "NovaKart Shopping Security",
                "developer": "Unknown Developer",
                "description": "Shopping app",
                "store": "Google Play",
                "url": "https://example.com/suspicious"
            },
            {
                "name": "NovaKrat Shopping",
                "developer": "Unknown Developer",
                "description": "Online shopping app",
                "store": "Google Play",
                "url": "https://example.com/lookalike"
            },
            {
                "name": "Weather Today",
                "developer": "Weather Company",
                "description": "Daily weather forecasts",
                "store": "Google Play",
                "url": "https://example.com/weather"
            }
        ]

        self.findings = monitor_apps(self.brand_profile, self.app_listings)
        self.finding_names = {item["name"] for item in self.findings}

    def test_suspicious_lookalike_is_flagged(self):
        self.assertIn("NovaKart Shopping Security", self.finding_names)


    def test_official_app_is_not_flagged(self):
        self.assertNotIn("NovaKart Shopping", self.finding_names)

    def test_finding_has_score_and_reasons(self):
        finding = next(
            item for item in self.findings
            if item["name"] == "NovaKart Shopping Security"
        )
        self.assertGreaterEqual(finding["risk_score"], 30)
        self.assertTrue(finding["reasons"])

    def test_character_swap_lookalike_is_flagged(self):
        test_apps = [
            {
                "name": "NovaKrat Shopping",
                "developer": "Unknown Developer",
                "description": "Online shopping app",
                "store": "Sample data",
                "url": ""
            }
        ]
        findings = monitor_apps(self.brand_profile, test_apps)
        self.assertTrue(findings)

    def test_added_word_lookalike_is_checked(self):
        test_apps = [
            {
                "name": "NovaKart Shopping Security",
                "developer": "Unknown Developer",
                "description": "Shopping app",
                "store": "Sample data",
                "url": ""
            }
        ]
        findings = monitor_apps(self.brand_profile, test_apps)
        self.assertTrue(findings)



class SocialMonitorTests(unittest.TestCase):
    def setUp(self):
        self.brand_profile = {
            "brand_name": "ThreatLens",
            "social_accounts": {
                "Instagram": "@threatlens_official"
            }
        }

    def test_suspicious_support_profile_is_flagged(self):
        profiles = [
            {
                "name": "ThreatLens Support",
                "username": "threatlens_help",
                "platform": "Instagram",
                "url": "https://example.com/threatlens_help"
            }
        ]

        findings = monitor_social_profiles(
            self.brand_profile, profiles
        )

        self.assertTrue(findings)
        self.assertGreaterEqual(findings[0]["risk_score"], 30)

    def test_official_profile_is_excluded(self):
        profiles = [
            {
                "name": "ThreatLens",
                "username": "threatlens_official",
                "platform": "Instagram",
                "url": "https://instagram.com/threatlens_official"
            }
        ]

        findings = monitor_social_profiles(
            self.brand_profile, profiles
        )

        self.assertEqual(findings, [])

    def test_unrelated_profile_is_not_high_risk(self):
        profiles = [
            {
                "name": "Sunny Weather",
                "username": "sunnyweather123",
                "platform": "Instagram",
                "url": "https://example.com/sunnyweather123"
            }
        ]

        findings = monitor_social_profiles(
            self.brand_profile, profiles
        )

        self.assertEqual(len(findings), 1)
        self.assertNotEqual(findings[0]["risk_level"], "High")

    def test_finding_contains_explanation(self):
        profiles = [
            {
                "name": "ThreatLens Security",
                "username": "threatlens_security",
                "platform": "Instagram",
                "url": "https://example.com/threatlens_security"
            }
        ]

        findings = monitor_social_profiles(
            self.brand_profile, profiles
        )

        self.assertTrue(findings)
        self.assertTrue(findings[0]["reasons"])
        self.assertIn("risk_score", findings[0])
        self.assertIn("risk_level", findings[0])

if __name__ == "__main__":
    unittest.main()