from bs4 import BeautifulSoup

html_content="<html><body><p>Hello, Beautiful Soup!</p></body></html>"

soup=BeautifulSoup(html_content,'html.parser')

paragraph_text=soup.find('p').text
print(paragraph_text)

html_content1="""
<html>
<head>
   <title>Example page</title>
</head>
<body>
   <h1>Welcome to Beautiful Soup</h1>
   <p class="intro">Beautiful Soup makes web scraping easy</p>
   <div id="content">
   <p>Here are some links:</p>
   <a href="http://example.com/page1">Link 1</a>
   <a href="http://example.com/page2">Link 2</a>
   <a href="http://example.com/page3">Link 3</a>
   </div>
</body>
</html>
"""
soup1=BeautifulSoup(html_content1,'html.parser')
print("Title of the page:",soup1.title.text)

intro_text=soup1.find('p',class_="intro").text
print("Intro text:",intro_text)

div_content=soup1.find('div',id='content')
links=div_content.find_all('a')
for link in links:
    print("Link:",link['href'])

first_link=soup1.find('a')
print("First link text:",first_link.text)

print("Next sibling of the first link:",first_link.next_sibling)

paragraphs=soup1.select('div#content p')
for paragraph in paragraphs:
    print('Paragraph inside content:',paragraph.text)

new_tag=soup1.new_tag('b')
new_tag.string="Important"
soup1.h1.append(new_tag)
print("Modified h1 tag:",soup1.h1)

