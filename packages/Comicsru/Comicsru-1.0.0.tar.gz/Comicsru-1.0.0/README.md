# Comicsru
A package to search and download comics from https://readcomicsonline.ru in cbz and many more formats
## Installation
```sh
pip install Comicsru
```
## Usage
```py
import Comicsru

#download comic
download_url = 'https://readcomicsonline.ru/comic/deadpool-back-in-black-2016/1'
Comicsru.download_comic(download_url,'cbz') #only cbz,zip,jpg formats supported

#suggest a random comic
print(Comicsru.suggest_random()) #prints a random comic title

#show summary of a comic
title = 'the-punisher-2016' #use '-' instead of spaces
about_comic = Comicsru.get_summary(title)
print(about_comic)

```
## Todo
- [ ] Add more formats (rar,cbz,pdf)
- [ ] Download all chapters at once
- [ ] More features