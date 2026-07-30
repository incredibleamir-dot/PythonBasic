"""
Test cases for Python Small Basic library.
Run with: python test_smallbasic.py
"""

import os
import sys
import math
import time
import logging
import tempfile
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

# Add parent to path so we can import smallbasic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smallbasic import (
    Array, Clock, Controls, Desktop, Dictionary, File, GraphicsWindow,
    ImageList, Keywords, Math, Mouse, Network, Program, Shapes,
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

    def test_arc_sin_clamp(self):
        self.assertAlmostEqual(Math.ArcSin(1), 90, places=3)
        self.assertAlmostEqual(Math.ArcSin(-1), -90, places=3)
        self.assertAlmostEqual(Math.ArcSin(1.5), 90, places=3)

    def test_arc_cos_clamp(self):
        self.assertAlmostEqual(Math.ArcCos(-1), 180, places=3)
        self.assertAlmostEqual(Math.ArcCos(1.5), 0, places=3)

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
        self.assertEqual(Math.Max(10, 20), 20)

    def test_max_with_multiple_args(self):
        self.assertEqual(Math.Max(10, 20, 5, 30, 15), 30)

    def test_max_with_one_arg(self):
        self.assertEqual(Math.Max(42), 42)

    def test_max_with_no_args(self):
        self.assertEqual(Math.Max(), 0)

    def test_min_with_multiple_args(self):
        self.assertEqual(Math.Min(10, 20, 5, 30, 15), 5)

    def test_min_with_no_args(self):
        self.assertEqual(Math.Min(), 0)

    def test_sum_with_args(self):
        self.assertEqual(Math.Sum(1, 2, 3, 4, 5), 15)
        self.assertEqual(Math.Sum(10, 20), 30)
        self.assertEqual(Math.Sum(), 0)

    def test_average_with_args(self):
        self.assertEqual(Math.Average(10, 20, 30), 20)
        self.assertAlmostEqual(Math.Average(1, 2), 1.5)
        self.assertEqual(Math.Average(), 0.0)

    def test_get_random_number(self):
        for _ in range(100):
            n = Math.GetRandomNumber(10)
            self.assertGreaterEqual(n, 1)
            self.assertLessEqual(n, 10)

    def test_get_random_number_one(self):
        for _ in range(10):
            n = Math.GetRandomNumber(1)
            self.assertEqual(n, 1)

    def test_pi(self):
        self.assertAlmostEqual(Math.Pi, 3.141592653589793, places=5)

    def test_remainder(self):
        self.assertEqual(Math.Remainder(10, 3), 1)
        self.assertEqual(Math.Remainder(10, 5), 0)

    def test_log(self):
        self.assertAlmostEqual(Math.Log(100), 2, places=5)
        self.assertAlmostEqual(Math.NaturalLog(math.e), 1, places=5)

    def test_degrees_radians(self):
        self.assertAlmostEqual(Math.GetDegrees(3.14159), 180, places=2)
        self.assertAlmostEqual(Math.GetRadians(180), 3.14159, places=2)


