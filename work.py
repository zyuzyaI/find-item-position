import csv
import requests 
from bs4 import BeautifulSoup
from multiprocessing import Pool
import multiprocessing.pool
import multiprocessing

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

# Main class
class GetTagPosition:
	def  __init__(self, url):
		self.url = url 
		
		with open("file.csv", "w"):
			pass
		self.tags, self.shop_name = self.getTags()
		if self.tags:
			p = MyPool(8)  # Pool tells how many at a time
			records = p.map(self.seachPage, self.tags)
			
	def getTags(self):
		# return list of searching tags and shop name
		html = requests.get(self.url)
		if html.status_code == 200:  
			soup = BeautifulSoup(html.text, "lxml")
			try:
				find_tags = soup.find("div", id="wt-content-toggle-tags-read-more").find_all("a")
				shop_name = soup.find("div", class_="wt-mb-xs-1").text.strip()
				shop_name = shop_name.split()[0].strip()
				tags = [tag.text.strip() for tag in find_tags]
			except:
				tags = []
				shop_name = None
		else:
			tags = []
			shop_name = None
		return tags, shop_name

	def seachPage(self, tag):
		print("[INFO] searching tag: ", tag)
		url = "https://www.etsy.com/search?q={}&ref=pagination&page=1".format(tag)
		html = requests.get(url)
		if html.status_code == 200:
			soup = BeautifulSoup(html.text, "lxml")
			pagination = soup.find("div", class_="wt-show-lg")
			pagination_text = [k.text for k in  pagination.find_all("a")]
			total_page = max(int(p) for k in pagination_text for p in k.split() if p.isdigit())
			pages = total_page if total_page <= 30 else 30
			flag = False
			table_dct = {}
			for page in range(1, pages+1):
				print("page: ", page)
				if flag: 
					break
				if page != 1:
					url = "https://www.etsy.com/search?q={}&ref=pagination&page={}".format(tag, page)
					html = requests.get(url)
					soup = BeautifulSoup(html.text, "lxml")
				else:
					html = html
					soup = BeautifulSoup(html.text, "lxml")

				if html.status_code == 200:
					try:
						body = soup.find("ul", class_="responsive-listing-grid")
						items = body.find_all("li")
						for item in range(len(items)):
							shop = items[item].find("div", class_="v2-listing-card__shop").text.split()[0].strip()
							if shop == self.shop_name:
								title = items[item].find("h3", class_="text-gray").text.strip()
								position = item + 1
								table_dct["title"] = title 
								table_dct["tag"] = tag 
								table_dct["position"] = position + (page-1) * 48
								table_dct["page"] = page 
								table_dct["total_page"] = total_page
								self.makeTable(table_dct)
								flag = True 
								break
					except:
						continue
				else:
					continue
			if page == 30:
				# if items not on 30 pages
				table_dct["title"] = None 
				table_dct["tag"] = tag 
				table_dct["position"] = "> 1140"
				table_dct["page"] = "> 30" 
				table_dct["total_page"]= total_page	
				self.makeTable(table_dct)	

	# create csv file
	def makeTable(self, dct):
		print('saving....')
		name = "file.csv" 
		with open(name, 'a') as f:
				writer = csv.writer(f)
				writer.writerow((dct['tag'],
								dct['title'],
								dct['position'],
								dct['page'],
								dct['total_page']								
							))


if __name__ == "__main__":
	# run program
	GetTagPosition("https://www.etsy.com/listing/816119187/macrame-wall-hanging-boho-style-modern?ref=shop_home_active_1&frs=1")