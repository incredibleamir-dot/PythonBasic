import os
import tempfile


class File:
    """
    Provides methods to access, read and write information from and to
    files on disk.
    
    Usage:
        contents = File.ReadContents("C:/temp/data.txt")
        File.WriteContents("C:/temp/data.txt", "Hello World")
        File.CopyFile("source.txt", "dest.txt")
    """

    LastError: str = ""

    @classmethod
    def ReadContents(cls, file_path: str) -> str:
        """
        Opens a file and reads the entire file's contents.
        
        Args:
            file_path: The full path of the file to read.
            
        Returns:
            The entire contents of the file, or "FAILED" on error.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def WriteContents(cls, file_path: str, contents: str) -> str:
        """
        Writes the specified contents into a file, replacing existing content.
        
        Args:
            file_path: The full path of the file to write to.
            contents: The contents to write.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(contents)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def ReadLine(cls, file_path: str, line_number: int) -> str:
        """
        Reads the contents at the specified line number.
        
        Args:
            file_path: The full path of the file.
            line_number: The line number (1-based).
            
        Returns:
            The text at the specified line.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if i == line_number:
                        return line.rstrip("\n\r")
            return ""
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def WriteLine(cls, file_path: str, line_number: int, contents: str) -> str:
        """
        Writes the contents at the specified line number (overwrites that line).
        
        Args:
            file_path: The full path of the file.
            line_number: The line number (1-based).
            contents: The contents to write.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            lines = []
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            while len(lines) < line_number:
                lines.append("\n")
            lines[line_number - 1] = contents + "\n"
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def InsertLine(cls, file_path: str, line_number: int, contents: str) -> str:
        """
        Inserts contents at the specified line without overwriting.
        
        Args:
            file_path: The full path of the file.
            line_number: The line number (1-based).
            contents: The contents to insert.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            lines = []
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            lines.insert(line_number - 1, contents + "\n")
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def AppendContents(cls, file_path: str, contents: str) -> str:
        """
        Appends contents to the end of the file.
        
        Args:
            file_path: The full path of the file.
            contents: The contents to append.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(contents)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def CopyFile(cls, source_file_path: str, destination_file_path: str) -> str:
        """
        Copies a file from source to destination.
        
        Args:
            source_file_path: The file to copy.
            destination_file_path: The destination path.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            import shutil
            dest_dir = os.path.dirname(destination_file_path)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(source_file_path, destination_file_path)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def DeleteFile(cls, file_path: str) -> str:
        """
        Deletes the specified file.
        
        Args:
            file_path: The path of the file to delete.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            os.remove(file_path)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def CreateDirectory(cls, directory_path: str) -> str:
        """
        Creates the specified directory.
        
        Args:
            directory_path: The path of the directory to create.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def DeleteDirectory(cls, directory_path: str) -> str:
        """
        Deletes the specified directory.
        
        Args:
            directory_path: The path of the directory to delete.
            
        Returns:
            "SUCCESS" or "FAILED".
        """
        try:
            import shutil
            shutil.rmtree(directory_path)
            return "SUCCESS"
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def GetFiles(cls, directory_path: str):
        """
        Gets the paths of all files in the specified directory.
        
        Args:
            directory_path: The directory to look for files.
            
        Returns:
            A dict (1-based) of file paths, or "FAILED".
        """
        try:
            files = [f for f in os.listdir(directory_path)
                     if os.path.isfile(os.path.join(directory_path, f))]
            return {i + 1: os.path.join(directory_path, f)
                    for i, f in enumerate(files)}
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def GetDirectories(cls, directory_path: str):
        """
        Gets the paths of all subdirectories in the specified directory.
        
        Args:
            directory_path: The directory to look for subdirectories.
            
        Returns:
            A dict (1-based) of directory paths, or "FAILED".
        """
        try:
            dirs = [d for d in os.listdir(directory_path)
                    if os.path.isdir(os.path.join(directory_path, d))]
            return {i + 1: os.path.join(directory_path, d)
                    for i, d in enumerate(dirs)}
        except Exception as e:
            cls.LastError = str(e)
            return "FAILED"

    @classmethod
    def GetTemporaryFilePath(cls) -> str:
        """
        Creates a new temporary file and returns its full path.
        
        Returns:
            The full path of the temporary file.
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as f:
                return f.name
        except Exception as e:
            cls.LastError = str(e)
            return tempfile.gettempdir()

    @classmethod
    def GetSettingsFilePath(cls) -> str:
        """
        Gets the full path of the settings file for this program.
        
        Returns:
            The full path of the settings file.
        """
        return os.path.join(os.getcwd(), "settings.txt")