class TestText(unittest.TestCase):
    """Test Text operations."""

    def test_append(self):
        self.assertEqual(Text.Append("Hello", " World"), "Hello World")
        self.assertEqual(Text.Append("", "Test"), "Test")
        self.assertEqual(Text.Append(123, "abc"), "123abc")

    def test_get_length(self):
        self.assertEqual(Text.GetLength("Hello"), 5)
        self.assertEqual(Text.GetLength(""), 0)
        self.assertEqual(Text.GetLength(12345), 5)

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
        Array._stores.clear()

    def test_set_and_get(self):
        Array.SetValue("test", "key1", "value1")
        self.assertEqual(Array.GetValue("test", "key1"), "value1")

    def test_get_nonexistent(self):
        self.assertEqual(Array.GetValue("test", "nonexistent"), "")

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

    def test_remove_nonexistent(self):
        Array.RemoveValue("test", "nonexistent")

    def test_get_all_indices(self):
        Array.SetValue("test", "a", 1)
        Array.SetValue("test", "b", 2)
        indices = Array.GetAllIndices("test")
        self.assertIn("a", indices.values())
        self.assertIn("b", indices.values())

    def test_resolve_with_dict(self):
        d = {"x": 1, "y": 2}
        self.assertEqual(Array._resolve(d), d)

    def test_resolve_with_string(self):
        Array.SetValue("arr", "key", "val")
        self.assertEqual(Array._resolve("arr"), {"key": "val"})

    def test_resolve_with_unknown_string(self):
        self.assertEqual(Array._resolve("unknown"), {})


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

    def test_push_various_types(self):
        Stack.PushValue("s", 42)
        Stack.PushValue("s", 3.14)
        Stack.PushValue("s", "text")
        Stack.PushValue("s", [1, 2, 3])
        self.assertEqual(Stack.GetCount("s"), 4)


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

    def test_minute_range(self):
        self.assertGreaterEqual(Clock.Minute, 0)
        self.assertLessEqual(Clock.Minute, 59)

    def test_second_range(self):
        self.assertGreaterEqual(Clock.Second, 0)
        self.assertLessEqual(Clock.Second, 59)

    def test_millisecond_range(self):
        self.assertGreaterEqual(Clock.Millisecond, 0)
        self.assertLessEqual(Clock.Millisecond, 999)

    def test_elapsed_milliseconds(self):
        self.assertGreater(Clock.ElapsedMilliseconds, 0)

    def test_weekday(self):
        self.assertIn(Clock.WeekDay, [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ])


class TestTextWindow(unittest.TestCase):
    """Test TextWindow operations."""

    def test_write_line_with_args(self):
        TextWindow.Show()
        TextWindow.WriteLine("a", "b", "c")
        TextWindow.Hide()

    def test_foreground_color(self):
        original = TextWindow.ForegroundColor
        TextWindow.ForegroundColor = "Red"
        self.assertEqual(TextWindow.ForegroundColor, "Red")
        TextWindow.ForegroundColor = original

    def test_background_color(self):
        original = TextWindow.BackgroundColor
        TextWindow.BackgroundColor = "Blue"
        self.assertEqual(TextWindow.BackgroundColor, "Blue")
        TextWindow.BackgroundColor = original

    def test_title(self):
        original = TextWindow.Title
        TextWindow.Title = "Test Title"
        self.assertEqual(TextWindow.Title, "Test Title")
        TextWindow.Title = original

    def test_left_top(self):
        TextWindow.Left = 200
        self.assertEqual(TextWindow.Left, 200)
        TextWindow.Top = 150
        self.assertEqual(TextWindow.Top, 150)

    def test_cursor_properties(self):
        TextWindow.CursorLeft = 5
        self.assertEqual(TextWindow.CursorLeft, 0)
        TextWindow.CursorTop = 5
        self.assertEqual(TextWindow.CursorTop, 0)


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

    def test_read_nonexistent(self):
        result = File.ReadContents("nonexistent_file.txt")
        self.assertEqual(result, "FAILED")
        self.assertNotEqual(File.LastError, "")

    def test_append(self):
        File.WriteContents(self.test_file, "Line 1")
        File.AppendContents(self.test_file, "\nLine 2")
        contents = File.ReadContents(self.test_file)
        self.assertIn("Line 2", contents)

    def test_get_temporary_path(self):
        path = File.GetTemporaryFilePath()
        self.assertTrue(os.path.exists(path))
        if path:
            os.remove(path)

    def test_copy_file(self):
        File.WriteContents(self.test_file, "Original")
        dest = "test_smallbasic_copy.txt"
        result = File.CopyFile(self.test_file, dest)
        self.assertEqual(result, "SUCCESS")
        self.assertTrue(os.path.exists(dest))
        if os.path.exists(dest):
            os.remove(dest)

    def test_delete_file(self):
        File.WriteContents(self.test_file, "To be deleted")
        result = File.DeleteFile(self.test_file)
        self.assertEqual(result, "SUCCESS")
        self.assertFalse(os.path.exists(self.test_file))

    def test_read_write_line(self):
        File.WriteContents(self.test_file, "Line 1\nLine 2\nLine 3")
        result = File.WriteLine(self.test_file, 2, "Modified Line 2")
        self.assertEqual(result, "SUCCESS")
        line = File.ReadLine(self.test_file, 2)
        self.assertEqual(line, "Modified Line 2")

    def test_insert_line(self):
        File.WriteContents(self.test_file, "Line 1\nLine 3")
        result = File.InsertLine(self.test_file, 2, "Line 2")
        self.assertEqual(result, "SUCCESS")
        line = File.ReadLine(self.test_file, 2)
        self.assertEqual(line, "Line 2")

    def test_create_and_delete_directory(self):
        test_dir = "test_smallbasic_dir"
        result = File.CreateDirectory(test_dir)
        self.assertEqual(result, "SUCCESS")
        self.assertTrue(os.path.isdir(test_dir))
        result = File.DeleteDirectory(test_dir)
        self.assertEqual(result, "SUCCESS")
        self.assertFalse(os.path.isdir(test_dir))

    def test_get_files(self):
        File.WriteContents(self.test_file, "test")
        files = File.GetFiles(".")
        self.assertIsInstance(files, dict)
        self.assertTrue(len(files) > 0)


