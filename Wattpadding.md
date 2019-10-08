
# Wattpadding


```python
from bs4 import BeautifulSoup
import re, os, csv
```


```python
import pandas as pd
```

## `wgetting` the HTML

The first thing we need to do is get the html from which we will extract the texts we want. The easiest way I know to do that is to use `wget`. While we can use some command line apps from within a Jupyter notebook by simply prepending a percent sign, %, it does not appear that `wget` is one of those. I tried and got: `UsageError: Line magic function `%wget` not found.` 

So I opened a terminal window and ran `wget -w 2 -i ../inputs/wattpad_list.txt` from within the folder/directory where I wanted to have the files downloaded, a directory I created for this project called, of all things, `wattpad`. 

This initial usage did not go as planned: for every file in the list, a 403 error was returned. I wasn't sure if the cause was the Wattpad site wanting a login, so I pasted one of the URLs into a browser to see what I would get, and it returned the page. I then remembered something about some sites wanting a human-operated browser, so I looked up a way to tell a site that wget was a browser, which uses the `--user-agent` flag. The solution I settled on was from [AskApache][] and it consisted of editing, or in my case creating, a .wgetrc file which supplied the necessary information to the picky server:

```bash
### Sample Wget initialization file .wgetrc by https://www.askapache.com
## Local settings (for a user to set in his $HOME/.wgetrc).  It is
## *highly* undesirable to put these settings in the global file, since
## they are potentially dangerous to "normal" users.
##
## Even when setting up your own ~/.wgetrc, you should know what you
## are doing before doing so.
header = Accept-Language: en-us,en;q=0.5
header = Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
header = Connection: keep-alive
user_agent = Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2
referer = https://www.askapache.com/
robots = off
```

I logged out and back into the terminal to make sure the resource file got loaded, or whatever, and ran `wget` again. A whole lot of scrolling later and:

```
FINISHED --2019-08-30 19:13:23--
Total wall clock time: 1m 47s
Downloaded: 35 files, 3.8M in 0.8s (4.62 MB/s)
```

The short version of how to use `wget` can be found on a [post][] I wrote a few years ago.

[AskApache]: https://www.askapache.com/linux/wget-header-trick/
[post]: http://johnlaudun.org/20160518-wgetting-ted-talk-transcripts/

## Parsing with `BeautifulSoup`

For each page, we will want to get the title of the page and, while we're at it, we might as well pick up some of the metadata the site offers us about the page as well as the text on the page. We'll start with the text because it's all inside paragraph elements and we can probably navigate that fairly quickly.

We will first create the particular kind of Python object that `BeautifulSoup` creates and which I kinda understand but not enought to explain it to anyone. (Note all the imports for this work are at the top of the page.)


```python
soup = BeautifulSoup(open("wattpad/279794502-my-immortal-commentary-chapters-1-5"), 
                        "html5lib")
```

### Getting the Text

If we can simply get all elements with `data-p-id` in a page, I think we'll have all the content we need, so I am going to start with this:

```html
<p data-p-id="ad1ea648c5d5d7a6914ef1cf3afc9adc">AN: Fangz 2 bloodytearz666 4 helpin me wif da chapta! BTW preps stop flaming ma story ok!<span class="comment-marker on-inline-comments-modal">
  <span class="num-comment">
    4
  </span>
  <span class="fa fa-comment-count fa-wp-neutral-2 " aria-hidden="true" style="font-size:28px;"></span>
</span>
</p>
```
Otherwise, we will have to deal with the `div` that holds all these paragraphs and/or the `pre` tag -- which still may work.
```html
<div class="col-xs-10 col-xs-offset-1 col-sm-10 col-sm-offset-1 col-md-7 col-md-offset-1 col-lg-6 col-lg-offset-3 panel panel-reading" dir="ltr">
<pre><p data-p-id="ad1ea648c5d5d7a6914ef1cf3afc9adc">AN: Fangz 2 bloodytearz666 4 helpin me wif da chapta! BTW preps stop flaming ma story ok!<span class="comment-marker on-inline-comments-modal">
  <span class="num-comment">
    4
  </span>
  <span class="fa fa-comment-count fa-wp-neutral-2 " aria-hidden="true" style="font-size:28px;"></span>
</span>
</p>
```

