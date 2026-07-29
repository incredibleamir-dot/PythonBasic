# Microsoft Small Basic - Complete Reference Documentation

*Generated from the official Small Basic XML documentation*

---

## Array

This object provides a way of storing more than one value for a given name. These values can be accessed by another index.

## Clock

This class provides access to the system clock

### Properties

- **Date**: Gets the current system date.
- **Day**: Gets the current day of the month.
- **ElapsedMilliseconds**: Gets the number of milliseconds that have elapsed since 1900.
- **Hour**: Gets the current Hour.
- **Millisecond**: Gets the current Millisecond.
- **Minute**: Gets the current Minute.
- **Month**: Gets the current Month.
- **Second**: Gets the current Second.
- **Time**: Gets the current system time.
- **WeekDay**: Gets the current day of the week.
- **Year**: Gets the current year.

## Controls

The Controls object allows you to add, move and interact with controls.

### Properties

- **LastClickedButton**: Gets the last Button that was clicked on the Graphics Window.
- **LastTypedTextBox**: Gets the last TextBox, text was typed into.

### Events

- **ButtonClicked**: Raises an event when any button control is clicked.
- **TextTyped**: Raises an event when text is typed into any TextBox control.

## Desktop

This class provides methods to interact with the desktop.

### Properties

- **Height**: Gets the screen height of the primary desktop.
- **Width**: Gets the screen width of the primary desktop.

## Dictionary

This class provides access to an online Dictionary service.

## DiscoveryCompletedEventArgs



### Properties

- **Result**: 

## DiscoveryCompletedEventHandler



## File

The File object provides methods to access, read and write information from and to a file on disk.  Using this object, it is possible to save and open settings across multiple sessions of your program.

### Properties

- **LastError**: 

### Methods

#### GetSettingsFilePath



**Returns:** The full path of the settings file specific for this program.

---

#### GetTemporaryFilePath



**Returns:** The full file path of the temporary file.

---

## Flickr

This class provides access to Flickr photo services.

### Methods

#### GetPictureOfMoment

Gets the URL for the picture of the moment.

**Returns:** A file URL for Flickr's picture of the moment

---

## GraphicsWindow

The GraphicsWindow provides graphics related input and output functionality.  For example, using this class, it is possible to draw and fill circles and rectangles.

### Properties

- **BackgroundColor**: Gets or sets the Background color of the Graphics Window.
- **BrushColor**: Gets or sets the brush color to be used to fill shapes drawn on the Graphics Window.
- **CanResize**: Specifies whether or not the Graphics Window can be resized by the user.
- **FontBold**: Gets or sets whether or not the font to be used when drawing text on the Graphics Window, is bold.
- **FontItalic**: Gets or sets whether or not the font to be used when drawing text on the Graphics Window, is italic.
- **FontName**: Gets or sets the Font Name to be used when drawing text on the Graphics Window.
- **FontSize**: Gets or sets the Font Size to be used when drawing text on the Graphics Window.
- **Height**: Gets or sets the Height of the graphics window.
- **LastKey**: Gets the last key that was pressed or released.
- **LastText**: Gets the last text that was entered on the Graphics Window.
- **Left**: Gets or sets the Left Position of the graphics window.
- **MouseX**: Gets the x-position of the mouse relative to the Graphics Window.
- **MouseY**: Gets the y-position of the mouse relative to the Graphics Window.
- **PenColor**: Gets or sets the color of the pen used to draw shapes on the Graphics Window.
- **PenWidth**: Gets or sets the width of the pen used to draw shapes on the Graphics Window.
- **Title**: Gets or sets the title for the graphics window.
- **Top**: Gets or sets the Top Position of the graphics window.
- **Width**: Gets or sets the Width of the graphics window.

### Events

- **KeyDown**: Raises an event when a key is pressed down on the keyboard.
- **KeyUp**: Raises an event when a key is released on the keyboard.
- **MouseDown**: Raises an event when the mouse button is clicked down.
- **MouseMove**: Raises an event when the mouse is moved around.
- **MouseUp**: Raises an event when the mouse button is released.
- **TextInput**: Raises an event when text is entered on the GraphicsWindow.

### Methods

#### Clear

Clears the window.

---

#### GetRandomColor

Gets a valid random color.

**Returns:** A valid random color.

---

#### Hide

Hides the Graphics window.

---