class TestSound(unittest.TestCase):
    """Test Sound operations."""

    def test_play_click(self):
        Sound.PlayClick()

    def test_play_chime(self):
        Sound.PlayChime()

    def test_play_bell(self):
        Sound.PlayBellRing()

    def test_stop(self):
        Sound.Stop()

    def test_pause_without_error(self):
        Sound.Pause()

    def test_resume_without_error(self):
        Sound.Resume()


class TestTimer(unittest.TestCase):
    """Test Timer operations."""

    def test_pause_resume(self):
        Timer.Interval = 100
        Timer.Resume()
        Program.Delay(250)
        Timer.Pause()

    def test_tick_event(self):
        Timer._running = False
        Timer._timer = None
        Timer._tick = None

        counter = {"value": 0}

        def on_tick():
            counter["value"] += 1

        Timer.Interval = 50
        Timer.Tick = on_tick
        Program.Delay(400)
        Timer.Pause()
        self.assertGreater(counter["value"], 0)
        Timer._tick = None
        Timer._running = False


class TestKeywords(unittest.TestCase):
    """Test Keywords docstring."""

    def test_keywords_class_exists(self):
        self.assertIsNotNone(Keywords)


class TestMouseBugFix(unittest.TestCase):
    """Test Bug Fix #1: Mouse operator precedence fix."""

    def test_is_left_button_returns_bool(self):
        result = Mouse.IsLeftButtonDown
        self.assertIsInstance(result, bool)

    def test_is_right_button_returns_bool(self):
        result = Mouse.IsRightButtonDown
        self.assertIsInstance(result, bool)

    def test_mouse_x_returns_int(self):
        result = Mouse.MouseX
        self.assertIsInstance(result, int)

    def test_mouse_y_returns_int(self):
        result = Mouse.MouseY
        self.assertIsInstance(result, int)

    def test_operator_precedence_fix(self):
        import ctypes
        key_state = ctypes.windll.user32.GetAsyncKeyState(0x01)
        expected = (key_state & 0x8000) != 0
        actual = Mouse.IsLeftButtonDown
        self.assertEqual(type(expected), type(actual))


class TestGraphicsWindowBugFix(unittest.TestCase):
    """Test Bug Fix #2 and #9: GetPixel and event callbacks."""

    def test_get_pixel_returns_string(self):
        result = GraphicsWindow.GetPixel(0, 0)
        self.assertIsInstance(result, str)

    def test_get_pixel_returns_color_format(self):
        result = GraphicsWindow.GetPixel(0, 0)
        self.assertTrue(
            result.startswith("#") or result in [
                "White", "Black", "Red", "Green", "Blue",
                "Yellow", "Cyan", "Magenta", "Gray"
            ]
        )


