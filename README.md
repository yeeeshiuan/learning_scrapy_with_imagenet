Learning Scrapy by downloading ImageNet images <br /><br />

Usage: scrapy crawl imageCrawler -a keyword=keyword\[\+keyword\]<br />
default keyword=dog<br /><br />

example:</br>
$ scrapy crawl imageCrawler -a keyword=cat<br />
$ scrapy crawl imageCrawler -a keyword=woman+lady<br />

After launch the command, <br />
you will get into interactive CLI to choose which categories to download.<br /><br />

The mapping between WordNet ID and words for all synsets in this 
[link](http://image-net.org/archive/words.txt) from ImageNet.<br />


