# Description
A spider to get image information from [Pixiv](pixiv.net)
# Why I write this
For some reason, I have to use some network techs to access this website, but you know, the ping of network is high, so I think if I can download it just text(url)? Then this program born.
## Why not Scrapy?
This repo is build from [GelbooruSpider](https://github.com/EnderCaster/GelbooruSpider)

# Usage
## help
```bash
    python app.py keyword
```
```bash
    # if you wanna to get R-18/R-18G please login and set the profile
    # then get your cookies,x-user-id in the F12 panel (network,xhr request)
    cp .Settings.py Settings.py
    # then paste it into Settings.py
    # if you wanna to unique the url
    python resolve_exists.py csv_file
    # and then it will resolve image infomation from csv_file.csv
    # or
    python resolve_exists.py 'csv file'
    # and then it will resolve image infomation from csv file.csv
```
## example
```bash
    python app.py honkai_impact_3rd
```
# Output
keyword.csv
## For Example
```bash
# if you input 
python app.py honkai_impact_3rd
# I will store the result into 
-rw-r--r-- 1 admin 197121  8628 11月 12 15:50 honkai_impact_3rd.csv
```