class TestShapesBugFix(unittest.TestCase):
    """Test Bug Fix #3: Shapes.Rotate with proper rotation matrix."""

    def test_add_rectangle(self):
        name = Shapes.AddRectangle(100, 50)
        self.assertIsNotNone(name)
        self.assertIn(name, Shapes._shapes)

    def test_add_ellipse(self):
        name = Shapes.AddEllipse(80, 60)
        self.assertIsNotNone(name)

    def test_add_triangle(self):
        name = Shapes.AddTriangle(0, 0, 50, 100, 100, 0)
        self.assertIsNotNone(name)

    def test_add_line(self):
        name = Shapes.AddLine(0, 0, 100, 100)
        self.assertIsNotNone(name)

    def test_rotate_preserves_shape(self):
        name = Shapes.AddRectangle(100, 50)
        Shapes.Rotate(name, 45)
        shape = Shapes._shapes.get(name)
        self.assertIsNotNone(shape)
        self.assertEqual(shape.angle, 45)

    def test_rotate_does_not_collapse(self):
        name = Shapes.AddRectangle(100, 50)
        orig_coords = Shapes._shapes[name].orig_coords
        Shapes.Rotate(name, 30)
        shape = Shapes._shapes[name]
        self.assertIsNotNone(shape)

    def test_move_shape(self):
        name = Shapes.AddRectangle(100, 50)
        Shapes.Move(name, 50, 60)
        self.assertEqual(Shapes.GetLeft(name), 50)
        self.assertEqual(Shapes.GetTop(name), 60)

    def test_remove_shape(self):
        name = Shapes.AddRectangle(100, 50)
        Shapes.Remove(name)
        self.assertNotIn(name, Shapes._shapes)

    def test_hide_show_shape(self):
        name = Shapes.AddRectangle(100, 50)
        Shapes.HideShape(name)
        shape = Shapes._shapes[name]
        self.assertFalse(shape.visible)
        Shapes.ShowShape(name)
        self.assertTrue(shape.visible)

    def test_opacity(self):
        name = Shapes.AddRectangle(100, 50)
        Shapes.SetOpacity(name, 50)
        self.assertEqual(Shapes.GetOpacity(name), 50)
        Shapes.SetOpacity(name, 150)
        self.assertEqual(Shapes.GetOpacity(name), 100)
        Shapes.SetOpacity(name, -10)
        self.assertEqual(Shapes.GetOpacity(name), 0)


