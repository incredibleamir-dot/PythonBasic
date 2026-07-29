"""
Test cases for Python Small Basic library.
Run with: python test_smallbasic.py
"""

import os
import sys
import time
import unittest

# Add parent to path so we can import smallbasic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smallbasic import (
    Array, Clock, Desktop, File, ImageList, Keywords,
    Math, Mouse, Network, Program, Shapes,
    Sound, Stack, Text, TextWindow, Timer, Turtle
)


class TestMath(unittest.TestCase):
    """Test Math operations including fun-with-arguments patterns."""

    def test_abs(self):
        self.assertEqual(Math.Abs(-5), 5)
        self.assertEqual(Math.Abs(5), 5)
        self.assertEqual(Math.Abs(0), 0)

    def test_ceiling(self):
        self.assertEqual(Math.Ceiling(3.2), 4)
        self.assertEqual(Math.Ceiling(-3.2), -3)

    def test_floor(self):
        self.assertEqual(Math.Floor(3.7), 3)
        self.assertEqual(Math.Floor(-3.7), -4)

    def test_sin_cos_tan(self):
        self.assertAlmostEqual(Math.Sin(0), 0, places=5)
        self.assertAlmostEqual(Math.Cos(0), 1, places=5)
        self.assertAlmostEqual(Math.Tan(0), 0, places=5)

    def test_arcsin_arccos_arctan(self):
        self.assertAlmostEqual(Math.ArcSin(0), 0, places=5)
        self.assertAlmostEqual(Math.ArcCos(1), 0, places=5)
        self.assertAlmostEqual(Math.ArcTan(0), 0, places=5)

    def test_square_root(self):
        self.assertEqual(Math.SquareRoot(9), 3)
        self.assertEqual(Math.SquareRoot(0), 0)

    def test_power(self):
        self.assertEqual(Math.Power(2, 3), 8)
        self.assertEqual(Math.Power(5, 0), 1)

    def test_round(self):
        self.assertEqual(Math.Round(3.4), 3)
        self.assertEqual(Math.Round(3.6), 4)

    def test_max_with_two_args(self):
        """Max with 2 arguments (traditional)."""
        self.assertEqual(Math.Max(10, 20), 20)

    def test_max_with_multiple_args(self):
        """Max with many arguments (fun with args)."""
        self.assertEqual(Math.Max(10, 20, 5, 30, 15), 30)

    def test_min_with_multiple_args(self):
        """Min with many arguments (fun with args)."""
        self.assertEqual(Math.Min(10, 20, 5, 30, 15), 5)

    def test_sum_with_args(self):
        """Sum using *args (fun with args)."""
        self.assertEqual(Math.Sum(1, 2, 3, 4, 5), 15)
        self.assertEqual(Math.Sum(10, 20), 30)
        self.assertEqual(Math.Sum(), 0)

    def test_average_with_args(self):
        """Average using *args (fun with args)."""
        self.assertEqual(Math.Average(10, 20, 30), 20)
        self.assertAlmostEqual(Math.Average(1, 2), 1.5)

    def test_get_random_number(self):
        for _ in range(100):
            n = Math.GetRandomNumber(10)
            self.assertGreaterEqual(n, 1)
            self.assertLessEqual(n, 10)

    def test_pi(self):
        self.assertAlmostEqual(Math.Pi, 3.141592653589793, places=5)

    def test_remainder(self):
        self.assertEqual(Math.Remainder(10, 3), 1)
        self.assertEqual(Math.Remainder(10, 5), 0)

    def test_log(self):
        self.assertAlmostEqual(Math.Log(100), 2, places=5)
        import math
        self.assertAlmostEqual(Math.NaturalLog(math.e), 1, places=5)

    def test_degrees_radians(self):
        self.assertAlmostEqual(Math.GetDegrees(3.14159), 180, places=2)
        self.assertAlmostEqual(Math.GetRadians(180), 3.14159, places=2)