A little experimentation turned up this method:


```python
for item in soup.find_all('p'):
#     print(item)
    if item.has_attr('data-p-id'):
        print(item.text) # Sadly, .text removes the bold and italic tags
```

    Chapter 1.
    AN: Special fangz (get it, coz Im goffik) No. 2 my gf (ew not in that way) raven, I spy with my little eye a homophobe. bloodytearz666 4 helpin me wif da story and spelling. U rok! Justin ur da luv of my deprzzing life u rok 2! MCR ROX!
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Hate to break it to ya honey, but that's not how you separate chapters and ANs.
    Hi my name is Ebony Dark'ness Dementia Raven Way and I have long ebony black hair Redundancy much? (that's how I got my name) with purple streaks and red tips that reaches my mid-back and icy blue eyes like limpid tears and a lot of people tell me I look like Amy Lee (AN: if u don't know who she is get da hell out of here!). I'm not related to Gerard Way but I wish I was because he's a major fucking hottie. I don't even know where to begin on that last sentence. I'm a vampire but my teeth are straight and white. Stop fucking lyin'.. I have pale white skin. I'm also a witch, and I go to a magic school called Hogwarts in England HOGWARTS IS IN SCOTLAND where I'm in the seventh year (I'm seventeen). I'm a goth (in case you couldn't tell) and I wear mostly black. Wow, really? I love Hot Topic and I buy all my clothes from there. For example today I was wearing a black corset with matching lace around it and a black leather miniskirt, pink fishnets and black combat boots. I was wearing Nobody gives a shit. black lipstick, white foundation, black eyeliner and red eye shadow. I was walking outside Hogwarts. It was snowing and raining Hailing or sleeting, basically. Get your ass back inside. so there was no sun, which I was very happy about. A lot of preps stared at me. I put up my middle finger at them.
    "Hey Ebony!" shouted a voice. I looked up. It was.... Draco Malfoy! Why the elipse?
    "What's up Draco?" I asked.
    "Nothing." he said shyly.
    But then, I heard my friends call me and I had to go away.
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX No.
    AN: IS it good? PLZ tell me fangz! This fic is one of those things that's so shitty that it's good.
    Chapter 2.
    AN: Fangz 2 bloodytearz666 4 helpin me wif da chapta! BTW preps stop flaming ma story ok!
    XXXXXXXXXXXXXXXXXXXXXX666XXXXXXXXXXXXXXXXXXXXXXXX
    The next day I woke up in my bedroom. It was snowing and raining again. I opened the door of my coffin and drank some blood from a bottle I had. My coffin was black ebony and inside it was hot pink velvet Later in the story though, Enoby claims she hates pink. with black lace on the ends. I got out of my coffin and took of my giant MCR t-shirt which I used for pajamas. Instead, I put on a black leather dress, a pentagram necklace, combat boots and black fishnets on. I put on four pairs of earrings in my pierced ears, and put my hair in a kind of messy bun. In a kind of messy bun.
    My friend, Willow (AN: Raven dis is u!) woke up then and grinned at me. She flipped her long waist-length raven black hair with pink streaks and opened her forest-green eyes. She put on her Marilyn Manson t-shirt with a black mini, fishnets and pointy high-heeled boots. We put on our makeup (black lipstick white foundation and black eyeliner.) Please stop describing clothes so damn much.
    "OMFG, I saw you talking to Draco Malfoy yesterday!" she said excitedly.
    "Yeah? So?" I said, blushing.
    "Do you like Draco?" she asked as we went out of the Slytherin common room and into the Great Hall.
    "No I so fucking don't!" I shouted. Which means you do. Come one Enoby, we read enough fics to know.


### Getting the Title and the Metadata

You can take a look at what the raw HTML looks like for yourself. The HTML below has been edited to focus on the elements and attributes we need to think about to get out the information we want: 

```html
<header class="panel panel-reading text-center">
<h2>Chapter 2.
</h2>
<div class="story-stats">
<span class="reads">
899
</span>
<span class="votes">
45
</span>
<span class="comments on-comments">
<a href="#">103</a>
</span>
</div>
<div class="author hidden-lg">
<a class="on-navigate" href="/user/VioletKingston">VioletKingston</a>
</div>
</header>
```

The tree structure for this would look like:

```
body - header - h2
              \
                story-stats - reads
                            \
                              votes
                             \
                              comments
              \ author
```

Title was easy:


```python
title = soup.find('h2')
print(title.text)
```

    Chapters 1-5
    


Let's see if we can pick up the other metadata, starting with the number of times a text has been read:


```python
reads = soup.select('span[class*="reads"]')
print(reads)
```

    [<span class="reads">
    <span aria-hidden="true" class="fa fa-view fa-wp-neutral-2" style="font-size:14px;"></span> 17
    </span>]


Ugly, and I can't get `BeautifulSoup` to clean this up, so I am going to go with some old-fashioned regex. The regex alone leaves in some newlines, for now, the ugliness below will have to do -- a better regex filter would take care of the newlines.


```python
# Our regex "filter"
clean = re.compile('<.*?>')
```


```python
# Our filtering process
text = re.sub(clean, '', str(reads)[1:-1]).rstrip().lstrip()
print(text) # Check results
```

    17



```python
votes = re.sub(clean, '', str(soup.select('span[class*="votes"]'))).lstrip('[\n').rstrip('\n]')
print(votes)
```

     0



```python
comments = re.sub(clean, '', str(soup.select('span[class*="comments"]'))).lstrip('[\n').rstrip('\n]')
print(comments)
```

    2


Not quite done. We still need author, and in looking at the HTML for where the author is, I see that what I have as title above is probably more like a subtitle or part. Here's the relevant code from the HTML file:
```html
<h1 class="title h5">
My Immortal Commentary
</h1>
<span class="author h6">by jyushiimatsuno</span>
</span>
```


```python
author = re.sub(clean, '', str(soup.select('span[class*="author h6"]'))).lstrip('[\n by').rstrip('\n]')
print(author)
```

    jyushiimatsuno



```python
title = re.sub(clean, '', str(soup.select('h1[class*="title h5"]'))).lstrip('[\n').rstrip('\n]')
print(title)
```

    My Immortal Commentary


Okay, now to stitch these various pieces of working, if also ugly, code together. We are going to create a function that produces these results. We are then going to write a `for` loop that works through all the files in our `inputs` directory, runs them through our function, and then we are going to save the outputs to a `csv` file.


```python
def parse(soup):
    # This function requires re
    clean = re.compile('<.*?>')
    title = re.sub(clean, '', str(soup.select('h1[class*="title h5"]'))).lstrip('[\n').rstrip('\n]')
    subtitle = soup.find('h2').text.rstrip()
    author = re.sub(clean, '', str(soup.select('span[class*="author h6"]'))).lstrip('[\n by').rstrip('\n]')
    reads = re.sub(clean, '', str(soup.select('span[class*="reads"]'))).lstrip('[\n ').rstrip('\n]')
    votes = re.sub(clean, '', str(soup.select('span[class*="votes"]'))).lstrip('[\n ').rstrip('\n]')
    comments = re.sub(clean, '', str(soup.select('span[class*="comments"]'))).lstrip('[\n').rstrip('\n]')
    text = ''.join([item.text for item in soup.find_all('p') if item.has_attr('data-p-id')])
    return(title, subtitle, author, reads, votes, comments, text)
```

We can test the functionality of the parse feature on our currently loaded soup:


```python
for item in parse(soup):
    print(item)
```

    My Immortal Commentary
    Chapters 1-5
    jyushiimatsuno
    17
    0
    2
    Chapter 1.AN: Special fangz (get it, coz Im goffik) No. 2 my gf (ew not in that way) raven, I spy with my little eye a homophobe. bloodytearz666 4 helpin me wif da story and spelling. U rok! Justin ur da luv of my deprzzing life u rok 2! MCR ROX!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Hate to break it to ya honey, but that's not how you separate chapters and ANs.Hi my name is Ebony Dark'ness Dementia Raven Way and I have long ebony black hair Redundancy much? (that's how I got my name) with purple streaks and red tips that reaches my mid-back and icy blue eyes like limpid tears and a lot of people tell me I look like Amy Lee (AN: if u don't know who she is get da hell out of here!). I'm not related to Gerard Way but I wish I was because he's a major fucking hottie. I don't even know where to begin on that last sentence. I'm a vampire but my teeth are straight and white. Stop fucking lyin'.. I have pale white skin. I'm also a witch, and I go to a magic school called Hogwarts in England HOGWARTS IS IN SCOTLAND where I'm in the seventh year (I'm seventeen). I'm a goth (in case you couldn't tell) and I wear mostly black. Wow, really? I love Hot Topic and I buy all my clothes from there. For example today I was wearing a black corset with matching lace around it and a black leather miniskirt, pink fishnets and black combat boots. I was wearing Nobody gives a shit. black lipstick, white foundation, black eyeliner and red eye shadow. I was walking outside Hogwarts. It was snowing and raining Hailing or sleeting, basically. Get your ass back inside. so there was no sun, which I was very happy about. A lot of preps stared at me. I put up my middle finger at them."Hey Ebony!" shouted a voice. I looked up. It was.... Draco Malfoy! Why the elipse?"What's up Draco?" I asked."Nothing." he said shyly.But then, I heard my friends call me and I had to go away.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX No.AN: IS it good? PLZ tell me fangz! This fic is one of those things that's so shitty that it's good.Chapter 2.AN: Fangz 2 bloodytearz666 4 helpin me wif da chapta! BTW preps stop flaming ma story ok!XXXXXXXXXXXXXXXXXXXXXX666XXXXXXXXXXXXXXXXXXXXXXXXThe next day I woke up in my bedroom. It was snowing and raining again. I opened the door of my coffin and drank some blood from a bottle I had. My coffin was black ebony and inside it was hot pink velvet Later in the story though, Enoby claims she hates pink. with black lace on the ends. I got out of my coffin and took of my giant MCR t-shirt which I used for pajamas. Instead, I put on a black leather dress, a pentagram necklace, combat boots and black fishnets on. I put on four pairs of earrings in my pierced ears, and put my hair in a kind of messy bun. In a kind of messy bun.My friend, Willow (AN: Raven dis is u!) woke up then and grinned at me. She flipped her long waist-length raven black hair with pink streaks and opened her forest-green eyes. She put on her Marilyn Manson t-shirt with a black mini, fishnets and pointy high-heeled boots. We put on our makeup (black lipstick white foundation and black eyeliner.) Please stop describing clothes so damn much."OMFG, I saw you talking to Draco Malfoy yesterday!" she said excitedly."Yeah? So?" I said, blushing."Do you like Draco?" she asked as we went out of the Slytherin common room and into the Great Hall."No I so fucking don't!" I shouted. Which means you do. Come one Enoby, we read enough fics to know.


## Writing the CSV

The code below for saving results of a parsing operation to a `csv` files is drawn from some boilerplate I have lying around that was first developed by Padraic C on StackOverflow. (All hail, Padraic!)


```python
def to_csv(pth, out):
    """This function requires both the csv and os modules."""
    # open file to write to.
    with open(out, "w") as out:
        # create csv.writer. 
        wr = csv.writer(out)
        # write our headers.
        wr.writerow(["title", "subtitle", "author", "reads", "votes", "comments", "text"])
        # get all our html files.
        for html in os.listdir(pth):
            with open(os.path.join(pth, html)) as f:
                # parse the file and write the data to a row.
                wr.writerow(parse(BeautifulSoup(f, "html5lib")))
```

And then all you do it this to run everything -- make sure you know what directory you are in before doing this so that the the function has the correct path to the input directory.


```python
to_csv("./wattpad","./outputs/beloveds.csv")
```

## Writing Text Files

Sometimes, instead of a CSV file, you want a collection of files you can load into some sort of machine text analysis system. Here is an alternative output:


```python
with open(csv_file) as file:
    reader = csv.reader(file, delimiter=',')
    count = -1
    for row in reader:
        row[1] = str(row[1]).replace(r'\n', '')
        row[1] = str(row[1]).replace(r'\r', '')
        if not row[1]:
            row[1] = ' '
        with open('corpus' + str(count) + '.txt', 'w') as output:
            output.write(str(row[1]))
        count += 1
```

Instead of working with the CSV, we could also try this in pandas:


```python
df = pd.read_csv('outputs/beloveds.csv')
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>subtitle</th>
      <th>author</th>
      <th>reads</th>
      <th>votes</th>
      <th>comments</th>
      <th>text</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>My Immortal with Commentary</td>
      <td>Chapter 3.</td>
      <td>VioletKingston</td>
      <td>878</td>
      <td>42</td>
      <td>140</td>
      <td>AN: STOP FLAMMING DA STORY PREPZ OK! odderwize...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>My Immortal Commentary</td>
      <td>Chapters 1-5</td>
      <td>jyushiimatsuno</td>
      <td>17</td>
      <td>0</td>
      <td>2</td>
      <td>Chapter 1.AN: Special fangz (get it, coz Im go...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Everything Wrong With My Immortal</td>
      <td>Chapter 7. Wake Me Up</td>
      <td>FFSins</td>
      <td>26</td>
      <td>2</td>
      <td>1</td>
      <td>Chapter 7. Bring me 2 life (That's an Evanesce...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>My immortal, the commentary</td>
      <td>Chapter 6</td>
      <td>Monkee66</td>
      <td>22</td>
      <td>1</td>
      <td>0</td>
      <td>Hello sweeties. How are you all doing? Here's ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>My Immortal with Commentary</td>
      <td>Chapter 4.</td>
      <td>VioletKingston</td>
      <td>729</td>
      <td>40</td>
      <td>101</td>
      <td>AN: I sed stup flaming ok ebony's name is ENOB...</td>
    </tr>
  </tbody>
</table>
</div>




```python
df["filename"] = df["author"] + " " + df["subtitle"]
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>subtitle</th>
      <th>author</th>
      <th>reads</th>
      <th>votes</th>
      <th>comments</th>
      <th>text</th>
      <th>filename</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>My Immortal with Commentary</td>
      <td>Chapter 3.</td>
      <td>VioletKingston</td>
      <td>878</td>
      <td>42</td>
      <td>140</td>
      <td>AN: STOP FLAMMING DA STORY PREPZ OK! odderwize...</td>
      <td>VioletKingston Chapter 3.</td>
    </tr>
    <tr>
      <th>1</th>
      <td>My Immortal Commentary</td>
      <td>Chapters 1-5</td>
      <td>jyushiimatsuno</td>
      <td>17</td>
      <td>0</td>
      <td>2</td>
      <td>Chapter 1.AN: Special fangz (get it, coz Im go...</td>
      <td>jyushiimatsuno Chapters 1-5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Everything Wrong With My Immortal</td>
      <td>Chapter 7. Wake Me Up</td>
      <td>FFSins</td>
      <td>26</td>
      <td>2</td>
      <td>1</td>
      <td>Chapter 7. Bring me 2 life (That's an Evanesce...</td>
      <td>FFSins Chapter 7. Wake Me Up</td>
    </tr>
    <tr>
      <th>3</th>
      <td>My immortal, the commentary</td>
      <td>Chapter 6</td>
      <td>Monkee66</td>
      <td>22</td>
      <td>1</td>
      <td>0</td>
      <td>Hello sweeties. How are you all doing? Here's ...</td>
      <td>Monkee66 Chapter 6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>My Immortal with Commentary</td>
      <td>Chapter 4.</td>
      <td>VioletKingston</td>
      <td>729</td>
      <td>40</td>
      <td>101</td>
      <td>AN: I sed stup flaming ok ebony's name is ENOB...</td>
      <td>VioletKingston Chapter 4.</td>
    </tr>
  </tbody>
</table>
</div>



We have filenames, but they aren't quite what they want. We want to get rid of spaces, replacing them with underscores, and get rid of periods, in case the OS we use doesn't like them in filenames -- most operating systems are okay with dashes and underscores, so we'll stick with those.


```python
df["filename"] = df["filename"].str.strip('.').replace(' ', '_', regex=True)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>subtitle</th>
      <th>author</th>
      <th>reads</th>
      <th>votes</th>
      <th>comments</th>
      <th>text</th>
      <th>filename</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>My Immortal with Commentary</td>
      <td>Chapter 3.</td>
      <td>VioletKingston</td>
      <td>878</td>
      <td>42</td>
      <td>140</td>
      <td>AN: STOP FLAMMING DA STORY PREPZ OK! odderwize...</td>
      <td>VioletKingston_Chapter_3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>My Immortal Commentary</td>
      <td>Chapters 1-5</td>
      <td>jyushiimatsuno</td>
      <td>17</td>
      <td>0</td>
      <td>2</td>
      <td>Chapter 1.AN: Special fangz (get it, coz Im go...</td>
      <td>jyushiimatsuno_Chapters_1-5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Everything Wrong With My Immortal</td>
      <td>Chapter 7. Wake Me Up</td>
      <td>FFSins</td>
      <td>26</td>
      <td>2</td>
      <td>1</td>
      <td>Chapter 7. Bring me 2 life (That's an Evanesce...</td>
      <td>FFSins_Chapter_7._Wake_Me_Up</td>
    </tr>
    <tr>
      <th>3</th>
      <td>My immortal, the commentary</td>
      <td>Chapter 6</td>
      <td>Monkee66</td>
      <td>22</td>
      <td>1</td>
      <td>0</td>
      <td>Hello sweeties. How are you all doing? Here's ...</td>
      <td>Monkee66_Chapter_6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>My Immortal with Commentary</td>
      <td>Chapter 4.</td>
      <td>VioletKingston</td>
      <td>729</td>
      <td>40</td>
      <td>101</td>
      <td>AN: I sed stup flaming ok ebony's name is ENOB...</td>
      <td>VioletKingston_Chapter_4</td>
    </tr>
  </tbody>
</table>
</div>




```python
df2 = df.set_index('filename')
df2 = df2.drop(columns = ['title', 'subtitle', 'author', 'reads', 'votes', 'comments'])
df2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>text</th>
    </tr>
    <tr>
      <th>filename</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>VioletKingston_Chapter_3</th>
      <td>AN: STOP FLAMMING DA STORY PREPZ OK! odderwize...</td>
    </tr>
    <tr>
      <th>jyushiimatsuno_Chapters_1-5</th>
      <td>Chapter 1.AN: Special fangz (get it, coz Im go...</td>
    </tr>
    <tr>
      <th>FFSins_Chapter_7._Wake_Me_Up</th>
      <td>Chapter 7. Bring me 2 life (That's an Evanesce...</td>
    </tr>
    <tr>
      <th>Monkee66_Chapter_6</th>
      <td>Hello sweeties. How are you all doing? Here's ...</td>
    </tr>
    <tr>
      <th>VioletKingston_Chapter_4</th>
      <td>AN: I sed stup flaming ok ebony's name is ENOB...</td>
    </tr>
  </tbody>
</table>
</div>




```python
df2.to_csv("./outputs/beloveds2.csv", header=False )
```

There still needs to be clean-up here.

Two regex possibilities:
```
[^A-Za-z,."'\s]
[\[\]\n]
```


```python
import re
```


```python
with open('./outputs/beloveds2.csv', 'r') as in_file:
    lines = in_file.readlines()
    for line in lines:
        with open('./beloveds/{}.txt'.format(line.split(',')[1]), 'w') as out_file:
            content = re.sub(r'[\[\]\n]', '', str(line.split(',')[2:]))
            out_file.write(content)
```