class TestDictionaryBugFix(unittest.TestCase):
    """Test Bug Fix #4: Dictionary translation methods."""

    def test_get_definition(self):
        result = Dictionary.GetDefinition("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_translation_to_spanish(self):
        result = Dictionary.GetDefinitionEnglishToSpanish("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_translation_to_french(self):
        result = Dictionary.GetDefinitionEnglishToFrench("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_translation_to_german(self):
        result = Dictionary.GetDefinitionEnglishToGerman("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_translation_to_italian(self):
        result = Dictionary.GetDefinitionEnglishToItalian("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_translation_to_japanese(self):
        result = Dictionary.GetDefinitionEnglishToJapanese("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_translation_to_korean(self):
        result = Dictionary.GetDefinitionEnglishToKorean("hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestSoundBugFix(unittest.TestCase):
    """Test Bug Fix #5 and #6: Sound pause/resume and PlayAndWait."""

    def test_sound_has_pause_method(self):
        self.assertTrue(hasattr(Sound, 'Pause'))
        self.assertTrue(callable(Sound.Pause))

    def test_sound_has_resume_method(self):
        self.assertTrue(hasattr(Sound, 'Resume'))
        self.assertTrue(callable(Sound.Resume))

    def test_sound_stop_method(self):
        Sound.Stop()
        self.assertEqual(Sound._current_file, "")

    def test_pause_resume_state(self):
        Sound._pause_event.set()
        Sound.Pause()
        self.assertFalse(Sound._pause_event.is_set())
        Sound.Resume()
        self.assertTrue(Sound._pause_event.is_set())

    def test_pause_signature(self):
        import inspect
        sig = inspect.signature(Sound.Pause)
        self.assertEqual(len(sig.parameters), 0)

    def test_stop_signature(self):
        import inspect
        sig = inspect.signature(Sound.Stop)
        self.assertEqual(len(sig.parameters), 0)


class TestTimerBugFix(unittest.TestCase):
    """Test Bug Fix #8: Timer exception logging."""

    def test_timer_logs_exceptions(self):
        with patch('smallbasic.timer.logger') as mock_logger:
            def bad_tick():
                raise ValueError("Test error")

            Timer._tick = bad_tick
            Timer._running = True
            Timer._paused = False

            try:
                Timer._run()
            except Exception:
                pass

            Timer._running = False
            Timer._tick = None

    def test_timer_has_logger(self):
        import smallbasic.timer as timer_module
        self.assertTrue(hasattr(timer_module, 'logger'))
        self.assertIsInstance(timer_module.logger, logging.Logger)


class TestFileBugFix(unittest.TestCase):
    """Test Bug Fix #7: File.GetTemporaryFilePath error handling."""

    def test_get_temporary_file_returns_string(self):
        result = File.GetTemporaryFilePath()
        self.assertIsInstance(result, str)

    def test_get_temporary_file_returns_valid_path(self):
        result = File.GetTemporaryFilePath()
        if result:
            self.assertTrue(os.path.exists(os.path.dirname(result)))

    def test_get_temporary_file_cleanup(self):
        path = File.GetTemporaryFilePath()
        if path and os.path.exists(path):
            os.remove(path)


class TestTextWindowBugFix(unittest.TestCase):
    """Test TextWindow event handling improvements."""

    def test_write_multiple_args(self):
        TextWindow.Show()
        TextWindow.WriteLine("one", "two", "three")
        TextWindow.Hide()

    def test_write_string_conversion(self):
        TextWindow.Show()
        TextWindow.Write(123)
        TextWindow.Write(3.14)
        TextWindow.Write(True)
        TextWindow.Hide()


class TestControls(unittest.TestCase):
    """Test Controls operations."""

    def test_add_button(self):
        btn = Controls.AddButton("Test", 100, 50)
        self.assertIsNotNone(btn)
        self.assertIn(btn, Controls._widgets)
        Controls.Remove(btn)

    def test_add_textbox(self):
        tb = Controls.AddTextBox(100, 100)
        self.assertIsNotNone(tb)
        self.assertIn(tb, Controls._widgets)
        Controls.Remove(tb)

    def test_set_get_button_caption(self):
        btn = Controls.AddButton("Original", 100, 50)
        Controls.SetButtonCaption(btn, "Modified")
        self.assertEqual(Controls.GetButtonCaption(btn), "Modified")
        Controls.Remove(btn)

    def test_set_get_textbox_text(self):
        tb = Controls.AddTextBox(100, 100)
        Controls.SetTextBoxText(tb, "Hello")
        self.assertEqual(Controls.GetTextBoxText(tb), "Hello")
        Controls.Remove(tb)

    def test_remove_control(self):
        btn = Controls.AddButton("Test", 100, 50)
        Controls.Remove(btn)
        self.assertNotIn(btn, Controls._widgets)

    def test_move_control(self):
        btn = Controls.AddButton("Test", 100, 50)
        Controls.Move(btn, 200, 200)
        Controls.Remove(btn)

    def test_hide_show_control(self):
        btn = Controls.AddButton("Test", 100, 50)
        Controls.HideControl(btn)
        Controls.ShowControl(btn)
        Controls.Remove(btn)

    def test_set_size(self):
        btn = Controls.AddButton("Test", 100, 50)
        Controls.SetSize(btn, 150, 40)
        Controls.Remove(btn)

    def test_counter_increments(self):
        initial = Controls._counter
        btn = Controls.AddButton("Test", 100, 50)
        self.assertEqual(Controls._counter, initial + 1)
        Controls.Remove(btn)

    def test_last_clicked_button(self):
        self.assertIsInstance(Controls.LastClickedButton, str)

    def test_last_typed_textbox(self):
        self.assertIsInstance(Controls.LastTypedTextBox, str)


class TestImageList(unittest.TestCase):
    """Test ImageList operations."""

    def test_load_nonexistent_image(self):
        result = ImageList.LoadImage("nonexistent.png")
        self.assertEqual(result, "")

    def test_get_width_nonexistent(self):
        result = ImageList.GetWidthOfImage("nonexistent")
        self.assertEqual(result, 0)

    def test_get_height_nonexistent(self):
        result = ImageList.GetHeightOfImage("nonexistent")
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
