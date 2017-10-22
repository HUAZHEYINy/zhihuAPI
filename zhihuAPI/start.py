from scrapy import cmdline
#1.use this line to create a scrapy project.
#2. since the cmdline will execute list of arguments, so we should use split() to split it by space.
#3. we can start develop web crawler.
#cmdline.execute("scrapy startproject zhihuAPI".split())

#4. use this line to execute ur spider
cmdline.execute("scrapy crawl zhihu".split())