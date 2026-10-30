import shutil
from pathlib import Path



#Maps target folder names to a list of associated file extensions.
DIRECTORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "Media": [".mkv",".avi", ".mov"],
    "Music": [".mp4", ".mp3", ".wav"],
    "Archives_Code": [".zip", ".tar", ".gz", ".rar", ".7z", ".py", ".js", ".html", ".json"],
    "Installers": [".exe", ".dmg", ".pkg", ".deb", ".rpm"],
}



#target_dir is a string input and is the path to the target folder that is to be sorted.
def folder_organise(taget_dir):

    """
    Scans specified directory, categorises files based on their extensions, automatically creates subfolders, and moves files into them based on their extensions.
    """

    #String path is converted to Path object.
    target_path = Path(taget_dir)

    #Checks that the directory exists.
    if not target_path.exists():
        print("Directory does not exist")
        return

    print(f"\nScanning and organising: {target_path.resolve()}")
    files_moved = 0

    for item in target_path.iterdir():

        #Checks if item is a directory or hidden file
        if item.is_dir() or item.name.startswith('.'):
            continue

        #Extracts the file extension and stores it.
        file_extension = item.suffix.lower()
        moved = False

        for category, extensions in DIRECTORIES.items():
            if file_extension in extensions:
                #Defines path for category subfolder.
                category_folder = target_path / category

                #Creates the subfolder if it does not already exist.
                category_folder.mkdir(exist_ok=True)

                #Defines final destination for the file.
                destination = category_folder / item.name

                #Checks for naming collisions
                destination = handle_collision(destination, category_folder, item)

                #Moves file from source location to new destination.
                shutil.move(str(item), str(destination))

                print(f"{item.name} has been successfully moved to {category}")
                files_moved += 1
                moved = True
                break

        if not moved:
            others_folder = target_path / "Others"
            others_folder.mkdir(exist_ok=True)
            destination = others_folder / item.name

            #Checks for name collisions in 'Others' folder
            destination = handle_collision(destination, others_folder, item)

            #Moves file from source location to new destination,
            shutil.move(str(item), str(destination))
            print(f"{item.name} has been successfully moved to 'Others'")
            files_moved += 1

    print("Directory successfully organised.")


def handle_collision(destination, folder, original_item):

    """
    Checks if there is an existing file with the same name, prevents overwriting by incrementing a counter for each identical record and adding said counter number to each record's name.
    """

    if destination.exists():
        #Saves file name without the extension.
        base = original_item.stem
        #Saves the extension without the file name.
        extension = original_item.suffix
        #Represents the amount of files there are with the same name.
        counter = 1

    #Runs until a file name that is not in use is found.
    while destination.exists():
        destination = folder / f"{base}_{counter}{extension}"
        counter += 1

    return destination


#==================
#SCRIPT ENTRY POINT
#==================
if __name__ == "__main__":
    #Prompt user to enter the path to the directory they would like organised.
    path_input = input("Enter the path of the folder that you would like organised: ").strip()

    #Clean any accidental quotation marks if user drag 'n' dropped their path.
    path_input = path_input.strip('"\'')

    #Runs the folder_organise function.
    folder_organise(path_input)