class TestText(unittest.TestCase):
    """Test Text operations."""

    def test_append(self):
        self.assertEqual(Text.Append("Hello", " World"), "Hello World")
        self.assertEqual(Text.Append("", "Test"), "Test")

    def test_get_length(self):
        self.assertEqual(Text.GetLength("Hello"), 5)
        self.assertEqual(Text.GetLength(""), 0)

    def test_is_subtext(self):
        self.assertTrue(Text.IsSubText("Hello World", "World"))
        self.assertFalse(Text.IsSubText("Hello", "xyz"))

    def test_ends_with(self):
        self.assertTrue(Text.EndsWith("Hello.py", ".py"))
        self.assertFalse(Text.EndsWith("Hello.py", ".txt"))

    def test_starts_with(self):
        self.assertTrue(Text.StartsWith("Hello World", "Hello"))
        self.assertFalse(Text.StartsWith("Hello World", "World"))

    def test_get_subtext(self):
        self.assertEqual(Text.GetSubText("Hello World", 1, 5), "Hello")
        self.assertEqual(Text.GetSubText("Hello", 3, 2), "ll")

    def test_get_subtext_to_end(self):
        self.assertEqual(Text.GetSubTextToEnd("Hello World", 7), "World")

    def test_get_index_of(self):
        self.assertEqual(Text.GetIndexOf("Hello World", "World"), 7)
        self.assertEqual(Text.GetIndexOf("Hello", "xyz"), 0)

    def test_case_conversion(self):
        self.assertEqual(Text.ConvertToUpperCase("hello"), "HELLO")
        self.assertEqual(Text.ConvertToLowerCase("HELLO"), "hello")

    def test_character_codes(self):
        self.assertEqual(Text.GetCharacter(65), "A")
        self.assertEqual(Text.GetCharacterCode("A"), 65)
        self.assertEqual(Text.GetCharacterCode("!"), 33)


class TestArray(unittest.TestCase):
    """Test Array operations."""

    def setUp(self):
        # Clear the internal stores
        Array._stores.clear()

    def test_set_and_get(self):
        Array.SetValue("test", "key1", "value1")
        self.assertEqual(Array.GetValue("test", "key1"), "value1")

    def test_contains_index(self):
        Array.SetValue("test", "name", "John")
        self.assertTrue(Array.ContainsIndex("test", "name"))
        self.assertFalse(Array.ContainsIndex("test", "nonexistent"))

    def test_contains_value(self):
        Array.SetValue("test", "x", 42)
        self.assertTrue(Array.ContainsValue("test", 42))
        self.assertFalse(Array.ContainsValue("test", 99))

    def test_get_item_count(self):
        Array.SetValue("test", "a", 1)
        Array.SetValue("test", "b", 2)
        Array.SetValue("test", "c", 3)
        self.assertEqual(Array.GetItemCount("test"), 3)

    def test_is_array(self):
        self.assertTrue(Array.IsArray({}))
        self.assertTrue(Array.IsArray([]))
        self.assertFalse(Array.IsArray("string"))
        self.assertFalse(Array.IsArray(42))

    def test_remove_value(self):
        Array.SetValue("test", "key", "val")
        Array.RemoveValue("test", "key")
        self.assertEqual(Array.GetValue("test", "key"), "")

    def test_get_all_indices(self):
        Array.SetValue("test", "a", 1)
        Array.SetValue("test", "b", 2)
        indices = Array.GetAllIndices("test")
        self.assertIn("a", indices.values())
        self.assertIn("b", indices.values())


class TestStack(unittest.TestCase):
    """Test Stack operations."""

    def setUp(self):
        Stack._stacks.clear()

    def test_push_and_pop(self):
        Stack.PushValue("s", "first")
        Stack.PushValue("s", "second")
        self.assertEqual(Stack.PopValue("s"), "second")
        self.assertEqual(Stack.PopValue("s"), "first")

    def test_pop_empty(self):
        self.assertEqual(Stack.PopValue("empty"), "")

    def test_get_count(self):
        self.assertEqual(Stack.GetCount("s"), 0)
        Stack.PushValue("s", "item")
        self.assertEqual(Stack.GetCount("s"), 1)


class TestClock(unittest.TestCase):
    """Test Clock properties."""

    def test_time_format(self):
        self.assertRegex(Clock.Time, r"\d{2}:\d{2}:\d{2}")

    def test_date_format(self):
        self.assertRegex(Clock.Date, r"\d{2}/\d{2}/\d{4}")

    def test_year(self):
        self.assertEqual(Clock.Year, 2026)

    def test_month_range(self):
        self.assertGreaterEqual(Clock.Month, 1)
        self.assertLessEqual(Clock.Month, 12)

    def test_day_range(self):
        self.assertGreaterEqual(Clock.Day, 1)
        self.assertLessEqual(Clock.Day, 31)

    def test_hour_range(self):
        self.assertGreaterEqual(Clock.Hour, 0)
        self.assertLessEqual(Clock.Hour, 23)

    def test_elapsed_milliseconds(self):
        self.assertGreater(Clock.ElapsedMilliseconds, 0)