#### Show

Shows the Graphics window to enable interactions with it.

---

## ImageList

This class helps to load and store images in memory.

## Keywords

Keywords object is a place holder for providing documentation for Small Basic Keywords

### Methods

#### And

Does a logical computation and returns true if both inputs are true.

---

#### Else

Check the If statement for information about the Else keyword.

---

#### ElseIf

The ElseIf keyword helps provide an alternate condition while making decisions using the If statement.

**Example:**
```smallbasic
If Clock.Hour < 12 Then
              TextWindow.WriteLine("Good Morning")
            ElseIf Clock.Hour < 16 Then
              TextWindow.WriteLine("Good Afternoon")
            ElseIf Clock.Hour < 20 Then
              TextWindow.WriteLine("Good Evening")
            EndIf
```

---

#### EndFor

Check the For statement for information about the EndFor keyword.

---

#### EndIf

Check the If statement for information about the EndIf keyword.

---

#### EndSub

Check the Sub statement for information about the EndSub keyword.

---

#### EndWhile

Check the While statement for information about the EndWhile keyword.

---

#### For

The For statement allows you to execute a set of statements multiple times.

**Example:**
```smallbasic
For i = 1 To 10 
              TextWindow.WriteLine(i)
            EndFor
```

---

#### Goto

The Goto statement allows branching to a new location in the program.

**Example:**
```smallbasic
start:
            TextWindow.WriteLine(i)
            i = i + 1
            Goto start
```

---

#### If

The If statement allows you to make decisions to do different things.

**Example:**
```smallbasic
If flip = "Tail" Then
              TextWindow.WriteLine("Win")
            Else
              TextWindow.WriteLine("Lose")
            EndIf
```

---

#### Or

Does a logical computation and returns true if either one of the inputs is true.

---

#### Step

The Step keyword is used to specify an increment in the For loop.

**Example:**
```smallbasic
For i = 1 to 10 Step 2
              TextWindow.WriteLine(i)
            EndFor
```

---

#### Sub

The Sub (Subroutine) statement allows you to do groups of things with a single call.

**Example:**
```smallbasic
Sub Win
              Sound.PlayBellRing()
              TextWindow.WriteLine("Win!")
            EndSub
```

---

#### Then

Check the If statement for information about the Then keyword.

---

#### To

Check the For statement for information about the To keyword.

---

#### While

The While statement allows you to repeat something until you achieve a desired result.

**Example:**
```smallbasic
While i < 100
              i = Math.GetRandomNumber(150)
              TextWindow.WriteLine(i)
            EndWhile
```

---

## Math

The Math class provides lots of useful mathematics related methods

### Properties

- **Pi**: Gets the value of Pi

## Mouse

The mouse class provides accessors to get or set the mouse related properties, like the cursor position, pointer, etc.

### Properties

- **IsLeftButtonDown**: Gets whether or not the left button is pressed.
- **IsRightButtonDown**: Gets whether or not the right button is pressed.
- **MouseX**: Gets or sets the mouse cursor's x co-ordinate.
- **MouseY**: Gets or sets the mouse cursor's y co-ordinate.

### Methods

#### HideCursor

Hides the mouse cursor on the screen.

---

#### ShowCursor

Shows the mouse cursors on the screen.

---

## NativeHelper

A private static helper for calling Native APIs

## Network

This helper class provides network access methods

## OfficeResearch



### Events

- **DiscoveryCompleted**: 
- **QueryCompleted**: 
- **RegistrationCompleted**: 
- **StatusCompleted**: 

### Methods

#### #ctor



---

#### Status



---

#### StatusAsync



---

## Platform

The Platform object provides a way to generically invoke other .Net libraries.

## Primitive

The primitive type representing either text or number.

## Program

The Program class provides helpers to control the program execution.

### Properties

- **ArgumentCount**: Gets the number of command-line arguments passed to this program.
- **Directory**: Gets the executing program's directory.

### Methods

#### End

Ends the program.

---

## QueryCompletedEventArgs



### Properties

- **Result**: 

## QueryCompletedEventHandler



## RegistrationCompletedEventArgs



### Properties

- **Result**: 

## RegistrationCompletedEventHandler



## RestHelper

A private static helper for calling Rest based APIs

## Shapes

The Shape object allows you to add, move and rotate shapes to the Graphics window.

## SmallBasicApplication

