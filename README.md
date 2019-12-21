# dataquality
GSU Data Mining Lab have Data Base of Sun's Image in heat map format. These images can be accessed using the web API:

http://dmlab.cs.gsu.edu/dmlabapi/

Database have images for around 9 years (starting from 2010 till date) with the interval of 6 minutes.

example:
http://dmlab.cs.gsu.edu/dmlabapi/images/SDO/AIA/param/64/512/?wave=171&starttime=2012-02-13T22:10:00&param=1

Output:

![API Output](https://github.com/SONAMDAWANI/dataquality/blob/master/GitImages/APIExample.jpeg)

Problem Statement:
Some of the images are have erroneous 90 degree rotation. Output these timestamps.

For example:

![Error Image Example](https://github.com/SONAMDAWANI/dataquality/blob/master/GitImages/ErrorImageExample.gif)