class TestTextWindow(unittest.TestCase):
    """Test TextWindow operations."""

    def test_write_line_with_args(self):
        """TextWindow.WriteLine with multiple args (fun with args)."""
        TextWindow.Show()
        TextWindow.WriteLine("a", "b", "c")
        TextWindow.Hide()

    def test_foreground_color(self):
        original = TextWindow.ForegroundColor
        TextWindow.ForegroundColor = "Red"
        self.assertEqual(TextWindow.ForegroundColor, "Red")
        TextWindow.ForegroundColor = original


class TestNetwork(unittest.TestCase):
    """Test Network REST API."""

    def test_get_webpage(self):
        result = Network.GetWebPageContents("https://jsonplaceholder.typicode.com/todos/1")
        self.assertIn("userId", result)
        self.assertIn("title", result)

    def test_rest_get(self):
        result = Network.Get("https://jsonplaceholder.typicode.com/posts/1")
        self.assertIn("id", result)

    def test_rest_post(self):
        result = Network.Post(
            "https://jsonplaceholder.typicode.com/posts",
            {"title": "test", "body": "test body", "userId": 1}
        )
        self.assertIn("test", result)

    def test_rest_put(self):
        result = Network.Put(
            "https://jsonplaceholder.typicode.com/posts/1",
            {"title": "updated", "body": "updated body", "userId": 1}
        )
        self.assertIn("updated", result)

    def test_rest_delete(self):
        result = Network.Delete("https://jsonplaceholder.typicode.com/posts/1")
        self.assertIn("{}", result)


class TestProgram(unittest.TestCase):
    """Test Program operations."""

    def test_argument_count(self):
        self.assertGreaterEqual(Program.ArgumentCount, 0)

    def test_directory(self):
        self.assertTrue(os.path.isdir(Program.Directory))

    def test_get_argument(self):
        self.assertEqual(Program.GetArgument(0), "")

    def test_delay(self):
        start = time.time()
        Program.Delay(100)
        elapsed = time.time() - start
        self.assertGreaterEqual(elapsed, 0.09)


class TestDesktop(unittest.TestCase):
    """Test Desktop properties."""

    def test_width(self):
        self.assertGreater(Desktop.Width, 0)

    def test_height(self):
        self.assertGreater(Desktop.Height, 0)


class TestFile(unittest.TestCase):
    """Test File operations."""

    def setUp(self):
        self.test_file = "test_smallbasic_temp.txt"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_and_read(self):
        result = File.WriteContents(self.test_file, "Hello World")
        self.assertEqual(result, "SUCCESS")
        contents = File.ReadContents(self.test_file)
        self.assertEqual(contents, "Hello World")

    def test_append(self):
        File.WriteContents(self.test_file, "Line 1")
        File.AppendContents(self.test_file, "Line 2")
        contents = File.ReadContents(self.test_file)
        self.assertIn("Line 2", contents)

    def test_get_temporary_path(self):
        path = File.GetTemporaryFilePath()
        self.assertTrue(os.path.exists(os.path.dirname(path)))

    def test_copy_file(self):
        File.WriteContents(self.test_file, "Original")
        dest = "test_smallbasic_copy.txt"
        result = File.CopyFile(self.test_file, dest)
        self.assertEqual(result, "SUCCESS")
        self.assertTrue(os.path.exists(dest))
        if os.path.exists(dest):
            os.remove(dest)


class TestSound(unittest.TestCase):
    """Test Sound operations."""

    def test_play_click(self):
        Sound.PlayClick()

    def test_play_chime(self):
        Sound.PlayChime()

    def test_play_bell(self):
        Sound.PlayBellRing()


class TestTimer(unittest.TestCase):
    """Test Timer operations."""

    def test_pause_resume(self):
        Timer.Interval = 100
        Timer.Resume()
        Program.Delay(250)
        Timer.Pause()


class TestKeywords(unittest.TestCase):
    """Test Keywords docstring."""

    def test_keywords_class_exists(self):
        self.assertIsNotNone(Keywords)


if __name__ == "__main__":
    unittest.main(verbosity=2)