The Application class provides a Small Basic program with an application object.

### Properties

- **Dispatcher**: Gets the dispatcher for the Small Basic application

## SmallBasicCallback

Signature callback that will be used by all Small Basic library events

## Sound

The Sound object provides operations that allow the playback of sounds.  Some sample sounds are provided along with the library.

### Methods

#### PlayBellRing

Plays the Bell Ring Sound.

---

#### PlayBellRingAndWait

Plays the Bell Ring Sound and waits for it to finish.

---

#### PlayChime

Plays the Chime Sound.

---

#### PlayChimeAndWait

Plays the Chime Sound and waits for it to finish.

---

#### PlayChimes

Plays the Chimes Sound.

---

#### PlayChimesAndWait

Plays the Chimes Sound and waits for it to finish.

---

#### PlayClick

Plays the Click Sound.

---

#### PlayClickAndWait

Plays the Click Sound and waits for it to finish.

---

## Stack

This object provides a way of storing values just like stacking up a plate.  You can push a value to the top of the stack and pop it off. You can only pop the values one by one off the stack and the last pushed value will be the first one to pop out.

## StatusCompletedEventArgs



### Properties

- **Result**: 

## StatusCompletedEventHandler



## Text

The Text object provides helpful operations for working with Text.

## TextWindow

The TextWindow provides text-related input and output functionalities.  For example using this class, it is possible to write or read some text or number to and from the text-based text window.

### Properties

- **BackgroundColor**: Gets or sets the background color of the text to be output in the text window.
- **CursorLeft**: Gets or sets the cursor's column position on the text window.
- **CursorTop**: Gets or sets the cursor's row position on the text window.
- **ForegroundColor**: Gets or sets the foreground color of the text to be output in the text window.
- **Left**: Gets or sets the Left position of the Text Window.
- **Title**: Gets or sets the Title for the text window.
- **Top**: Gets or sets the Top position of the Text Window.

### Methods

#### Clear

Clears the TextWindow.

---

#### Hide

Hides the text window.  Content is perserved when the window is shown again.

---

#### Pause

Waits for user input before returning.

---

#### PauseIfVisible

Waits for user input only when the TextWindow is already open.

---

#### PauseWithoutMessage

Waits for user input before returning.

---

#### Read

Reads a line of text from the text window.  This function will not return until the user hits ENTER.

**Returns:** The text that was read from the text window

---

#### ReadKey

Reads a single character from the text window.

**Returns:** The character that was read from the text window.

---

#### ReadNumber

Reads a number from the text window.  This function will not return until the user hits ENTER.

**Returns:** The number that was read from the text window

---

#### Show

Shows the Text window to enable interactions with it.

---

#### VerifyAccess

Verifies if the access to text Window has been made yet

---

## Timer

The Timer object provides an easy way for doing something repeatedly with a constant interval between.

### Properties

- **Interval**: Gets or sets the interval (in milliseconds) specifying how often the timer should raise the Tick event.  This value can range from 10 to 100000000

### Events

- **Tick**: Raises an event when the timer ticks.

### Methods

#### Pause

Pauses the timer.  Tick events will not be raised.

---

#### Resume

Resumes the timer from a paused state.  Tick events will now be raised.

---

## Turtle

The Turtle provides Logo-like functionality to draw shapes by manipulating the properties of a pen and drawing primitives.

### Properties

- **Angle**: Gets or sets the current angle of the turtle.  While setting, this will turn the turtle instantly to the new angle.
- **Speed**: Specifies how fast the turtle should move.  Valid values are 1 to 10.  If Speed is set to 10, the turtle moves and rotates instantly.
- **X**: Gets or sets the X location of the Turtle.  While setting, this will move the turtle instantly to the new location.
- **Y**: Gets or sets the Y location of the Turtle.  While setting, this will move the turtle instantly to the new location.

### Methods

#### Hide

Hides the Turtle and disables interactions with it.

---

#### PenDown

Sets the pen down to enable the turtle to draw as it moves.

---

#### PenUp

Lifts the pen up to stop drawing as the turtle moves.

---

#### Show

Shows the Turtle to enable interactions with it.

---

#### TurnLeft

Turns the turtle 90 degrees to the left.

---

#### TurnRight

Turns the turtle 90 degrees to the right.

---

---
*This documentation covers all objects in the Microsoft Small Basic Library.*
