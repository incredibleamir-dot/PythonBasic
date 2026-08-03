"""
Demo 7: Network - HTTP GET, POST, JSON
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import Network, TextWindow

TextWindow.Title = "Network Demo"
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "DarkSlateGray"
TextWindow.Show()

TextWindow.WriteLine("=== Network (REST) Demo ===")
TextWindow.WriteLine()

# GET request
TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("--- JSON API (GET) ---")
TextWindow.ForegroundColor = "White"
response = Network.GetWebPageContents("https://jsonplaceholder.typicode.com/todos/1")
TextWindow.WriteLine("API Response:")
TextWindow.WriteLine(response)
TextWindow.WriteLine()

TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("--- GetWebPageContents ---")
TextWindow.ForegroundColor = "White"
response = Network.GetWebPageContents("https://example.com")
TextWindow.WriteLine("Example.com HTML (first 300 chars):")
TextWindow.WriteLine(response[:300] + "...")
TextWindow.WriteLine()

TextWindow.WriteLine("Done! The Network library uses Python http.client / urllib.")
TextWindow.Pause()
