from __future__ import print_function
from builtins import str
from wikimarkup.parser import Parser
import re
from wikitools import wiki, api

parser = Parser()

def galleryTagHook(parser_env, body, attributes={}):
    widths = attributes.get('widths')
    if widths:
        widths = re.sub('px', '', widths)
        gal_width = int(widths)
    else:
        gal_width = 155
        
    heights = attributes.get('heights')
    if heights:
        heights = re.sub('px', '', heights)
        def_image = int(heights)
    else:
        def_image = 120
    
    start_text = ''
    if attributes.get('mode', None) == 'packed':
        start_text = '<ul class="gallery mw-gallery-packed">'
        files = body.split('\n')
        for file in files:
            if file.strip() != '':
                res = file.split('|')
                filename = res[0].strip()
                
                site = wiki.Wiki('https://en.wikipedia.org/w/api.php')
                
                params = {'action': 'query', 'titles': filename,'prop': 'imageinfo', 'iiprop': 'url|thumbmime', 'iiurlheight': 131}
                request = api.APIRequest(site, params)
                result = request.query()
                try:
                    url = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumburl']
                    desc_url = list(result['query']['pages'].values())[0]['imageinfo'][0]['descriptionurl']
                    width = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbwidth']
                    height = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbheight']
                except:
                    continue
                text = '<li class="gallerybox" style="width: %spx"><div style="width: %spx">' % (float(int(width)) + 1.496, float(int(width)) + 1.496)
                text += '<div class="thumb" style="width: %spx;"><div style="margin:0px auto;">' % (float(int(width)) + 0.496)
                
                text += '<a href="%s" class="image"><img src="%s" width="%s" height="%s"></a>' % (desc_url, url,
                                                                                                  width,
                                                                                                  height)
                text += '</div></div></div><div class="gallerytext"><p>'
                if res[1] == 'thumb':
                    inner_text = '|'.join(res[2:]).strip()
                else:
                    inner_text = '|'.join(res[1:]).strip()
                text += parser.parse(inner_text)
                text += '</p></div></li>'
                start_text += text
    elif attributes.get('mode', None) == 'nolines':
        start_text = '<ul class="gallery mw-gallery-nolines">'
        
        if not attributes.get('widths'):
            gal_width = 125

        files = body.split('\n')
        for file in files:
            if file.strip() != '':
                res = file.split('|')
                filename = res[0].strip()
                
                site = wiki.Wiki('https://en.wikipedia.org/w/api.php')
                params = {'action': 'query', 'titles': filename,'prop': 'imageinfo', 'iiprop': 'url|thumbmime', 'iiurlwidth': gal_width-5}
                request = api.APIRequest(site, params)
                result = request.query()
                try:
                    url = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumburl']
                    desc_url = list(result['query']['pages'].values())[0]['imageinfo'][0]['descriptionurl']
                    width = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbwidth']
                    height = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbheight']
                except:
                    continue
                
                ratio = float(float(width)/float(height))
                
                if height > def_image:
                    height = def_image
                    width = ratio * def_image
                
                text = '<li class="gallerybox" style="width: %spx"><div style="width: %spx">' % (gal_width, gal_width)
                text += '<div class="thumb" style="width: %spx;"><div style="margin:0px auto;">' % (gal_width-5)
                
                text += '<a href="%s" class="image"><img src="%s" width="%s" height="%s"></a>' % (desc_url, url,
                                                                                                  width,
                                                                                                  height)
                text += '</div></div></div><div class="gallerytext"><p>'
                if res[1] == 'thumb':
                    inner_text = '|'.join(res[2:]).strip()
                else:
                    inner_text = '|'.join(res[1:]).strip()
                text += parser.parse(inner_text)
                text += '</p></div></li>'
                start_text += text
    else:   
        start_text = '<ul class="gallery mw-gallery-traditional">'
        files = body.split('\n')
        for file in files:
            if file.strip() != '':
                res = file.split('|')
                filename = res[0].strip()
                
                site = wiki.Wiki('https://en.wikipedia.org/w/api.php')
                params = {'action': 'query', 'titles': filename,'prop': 'imageinfo', 'iiprop': 'url|thumbmime', 'iiurlwidth': gal_width-35}
                request = api.APIRequest(site, params)
                result = request.query()
                try:
                    url = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumburl']
                    desc_url = list(result['query']['pages'].values())[0]['imageinfo'][0]['descriptionurl']
                    width = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbwidth']
                    height = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbheight']
                except:
                    continue
                
                ratio = float(float(width)/float(height))
                
                if height > def_image:
                    height = def_image
                    width = ratio * def_image
                
                
                text = '<li class="gallerybox" style="width: %spx"><div style="width: %spx">' % (gal_width, gal_width)
                text += '<div class="thumb" style="width: %spx;"><div style="margin:%spx auto;">' % (gal_width-5, float(gal_width-height)/2.0)
                
                text += '<a href="%s" class="image"><img src="%s" width="%s" height="%s"></a>' % (desc_url, url,
                                                                                                  width,
                                                                                                  height)
                text += '</div></div></div><div class="gallerytext"><p>'
                if len(res) > 1 and res[1] == 'thumb':
                    # need to test length because of cases like https://en.wikipedia.org/wiki/Talk:Federal_Assault_Weapons_Ban/Archive_2#RfC:_Is_inclusion_of_the_word_.22cosmetic.22_in_the_Criteria_section_appropriate.3F
                    inner_text = '|'.join(res[2:]).strip()
                else:
                    inner_text = '|'.join(res[1:]).strip()
                text += parser.parse(inner_text)
                text += '</p></div></li>'
                start_text += text
    start_text += '</ul>'
    return start_text
            
