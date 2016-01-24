# digital-mess-cleaner
Collection of tools which help to structure and clean up your digital storage mess

#Image Sort & Deduplicate
This scipt scans a directory tree for images from Digital Cameras and sorts it into a new folder structure grouping it by date Year/Month. If the Target already exists a SHA256 Sum is calculated over the File to check it it is a Duplicate. Duplicates will be removed others will be renamed and moved to the other files.

#Folder Watchdog
Start python importWatchdog.py /path/to/somefolder/ /path/to/imagelibrary to have a watchdog monitoring the import folder.
Files copied to that folder will be processed and moved to the calculated targetfolder within the library. If there is a matching processor