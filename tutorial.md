Hi everyone! 

Today I'm going to be talking about [Python Selenium](https://pypi.org/project/selenium), a Python package that automates web browser interactions. I will briefly be going over several basic Selenium functions in this tutorial.

If you enjoy this tutorial, make sure to leave feedback and upvote! 

## Tutorial Contents

* Introduction
* Installing and Importing
* Web Drivers
  * Chromium
* Load URLs
* Finding Elements
  * Text
  * Input Boxes
  * Buttons
* Using Other Selectors
  * Tag Name 
  * Link Text
* Conclusion

## Introduction

[Python Selenium](https://pypi.org/project/selenium) is a package that allows you to automate web browser interactions in Python! This can be very helpful for web scraping and creating programs that use the internet. Today, I'm going to teach you the basics of Python Selenium. If you prefer other languages over Python, Selenium is also supported in Java, C#, Ruby, and a lot more!

**Note:** This tutorial assumes that you have basic Python knowledge.

## Installing and Importing

Python Selenium is easy to install and import. Since this is a replit tutorial, I will be using replit in my examples!

To install the package, open your shell terminal and type the following Pip command:

`pip install selenium`

Now we are going to import Selenium's web driver, which will allow us to interact with the browser.

At the top of your Python file, add the following code:

`from selenium import webdriver`

Now we can begin using Selenium!

## Web Drivers

Selenium can use different browsers such as Firefox, Chromium, Safari, and Edge. For this tutorial, we are going to use Chromium. To create our driver, we need to do a couple of things beforehand.

First, we need to import `chrome.options`. You can do this by adding the following code under your first import:

`from selenium.webdriver.chrome.options import Options`

Next, we must add a few arguments that will help Chromium load successfully.
Add the following code below your imports:

```py
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
```
Lastly, we can finally define our Chrome driver by adding this line:

`driver = webdriver.Chrome(options=chrome_options)`

Your code (so far!) should look something like this:

```py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
```

Next, we'll go over loading URLs in Selenium!

## Load URLs

To open a specified URL with Selenium, we are going to use `driver.get`. This will load the URL we want to go to. 

For this tutorial, we can load `google.com` by adding this code:

`driver.get("https://google.com")`

This will likely be the first thing you do when using Selenium on your own.

## Finding Elements

Now we are going to learn how to find elements in Selenium. Let's start with reading text.

### Text

You can read text in Selenium using the `.text` attribute. But to use it, we must first *find* the actual element! Let's use `class` to get an element in the Google homepage. This means that Selenium will search for an element with a certain class. 

The "About" link in the top right corner of the Google homepage has the class `MV3Tnb`. Even though we know the link text is "About", let's fetch the text as an example.

First, import the following:

`from selenium.webdriver.common.by import By`

Next, add this line of code to your file:

`google_text = driver.find_element(By.CLASS_NAME, "MV3Tnb").text`

Then, let's print the answer using:

`print(google_text)`

If you correctly added the code, "About" should appear in your output!

### Input

We can find and type in input boxes with Selenium as well. This is similar to finding text, which we covered in the previous step. 

You don't have to import anything new to simply find text on a webpage. We can use `find_element` as we did with text. Also, since the Google Search bar has a much more simple name than class, we'll use that in our function.

For example:

`input_box = driver.find_element(By.NAME, "q")`

This gets the input box you would like to use. Now that you have defined it, you can type in it!

`input_box.send_keys("I am typing in Google Search through Selenium!")`

If you add these lines of code to your file and run it, you should see the text being typed into the search bar.

### Buttons

Guess what? In Selenium, you can also press buttons and keys! Let's say we have typed in our Google Search with Selenium. Now, we can automatically press the `Enter` key to load our search results.

We can use `send_keys` to press `Enter` just as we did in the Input section. First, however, we must import Keys:

`from selenium.webdriver.common.keys import Keys`

Now, if you haven't already, define your input box:

`input_box = driver.find_element(By.NAME, "q")`

Finally, we can press `Enter`:

`input_box.send_keys(Keys.ENTER)`

Now what if there is a different button or link we want to press? 

Since we have already made a Google Search in Selenium, let's say we want to go back home by pressing the "Google" logo. Since it is a link, we'll have to define it using this code (we can find it by ID this time!):

`home_link = driver.find_element(By.ID, "logo")`

Now, you can click on it using:

`home_link.click()`

## Using Other Selectors

Now that we have gone over some basic elements that you can interact with, I'm going to talk about different ways that you can find them. So far, we've used `ID` and `CLASS_NAME`, but there are more!

### Tag Name

We can get an element with it's Tag Name like this:

`driver.find_element(By.TAG_NAME, "a")`

This will return the first element found with that tag name. If there are none, you will receive an error.

If you are unfamiliar with HTML Tag names, you can browse some [here](https://www.w3schools.com/TAGS/default.ASP).

### Link Text

We can also get links by their text. 

For example:

`driver.find_element(By.LINK_TEXT, "About")`

This will find the "About" link in the top left corner of Google. You can then add attributes.

There are many other selectors you can use to find elements. You can view a list [here](https://selenium-python.readthedocs.io/locating-elements.html).

## Conclusion

Thank you all for reading through this guide! Though this didn't go through every part of Selenium, I hope you learned something and feel encouraged to use the package in other projects.

Until next time!