from bs4 import BeautifulSoup


IN_FN = r'..\mvvm.html'

soup = BeautifulSoup(open(IN_FN))

la = soup.find_all('a')
print la
