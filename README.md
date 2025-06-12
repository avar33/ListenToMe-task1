**Title: Listen to Me!**

**Description:** "Listen to Me!" is a music recommendation app designed to help users discover songs and artists that align with their personal tastes.
Users can choose whether they want recommendations for artists, songs, or both. After that, they can select 3 to 6 preferences from a set of options that reflect mood, genre, and style.

Using these selected preferences, the app generates a ranked list of recommendations that best match the user's criteria—from most to least fitting. Every recommended item shares at least one attribute with the selected preferences, ensuring relevance in all results. 

**Installations:**
  python 3.12.4 
  Pyside6: current working version 6.9.0 (or compatible)
  Qt Designer: included with pyside6 installation 
  
  main repository: https://github.com/avar33/ListenToMe-task1.git
  
**instructions given as pertains to VSC
Clone the repo using the main repository URL given above. To set up a virtual environment in VSC begin by opening the Command Palette. Select: "Python: Create Environment" -> .venv -> choose the appropriate python version -- in this case 3.12.4. The version can be found using the following command: "python --version". Once your enviroment has been established install Pyside6 --"pip install pyside6"-- if not already installed. Verfity its installation and other important information using "pip show pyside6". To launch Qt Designer, loctae pyside6-designer.exe inside your .venv/Scripts/ directory. This will help you build the UI using a drag and drop approach. The aformentioned installations shall provide the necessary foundation for the projects compilation and execution. The project should launch when running the main.py file.

**iTunes API:** Images for this project were gathered using the iTunes Search API, courtesy of Apple Developer. The API returns data available across Apple storefronts including the iTunes Store, App Store, iBooks Store and Mac App Store. Content includes but is not limited to images and general information from books, audiobooks, music, music videos, podcasts, TV shows, and movies. Free for non-commercial use with terms and conditions. Learn more about licensing, restirctions, and use of the API on the Apple Developer website or using the following: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html#:~:text=The%20Search%20API%20allows%20you,and%20not%20for%20entertainment%20purposes.
