# AmazonScrapingApp

This app uses Selenium, Tkinter and Pandas. For Selenium it will attempt to use the Chrome browser, therefore a path to your chromedriver.exe must be specified.
In the very first line you will find the variable PATH, set to the default path to the chromedriver.exe(C/programs(86x). You can simply change this if your chromediver is somewhere 
else.

If you don't have the chromedriver.exe yet, you can easily download it here:
https://chromedriver.chromium.org/downloads

When you run the app, the first window will open. Here you can specify the product your are looking for and set additional pages (the default is 0, it will
only look on the first page). Then press "Search & Collect" to start the search.
The app will print its current status on the console and will print "Finished." once the search is completed. Then you can either
search for more products by repeating this step, or delete the current results by pressing "Clear All Data", or press "Exit & View Data" to proceed to the next
window. 

The second window will allow you to scroll through your products + their price. To save it as a xlsx-file, you can just type a filename into the empty field
below and press "Save as xlsx". The file will be in the same folder as the AmazonScrpingApp.py 
Or you can press "Exit & Over" to close the app without saving data.
