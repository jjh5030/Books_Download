from bs4 import BeautifulSoup
import urllib
import os.path
import urlparse
import sys

extensions_to_download = ['.pdf']
site_link = "http://stackoverflow.com/questions/194812/list-of-freely-available-programming-books"
pageFile = urllib.urlopen("http://stackoverflow.com/questions/194812/list-of-freely-available-programming-books")
pageHtml = pageFile.read()
pageFile.close()
 
soup = BeautifulSoup("".join(pageHtml))
sAll = soup.findAll("a")

site_list = []

try:
    os.makedirs("stackoverflow/")
except:
    pass

for link in soup.find_all('a'):
    if link.get('href') is not None:
        file_name = urlparse.urljoin(site_link,link.get('href'))        
        site_list.append(file_name)
        
for link in site_list:    
    if os.path.splitext(link)[1].lower() in extensions_to_download:      
        try:	
            file_name = link.split('/')[-1]        
            u = urllib.urlopen(link)
            f = open("stackoverflow/" + file_name.decode('utf8'), 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Attemping to Download: %s" % (file_name)
                
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

            f.close()
        except IOError:
            pass
        except KeyboardInterrupt:
            break
        except IndexError:
            pass
        except:
            print "ERROR", sys.exc_info()[0]
    else:
        pass