Learning Scrapy by downloading ImageNet images <br /><br />

example 1:</br>
$ scrapy crawl imageCrawler -a getSearch=cat<br />
default getSearch=dog<br /><br />

example 2:</br>
$ scrapy crawl imageCrawler -a getSearch=person -a wnid=n00007846<br />
In this case, getSearch is just the directory's name.<br /><br />

The mapping between WordNet ID and words for all synsets in this 
[link](http://image-net.org/archive/words.txt) from ImageNet.<br />


