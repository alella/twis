twis
=======

twis is a twitter search and notify application for staying distracted at work. You could as well search for keywords in twitter but then, you'll have to keep pressing on the refresh button for getting the latest content. Most of the time there is no content, so your effort gets wasted. This service lets you access to the content as soon as its posted.

**Requirements**
* oauthlib
* pygame
* python-twitter
* requests
* requests-oauthlib
* simplejson
* awesome window manager (for desktop notifications)

**Setup:**

Clone this repo

`git clone https://github.com/alella/twis.git`

Make sure you install all requirements

`sudo pip install -r requirements.txt`

Populate *mytwitterkeys.py* with your twitter api keys.

Run the service using (replace `<search string>` with any search string like cool, linux, python)

`python twis.py <search string>`

example `python twis.py avengers` would result in something like this
![](http://s3.postimg.org/q1oyc7xzn/Untitled.png)

[awesome WM 3.5]:http://awesome.naquadah.org/
