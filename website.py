
import bottle
import datetime
import random
global message
message = []
global subject
subject = []
global date
date = []
global rate
rate = []
global theme
theme = 'theme1.css'
global result
result = 0

def htmlify(title, content):
    global theme
    page = '<!DOCTYPE html>\n'
    page = page + '<html>\n'
    page = page + '  <head>\n'
    page = page + '    <link type="text/css" rel="stylesheet" href="static/' +theme+ '"/>\n'
    page = page + '    <title>' + title + '</title>\n'
    page = page + '    <meta charset="utf-8" />\n'
    page = page + '<div id="header"> <h6>Forum Discussion </h6></div>\n'
    page = page + '  </head>\n'
    page = page + '  <body>\n'
    page = page + '    ' + content + '\n<br>'
    page = page + ' <span id ="stylechanger"><br><a href="toggletheme"> Click </a> to toggle theme</span> \n'
    page = page + '  </body>\n'
    page = page + '</html>\n'
    return page

@bottle.route('/save',method='POST')
def save():
    global message
    global subject
    global date
    global rate
    tosavemes = bottle.request.POST.get('savemessage')
    tosavesub = bottle.request.POST.get('savesubject')
    captcha = bottle.request.POST.get('captcha')
    if result==int(captcha):
        message = message + [tosavemes]
        subject = subject + [tosavesub]
        date = date + [datetime.datetime.now()]
        rate = rate + [0]
        bottle.redirect('show')
    else:
        return htmlify('Ooops!','<h4>You are not a human! Get the hell out of here! <a href="/add"> Click </a> to go back.</h4>')

@bottle.route('/show')
def show():
    global message
    global subject
    global date
    htmltext = ''
    for i in range(0,len(message)):
        htmltext = htmltext + '<p><br>' + 'Subject name:' + str(subject[i]) +'<br><br>'+ 'Message:' +'<br>'+ str(message[i]) +'<a href="rateplus/' +str(i)+ '"> (+) </a> ' +str(rate[i])+ ' <a href="rateminus/' +str(i)+ '"> (-) </a><br>' + '<a href="delete/' +str(i)+ '"> Delete </a><br><span id="datetime">Post date and time</span> ' + str(date[i]) + '</p>'
    if(len(message) != 0):
        return htmlify('Messages','<h1>Posted messages are follows:</h1>' + htmltext + '<br><h3><a href="/add">Click to add comment.</a></h3><br><br><form action="/search" method="post"><input type="text" name="for" /><input type="submit" value="Search" /></form>')
    else:
        return htmlify('Messages','<h2>There is no message to show!</h2> <br><h3><a href="/add">Click</a> to add comment.</h3>')

@bottle.route('/delete/<name>')
def delete(name):
    a = int('%s' %name.title())
    del message[a]
    del subject[a]
    del date[a]
    del rate[a]
    bottle.redirect('/..')

@bottle.route('/rateplus/<name>')
def rateplus(name):
    a = int('%s' %name.title())
    rate[a] = rate[a]+1
    bottle.redirect('/..')

@bottle.route('/rateminus/<name>')
def rateminus(name):
    a = int('%s' %name.title())
    rate[a] = rate[a]-1
    bottle.redirect('/..')

@bottle.route('/toggletheme')
def toggletheme():
    global theme
    if theme == 'theme1.css':
        theme = 'theme2.css'
    else:
        theme = 'theme1.css'
    bottle.redirect('/..')

@bottle.route('/')
def default():
    bottle.redirect('show')

@bottle.route('/search',method='POST')
def search():
    global message
    global subject
    global date
    name = bottle.request.POST.get('for')
    htmltext = ''
    for j in range(0,len(subject)):
        found = subject[j].find(name)
        if found != -1:
            for i in range(0,len(message)):
                htmltext = htmltext + '<p><span id="' + str(i==j) + '"><b>'+ 'Subject name:' + str(subject[i]) +'<br><br>'+ 'Message:' +'<br>' + str(message[i]) + '</b><a href="rateplus/' +str(i)+ '"> (+) </a> ' +str(rate[i])+ ' <a href="rateminus/' +str(i)+ '"> (-) </a><br>' +'<a href="delete/' +str(i)+ '">  Delete  </a><br><span id="datetime">Post date and time</span> ' + str(date[i]) + '</span></p>'
            if(len(message) != 0):
                return htmlify('Messages','<h1>Posted messages are follows:</h1> ' + htmltext + '<br><h3><a href="/add">Click to add comment.</a></h3><br><br><br><form action="/search" method="post"><input type="text" name="for" /><input type="submit" value="Search" /></form>   ')
            else:
                return htmlify('Messages','There is no message to show <br><br/><h3><a href="/add">Click to add comment.</a></h3>')
    for j in range(0,len(subject)):
        found = message[j].find(name)
        if found != -1:
            for i in range(0,len(message)):
                htmltext = htmltext + '<p><span id="' + str(i==j) + '"><br>' + 'Subject name:' + str(subject[i]) +'<br><br>'+ 'Message:' +'<br>' + str(message[i]) + '<a href="rateplus/' +str(i)+ '"> (+) </a> ' +str(rate[i])+ ' <a href="rateminus/' +str(i)+ '"> (-) </a><br>' + '<a href="delete/' +str(i)+ '"> Delete  </a><br><span id="datetime">Post date and time</span> ' + str(date[i]) + '</span></p>'
            if(len(message) != 0):
                return htmlify('Messages','<h1>Posted messages are follows:</h1> ' + htmltext + '<br><h3><a href="/add">Click to add comment.</a></h3><br><br><br><form action="/search" method="post"><input type="text" name="for" /><input type="submit" value="Search" /></form>   ')
            else:
                return htmlify('Messages','There is no message to show! <br><h3><a href="/add">Click to add comment.</a></h3>')
    return htmlify('Search page','<h5>search term not found. <a href="/.."> click </a> to return. </h5>')

@bottle.route("/static/<filename>")
def mycss(filename):
    return bottle.static_file(filename,root="/home/artunc/mysite/static/")

@bottle.route('/add')
def add():
    global result
    a = random.randint(1, 40)
    b = random.randint(1, 50)
    result = a+b

    return htmlify('Start page','''
    <p id="adder">You can add your messages and subjects down:</p>
    <form action="/save" method="post">
    Subject:<br><br>
    <input type="text" name="savesubject" /><br>
    Message:<br><br>
    <input type="text" name="savemessage" /><br>
    <span id="captcha">Prove that you are a human being What is:</span> <div id="captcha"> ''' + str(a) + ''' + ''' + str(b) +  '''
    ?</div> <input type="text" name="captcha" /><br><br><input type="submit" value="Submit" />
    </form>
    ''')


application = bottle.default_app()

