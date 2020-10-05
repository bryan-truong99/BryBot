import urllib.request
import re

search_keyword="playboi carti whole lotta red"
search_keyword = search_keyword.replace(" ", "+")
html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
print("https://www.youtube.com/watch?v=" + video_ids[0])