parser.registerTagHook('gallery', galleryTagHook)

def slinkHook(parser_env, namespace, body):
    print(body)
    vals = body.split('|')
    href = vals[1].strip()
    text = href[1:]
    return '<a href="%s">&#167; %s</a>' % (vals[1], text)
    
def linkHook(parser_env, namespace, body):
    (article, pipe, text) = body.partition('|') 
    href = article.strip().capitalize().replace(' ', '_') 
    text = (text or article).strip() 
    if not text.startswith('comment_'):
        return '<a href="http://en.wikipedia.org/wiki/%s">%s</a>' % (href, text)
    else:
        return '[[' + str(body) + ']]'

def userHook(parser_env, namespace, body):
    (article, pipe, text) = body.partition('|') 
    href = article.strip().capitalize().replace(' ', '_') 
    text = (text or article).strip() 
    return '<a href="http://en.wikipedia.org/wiki/User:%s">%s</a>' % (href, text)

def fileHook(parser_env, namespace, body):
    (file_name, pipe, size) = body.partition('|') 
    size_match = re.search('[1-9][0-9]{0,3}' , size)
    if size_match:
        size = size_match.group(0)
    else:
        size = '20'
    site = wiki.Wiki('https://en.wikipedia.org/w/api.php')
    params = {'action': 'query', 'titles': 'File:' + file_name,'prop': 'imageinfo', 'iiprop': 'url|thumbmime', 'iiurlwidth': size}
    request = api.APIRequest(site, params)
    result = request.query()
    try:
        url = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumburl']
        desc_url = list(result['query']['pages'].values())[0]['imageinfo'][0]['descriptionurl']
        width = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbwidth']
        height = list(result['query']['pages'].values())[0]['imageinfo'][0]['thumbheight']
    except:
        return file_name
    text = '<a href="%s" class="image">' % desc_url
    text += '<img alt="%s" src="%s" width="%s" height="%s"></a>' % (file_name, url, width, height)
    return text

def userTalkHook(parser_env, namespace, body):
    (article, pipe, text) = body.partition('|') 
    href = article.strip().capitalize().replace(' ', '_') 
    text = (text or article).strip() 
    return '<a href="http://en.wikipedia.org/wiki/User_talk:%s">%s</a>' % (href, text)

def pingTempHook(parser_env, namespace, body): 
    names = body.split('|') 
    text = []
    for name in names:
        text.append('<a href="http://en.wikipedia.org/wiki/User:%s">%s</a>' % (name, name))
    return '@' + ', '.join(text)

def quoteHook(parser_env, namespace, body):
    return '<span class="inline-quote-talk" style="font-family: Georgia, \'DejaVu Serif\', serif; color: #008560;">%s</span>' % body

def quote2Hook(parser_env, namespace, body):
    return '<span class="inline-quote-talk" style="font-family: Georgia, \'DejaVu Serif\', serif; color: #8B0000;">%s</span>' % body


