<h2>This is a web based Instagram Scraper</h2>

<p>This scrapper is written on a python library `selenium webdriver` and hosted on a browser using `node js`</p>

<p>For the scrapper to work you need to have python and javascrpt installed on the machine and to host it install the languages on the server </p>

<p>The javascript takes in a name and the python takes over when the button is clicked to find the person and scrape some details from the account of the user</p>

<P>The details that are scraped from the user are :
<ul>
  <li>The name offered</li>
  <li>bio given, if available</li>
  <li>Number of posts</li>
</ul>

and gets into each post individually to get :
<ul>
  <li>All captions - this includes the hashtags</li>
  <li>All the comments</li>
</ul>
</P>

<P>When the scrapper is done it saves the data in a csv file and push's the data to the frontend javascript and automatically the browser downloads the file for you to display the content</P>
