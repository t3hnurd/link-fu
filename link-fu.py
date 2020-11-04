'''
Tell search engine tracking links how you really feel!
Remove the junk and keep the main URL.

This is meant to be a light, portable program with minimal dependencies.
'''

import tkinter as tk
import urllib.parse as link

'''
List of target search engines (not all are supported yet)

Only Google and AOL/Yahoo! are supported right now. Not all may have tracking items to remove (startpage, duckduckgo?). Some may be difficult to circumvent (baidu, sogou?).

Can probably be expanded to other sites like Amazon, etc.
'''

engines=['aol', 'ask', 'baidu', 'bing', 'duckduckgo', 'ecosia', 'gigablast', 'google', 'lycos', 'mojeek', 'qwant', 'sogou', 'startpage', 'swisscows', 'yahoo', 'yandex', 'yippy']

def detect(source): # Determine the search engine site
    loc = link.urlparse(source).netloc
    for i in loc.split('.'):
        if i in engines:
            return i
    return 'unknown'

def convert(site, source): # Pull the referenced link without added crap
    url = link.urlparse(source)
    if (site == 'aol') or (site == 'yahoo'): # Both operated by Verizon Media
        unpacked = url.path.split('/')
        separated = {}
        for i in unpacked:
            separated.update(link.parse_qs(i))
        if separated['RU']:
            return ''.join(separated['RU'])
    elif site == 'google': # Grab the 'q' parameter
        if url.query:
            return ''.join(link.parse_qs(url.query)['q'])
    else: # Simply return the original source if nothing else
        return source

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.instructions = tk.Label(self, text="Toss a search engine \
link below and click to remove tracking crap.")
        self.instructions.pack(side="top")
        self.input = tk.Entry(self, width=40)
        self.input.pack(side="top")
        self.convert = tk.Button(self, text="FU-Convert", bg="red4", \
                fg="gray75", command=self.click)
        self.convert.pack(side="top")
        self.output = tk.Entry(self, width=40, state='disabled')
        self.output.pack(side="bottom")

    def click(self):
        dirtySource = self.input.get()
        self.output.config(state='normal')
        self.output.delete(0, 'end')
        self.output.insert(0, convert(detect(dirtySource), dirtySource))
        self.output.config(state='readonly')

root = tk.Tk()
root.title("Link-FU: The URL De-Crappifier")
app = Application(master=root)
app.mainloop()