def archiveHook(parser_env, namespace, body):
    return 'Archived: <p style="background-color: #ffffff;">%s</p>' % body

def quoteBoxHook(parser_env, namespace, body):
    res = body.split('\n')
    for item in res:
        i = item.split('=')
        quote_head = re.sub('\|', '', i[0]).strip().lower()
        if quote_head == 'quote':
            quote = i[1].strip()
            return '<p style="background-color: #ffffff;">%s</p>' % quote

def highlightHook(parser_env, namespace, body):
    text = '<span style="margin-right: 0.4em; padding: 3px 4px 2px; background-color: yellow; border: 1px; -moz-border-radius: 3px; -webkit-border-radius: 3px; border-radius: 3px;; box-shadow: 0.1em 0.1em 0.25em rgba(0,0,0,0.75); -moz-box-shadow: 2px 2px 4px #A0A080; -webkit-box-shadow: 2px 2px 4px #A0A080; box-shadow: 2px 2px 4px #A0A080;">'
    text += body
    text += '</span>'
    return text

def cotHook(parser_env, namespace, body):
    text = '<div style="background: #CCFFCC; font-size:87%; padding:0.2em 0.3em; text-align:center;">'
    text += body
    text += '</div>'
    return text

def colorHook(parser_env, namespace, body):
    (color, pipe, text) = body.partition('|') 
    return '<span style="color: %s">%s</span>' % (color, text)

def talkquoteHook(parser_env, namespace, body):
    text = '<blockquote>'
    print(body)
    res = body.split('=')
    res = '='.join(res[1:])
    res = res.split('|')
    
    text_lines = res[0].split('\n')
    for i in text_lines:
        text += '<p>' + i + '</p>'
    if len(res) == 2:
        info = res[1].split('=')
        if info[0] == 'by':
            text += '&nbsp;&nbsp;&nbsp;&nbsp; &mdash; User:' + '='.join(info[1:])
        elif info[0] == 'source':
            text += '&nbsp;&nbsp;&nbsp;&nbsp; &mdash; <i>' + '='.join(info[1:]) + '</i>'
    text += '</blockquote>'
    return text;

def emphHook(parser_env, namespace, body):
    return '<i>' + body + '</i>'

def pbHook(parser_env, namespace, body):
    print(parser_env)
    print(namespace)
    print(body)
    return '<br><br>'

def sndHook(parser_env, namespace, body):
    print(parser_env)
    print(namespace)
    print(body)
    return ' - '

def passThroughHook(parser_env, namespace, body):
    return body
    

parser.registerInternalLinkHook('*', linkHook)
parser.registerInternalLinkHook('user talk', userTalkHook)
parser.registerInternalLinkHook('user', userHook)
parser.registerInternalLinkHook('userlink', userHook)
parser.registerInternalLinkHook('file', fileHook)
parser.registerInternalLinkHook('slink', slinkHook)

parser.registerInternalTemplateHook('ping', pingTempHook)
parser.registerInternalTemplateHook('reply to', userHook)
parser.registerInternalTemplateHook('replyto', userHook)
parser.registerInternalTemplateHook('u', userHook)
parser.registerInternalTemplateHook('re', userHook)
parser.registerInternalTemplateHook('color', colorHook)
parser.registerInternalTemplateHook('cot', cotHook)
parser.registerInternalTemplateHook('tq2', quoteHook)
parser.registerInternalTemplateHook('tq', quoteHook)
parser.registerInternalTemplateHook('xt', quoteHook)
parser.registerInternalTemplateHook('!xt', quote2Hook)
parser.registerInternalTemplateHook('pb', pbHook)
parser.registerInternalTemplateHook('snd', sndHook)
parser.registerInternalTemplateHook('em', emphHook)
parser.registerInternalTemplateHook('archivetop', archiveHook)
parser.registerInternalTemplateHook('Quote', quoteBoxHook)
parser.registerInternalTemplateHook('quote box', quoteBoxHook)
parser.registerInternalTemplateHook('highlight round', highlightHook)
parser.registerInternalTemplateHook('rfc top', passThroughHook)
parser.registerInternalTemplateHook('outdent', passThroughHook)
parser.registerInternalTemplateHook('outindent', passThroughHook)
parser.registerInternalTemplateHook('talkquote', talkquoteHook)

