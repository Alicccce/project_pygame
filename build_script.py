import PyInstaller.__main__

PyInstaller.__main__.run([
    'pygame_script.py',
    '--onefile',        # Создать один исполняемый файл
    '--name=myexecutable',  # Имя выходного файла (без расширения)
    '--clean',          # Очистить временные файлы после сборки
])