import os
import shutil
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "C:/Users/abdel/Downloads"
image_dir = "C:/Users/abdel/OneDrive/Pictures"
vid_dir = "C:/Users/abdel/Videos"
music_dir = "C:/Users/abdel/Music"

def make_name(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    new_name = name
    while os.path.exists(os.path.join(dest, new_name)):
        new_name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return new_name


def move(dest, entry, name):
    file_exists_before = os.path.exists(os.path.join(dest, name))
    if file_exists_before:
        new_name = make_name(dest, name)
        os.rename(entry, os.path.join(dest, new_name))
    else:
        shutil.move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    name = entry.name
                    dest=source_dir
                    if name.endswith('.mp3') or name.endswith('.wav'):
                        dest=music_dir
                        move(dest, entry.path, name)
                    elif name.endswith('.mp4') or name.endswith('.mov'):
                        dest=vid_dir
                        move(dest, entry.path, name)
                    elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png') or name.endswith('.WebP') or name.endswith('.AVIF'):
                        dest=image_dir
                        move(dest, entry.path, name)

if __name__ == "__main__":
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
