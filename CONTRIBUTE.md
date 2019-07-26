## TODO

* Add Downloading
* Prevent multiple clicks on play button from playing the same video many times
* Add statusbar
* Add toolbar
* Catch exceptions for no network connection
* Show video info on left panel
* Add app icon

## How It Works
**UI**

The launch script first creates a QMainWindow, and it's init continues to create the rest of the UI using makeItems. It creates a toolbar, statusbar, and tab-bar. The centralWidget is a tab widget. This is meant to seperate the search results from the subscription menu and Downloads menu. The list of search results is a QStackedWidge of QScrollArea widgets in order for the result view to be easily extended to include other sites. This is also the purpose of the QComboBox.


**Network Requests**

All network requests, downloads, and playback are done using QThreads. A list of objects for interfacing with the sites to be searched is stored in an attribute of the state object. When the Search button is clicked, or carriage return is pressed in the input box, the getPage() method of the interface object is called. It creates a subclassed QThread as an attribute of the main window object. In the youtube interface, this thread requests the html page from youtube, and passes the file to pullData() before being destoryed.
Data is pulled out of the html file by using a BeautifulSoup4 tree. It finds all branches with the attribute 'data-context-item-id' and uses the value of the id, and it's title attribute to build a list of contentblocks. Each has the title of the content, the video link, and the image link.
All play button click events are connected to playVideo(). It creates a VidWorker (subclassed from QThread), and plays the video using a subprocess once the thread has been started.


