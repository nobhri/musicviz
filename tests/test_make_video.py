import unittest
from decimal import Decimal

from scripts.make_video import build_ffmpeg_command, build_filtergraph, format_duration


class FiltergraphTests(unittest.TestCase):
    def test_five_second_audio_uses_last_frame_index_149(self) -> None:
        filtergraph = build_filtergraph(Decimal("5.000000"))

        self.assertIn("zoompan=z='1+on/149'", filtergraph)
        self.assertIn("drawtext=", filtergraph)
        self.assertIn("showwaves=", filtergraph)

    def test_fractional_duration_rounds_frame_count_up(self) -> None:
        filtergraph = build_filtergraph(Decimal("1.01"))

        self.assertIn("zoompan=z='1+on/30'", filtergraph)


class CommandTests(unittest.TestCase):
    def test_command_preserves_verified_output_settings(self) -> None:
        command = build_ffmpeg_command(Decimal("5.000000"))

        self.assertEqual(command[-3:], ["-t", "5", "output/phase-4-python-wrapper.mp4"])
        self.assertIn("libx264", command)
        self.assertIn("aac", command)
        self.assertNotIn("shell=True", command)

    def test_duration_format_does_not_use_exponent_notation(self) -> None:
        self.assertEqual(format_duration(Decimal("0.000001")), "0.000001")


if __name__ == "__main__":
    unittest.main()
