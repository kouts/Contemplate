# -*- coding: UTF-8 -*-
##
#  Contemplate
#  Light-weight Templating Engine for PHP, Python, Node and client-side JavaScript
#
#  @version 0.6.3
#  https://github.com/foo123/Contemplate
#
#  @inspired by : Simple JavaScript Templating, John Resig - http://ejohn.org/ - MIT Licensed
#  http://ejohn.org/blog/javascript-micro-templating/
#
##

# needed imports
import os, sys, re, time, datetime, calendar, codecs

# http://docs.python.org/2/library/collections.html#collections.OrderedDict
# http://code.activestate.com/recipes/576693/
#try:
#    import collections.OrderedDict
#    ODict = collections.OrderedDict
#except ImportError:
#    ODict = dict

ODict = dict

try:
    # Python 3.x
    import html
    __htmlent__ = html
    __ENT_COMPAT__ = False
    
    # http://www.php2python.com/wiki/function.stripslashes/
    # http://tech.7starsea.com/post/203
    # static
    def stripslashes(s):
        return codecs.decode(s, 'unicode_escape')
        

except ImportError:
    # Python 2.x
    import cgi
    __htmlent__ = cgi
    __ENT_COMPAT__ = True
    
    # http://www.php2python.com/wiki/function.stripslashes/
    # static
    def stripslashes(s):
        return s.decode('string_escape')

try:
    # Python 3.x
    import urllib.parse
    __urlencode__ = urllib.parse
except ImportError:
    # Python 2.x
    import urllib
    __urlencode__ = urllib

    

# (protected) global properties
class _G:

    isInited = False
    cacheDir = './'
    cacheMode = 0
    cache = {}
    templates = {}
    inlines = {}
    partials = {}
    locale = {}
    plurals = {}

    leftTplSep = "<%"
    rightTplSep = "%>"
    preserveLinesDefault = "' + \"\\n\" + '"
    preserveLines = ''
    escape = True
    EOL = "\n"
    TEOL = os.linesep
    tplStart = ''
    tplEnd = ''
    tplPrefixCode = ''

    pad = "    "
    level = 0
    loops = 0
    ifs = 0
    loopifs = 0
    blocks = []
    allblocks = []
    blockcnt = 0
    extends = None
    id = 0
    funcId = 0
    stack = None
    uuid = 0

    NEWLINE = None
    NL = None

    ALPHA = r'^[a-zA-Z_]'
    NUM = r'^[0-9]'
    ALPHANUM = r'^[a-zA-Z0-9_]'
    SPACE = r'^\s'
    
    regExps = {
        'specials' : None,
        'replacements' : None,
        'functions' : None,
        'controls' : None,
        'controls2' : None
    }

    controlConstructs = [
        'include', 'template', 
        'extends', 'endblock', 'block',
        'elsefor', 'endfor', 'for',
        'set', 'unset', 'isset',
        'elseif', 'else', 'endif', 'if'
    ]

    funcs = [
        'htmlselect', 'htmltable',
        'plugin_([a-zA-Z0-9_]+)', 'haskey',
        'lowercase', 'uppercase', 'camelcase', 'snakecase', 'pluralise',
        'concat', 'ltrim', 'rtrim', 'trim', 'sprintf', 'addslashes', 'stripslashes',
        'tpl', 'uuid',
        'html', 'url', 'count', 
        'ldate', 'date', 'now', 'locale',
        'dq', 'q', 'l', 's', 'n', 'f' 
    ]

    plugins = {}
            
    # generated tpl class code as a heredoc template
    tplClassCode = """\
# -*- coding: UTF-8 -*-
# Contemplate cached template '__{{ID}}__'

__{{PREFIX_CODE}}__

# imports start here, if any
__{{IMPORTS}}__
# imports end here

def __getTplClass__(Contemplate):

    # extends the main Contemplate class
    class __{{CLASSNAME}}__(Contemplate):
        'Contemplate cached template __{{ID}}__'

        # constructor
        def __init__(self, id=None, __=None):
            # initialize internal vars
            self.id = None 
            self.data = None 
            self._renderFunction = None 
            self._parent = None  
            self._blocks = None 

            self.id = id 
            
            # parent tpl assign code starts here
__{{PARENTCODE}}__
            # parent tpl assign code ends here



        # tpl-defined blocks render code starts here
__{{BLOCKS}}__
        # tpl-defined blocks render code ends here

        # render a tpl block method
        def renderBlock(self, block, __instance__=None):
            if ( not __instance__ ): __instance__ = self

            method = '_blockfn_' + block

            if (hasattr(self, method) and callable(getattr(self, method))): 
                return getattr(self, method)(__instance__)

            elif self._parent is not None: 
                return self._parent.renderBlock(block, __instance__)

            return ''
            
        
        # tpl render method
        def render(self, data, __instance__=None):
            __p__ = '' 
            if ( not __instance__ ): __instance__ = self

            if self._parent is not None: 
                __p__ = self._parent.render(data, __instance__)

            else: 
                # tpl main render code starts here
__{{RENDERCODE}}__
                # tpl main render code ends here

            self.data = None 
            return __p__
    
    return __{{CLASSNAME}}__

# allow to 'import *'  from this file as a module
__all__ = ['__getTplClass__']        
"""
    
    # generated tpl block method code as a heredoc template
    tplBlockCode = """
# tpl block render method for block '__{{BLOCK}}__'
def __{{BLOCKMETHOD}}__(self, __instance__):
__{{BLOCKMETHODCODE}}__
"""

    
    # generated IF code
    IF = """
if ( __{{COND}}__ ):
"""
    
    # generated ELSEIF code
    ELSEIF = """
elif ( __{{COND}}__ ):
"""

    # generated ELSE code
    ELSE = """
else:
"""
    
    # generated ENDIF code
    ENDIF = """
"""
    
    # a = [51,27,13,56]   dict(enumerate(a))
    # generated FOR code
    FOR = """
__{{O}}__ = __{{FOR_EXPR_O}}__
if ( len(__{{O}}__) > 0  ):
    # be able to use both key/value in loop
    __{{ASSIGN11}}__
    __{{ASSIGN12}}__
    for  __{{K}}__,__{{V}}__ in __{{LoopO}}__ :
        __{{ASSIGN21}}__
        __{{ASSIGN22}}__
"""
    
    # generated ELSEFOR code
    ELSEFOR = """
else:
"""
    
    # generated ENDFOR code
    ENDFOR1 = """
"""
    
    # generated ENDFOR code
    ENDFOR2 = """
"""
    
    # generated block code snippet
    DOBLOCK = """
__p__ = ''
__{{CODE}}__
return __p__
"""

    
    # generated dynamic render code
    TFUNC1 = "return ''"

    # generated dynamic render code
    TFUNC2 = """
__p__ = '' 
__{{CODE}}__
return __p__
"""

    RCODE1 = "__p__ = ''"
    
    RCODE2 = """
__instance__.data = Contemplate.data( data )
__{{CODE}}__
"""

#def backupOptions( ):
#    global _G
#    optionsBackUp = [
#        _G.cacheDir,
#        _G.cacheMode,
#        _G.leftTplSep,
#        _G.rightTplSep,
#        _G.preserveLines
#    ]
#    return optionsBackUp
#
#def restoreOptions( optionsBackUp ):
#    global _G
#    _G.cacheDir = optionsBackUp[ 0 ]
#    _G.cacheMode = optionsBackUp[ 1 ]
#    _G.leftTplSep = optionsBackUp[ 2 ]
#    _G.rightTplSep = optionsBackUp[ 3 ]
#    _G.preserveLines = optionsBackUp[ 4 ]
    
def getSeparators( text, separators=None ):
    global _G
    if separators:
        seps = separators.strip( ).split( " " )
        _G.leftTplSep = seps[ 0 ].strip( )
        _G.rightTplSep = seps[ 1 ].strip( )
    else:
        # tpl separators are defined on 1st (non-empty) line of tpl content
        lines = text.split( "\n" )
        while  len(lines)>0 and 0 == len( lines[ 0 ].strip() ): lines.pop( 0 )
        if len(lines):
            seps = lines.pop( 0 ).strip( ).split( " " )
            _G.leftTplSep = seps[ 0 ].strip( )
            _G.rightTplSep = seps[ 1 ].strip( )
        
        text = "\n".join( lines )
    return text
    

#
# Control structures
#

# whether var is set
def t_isset(varname):
    return ' ( "' + varname + '__RAW__" in __instance__.data ) '
        
# set/create/update tpl var
def t_set(args):
    global _G
    args = args.split(',')
    varname = args.pop(0).strip()
    expr = ','.join(args).strip()
    return "';" + _G.TEOL + padLines( varname + ' = ('+ expr +')' ) + _G.TEOL

# unset/remove/delete tpl var
def t_unset(varname=None):
    global _G
    if varname:
        varname = str(varname).strip()
        return "';" + _G.TEOL + padLines( 'if ( "'+varname+'__RAW__" in __instance__.data ): del ' + varname ) + _G.TEOL
    return "'; " + _G.TEOL
    
# if
# static
def t_if(cond='False'):
    global _G
    _G.ifs += 1
    
    out = "' "
    out1 = _G.IF.replace('__{{COND}}__', cond)
    out += padLines(out1)
    _G.level += 1
    
    return out
    
# elseif    
# static
def t_elseif(cond='False'):
    global _G
    out = "' "
    out1 = _G.ELSEIF.replace('__{{COND}}__', cond)

    _G.level -= 1
    out += padLines(out1)
    _G.level += 1
    
    return out
    
# else
# static
def t_else(args=''):
    global _G
    out = "' "
    out1 = _G.ELSE
    
    _G.level -= 1
    out += padLines(out1)
    _G.level += 1
    
    return out

# endif
# static
def t_endif(args=''):
    global _G
    _G.ifs -= 1
    
    out = "' "
    out1 = _G.ENDIF
    
    _G.level -= 1
    out += padLines(out1)
    
    return out
    
# for, foreach
# static
def t_for(for_expr):
    global _G
    _G.loops += 1  
    _G.loopifs += 1
    for_expr = for_expr.split(' as ')
    exprO = for_expr[0].strip()
    kv = for_expr[1].split('=>')
    k = kv[0].strip() + '__RAW__'
    v = kv[1].strip() + '__RAW__'
    
    _G.id += 1
    loopo = '_loopObj' + str(_G.id)
    _G.id += 1
    o = '_loopObj' + str(_G.id)
    forReplace = {
        '__{{FOR_EXPR_O}}__' : exprO,
        '__{{O}}__' : o,
        '__{{K}}__' : k,
        '__{{V}}__' : v,
        '__{{LoopO}}__' : loopo,
        '__{{ASSIGN11}}__' : 'if isinstance('+o+', list): '+loopo+' = enumerate('+o+')',
        '__{{ASSIGN12}}__' : 'else: '+loopo+' = '+o+'.items()',
        '__{{ASSIGN21}}__' : '__instance__.data[\''+k+'\'] = '+k+'',
        '__{{ASSIGN22}}__' : '__instance__.data[\''+v+'\'] = '+v+''
    }
    
    out1 = _G.FOR
    for k in forReplace:  out1 = out1.replace( k, forReplace[k] )
    
    out = "' "
    
    out += padLines(out1)
    _G.level += 2
    
    return out

# elsefor
# static
def t_elsefor(args=''):
    # else attached to  for loop
    global _G
    _G.loopifs -= 1
    out = "' "
    out1 = _G.ELSEFOR
    
    _G.level += -2
    out += padLines(out1)
    _G.level += 1
    
    return out
    
# endfor
# static
def t_endfor(args=''):
    global _G
    out = "' "
    if _G.loopifs == _G.loops:
        _G.loops -= 1 
        _G.loopifs -= 1
        
        out1 = _G.ENDFOR1
        
        _G.level += -2
        out += padLines(out1)
        
        return out
    
    _G.loops -= 1
    out1 = _G.ENDFOR2
    
    _G.level += -1
    out += padLines(out1)
    
    return out

# include file
# static
def t_include(id):
    global _G
    # cache it
    if id not in _G.partials:
        pushState()
        resetState()
        _G.partials[id] = " " + parse(getSeparators( Contemplate.getTemplateContents(id) ), False) + "' " + _G.TEOL
        popState()
    
    return padLines( _G.partials[id] )

# include template
# static
def t_template(args):
    global _G
    args = args.split(',')
    id = args.pop(0).strip()
    obj = ','.join(args)
    return '\' + %tpl( "'+id+'", '+obj+' ) ' + _G.TEOL

# extend another template
# static
def t_extends(tpl):
    global _G
    _G.extends = tpl
    return "' " + _G.TEOL
    
# define (overridable) block
# static
def t_block(block):
    global _G
    block = block.strip()
    if block not in _G.allblocks:
        _G.allblocks.append(block)
    
    _G.blockcnt += 1
    _G.blocks.append(block)
    return "' +  __||" + block + "||__"  
    
# end define (overridable) block
# static
def t_endblock(args=''):
    global _G
    if _G.blockcnt>0:
        _G.blockcnt -= 1
        return "__||/" + _G.blocks.pop() + "||__"
    return ''


#
# auxilliary parsing methods
#

# static
def merge(m, *args): 
    numargs = len(args)
    if numargs < 1: return m
    
    merged = m
    
    for arg in args:
        # http://www.php2python.com/wiki/function.array-merge/
        merged = ODict(merged)
        merged.update(arg)
    
    return merged

# static
def split(s):
    global _G
    parts1 = s.split( _G.leftTplSep )
    l = len(parts1)
    parts = []
    for i in range(l):
        tmp = parts1[i].split( _G.rightTplSep )
        parts.append ( tmp[0] )
        if len(tmp) > 1: parts.append ( tmp[1] )
    
    return parts


# static
def parseControlConstructs(m):
    global _G
    ctrl = m.group(1) 
    args = m.group(2)
    
    if ('isset'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_isset(args)
    
    elif ('set'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_set(args)
    
    elif ('unset'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_unset(args)
    
    elif ('if'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_if(args)
    
    elif ('elseif'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_elseif(args)
    
    elif ('else'==ctrl): 
        return t_else(args)
    
    elif ('endif'==ctrl): 
        return t_endif(args)
    
    elif ('for'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_for(args)
    
    elif ('elsefor'==ctrl): 
        return t_elsefor(args)
    
    elif ('endfor'==ctrl): 
        return t_endfor(args)
    
    elif ('template'==ctrl): 
        # constructs in args, eg. isset
        args = re.sub(_G.regExps['controls2'], parseControlConstructs, args)
        return t_template(args)
    
    elif ('extends'==ctrl): 
        return t_extends(args)
    
    elif ('block'==ctrl): 
        return t_block(args)
    
    elif ('endblock'==ctrl): 
        return t_endblock(args)
    
    elif ('include'==ctrl): 
        return t_include(args)
    
    return m.group(0)

# static
def parseNestedBlocks(code, blocks=None):
    if blocks: bl = len(blocks)
    else: bl = 0
    
    if bl > 0:
        while bl>0:
            bl -= 1
            block = blocks[ bl ]
            delim1 = '__||' + block + '||__'
            delim2 = '__||/' + block + '||__'
            
            len1 = len(delim1)
            len2 = len1+1
            
            pos1 = code.find(delim1, 0) 
            pos2 = code.find(delim2, pos1+len1)
            
            replace = (0 <= pos1)
            while replace:
            
                # replace all occurances of the block on the current template, 
                # with the code found previously
                # in the 1st block definition
                code = code[0:pos1] + "__instance__.renderBlock( '" + block + "' ) " + code[pos2+len2:]
                
                
                pos1 = code.find(delim1, 0)
                replace = (0 <= pos1)
                if replace: pos2 = code.find(delim2, pos1+len1)
            
        
    return code

# static
def parseBlocks(s):
    global _G
    blocks = {} 
    bl = len(_G.allblocks)
    while bl:
        bl -= 1
        block = _G.allblocks[bl] #_G.allblocks.pop()
        delim1 = '__||' + block + '||__' 
        delim2 = '__||/' + block + '||__'
        
        len1 = len(delim1) 
        len2 = len1+1 
        
        pos1 = s.find(delim1, 0) 
        pos2 = s.find(delim2, pos1+len1)
        
        code = s[pos1:pos2+len2]
        
        if len(code)>0:
            code = parseNestedBlocks(code[len1:-len2], _G.allblocks) #.replace("+ '' +", '+')  # remove redundant code
            
            bout = _G.DOBLOCK.replace('__{{CODE}}__', code+"'")
            
            blocks[block] = bout
        
        replace = (0 <= pos1)
        while replace:
            # replace all occurances of the block on the current template, 
            # with the code found previously
            # in the 1st block definition
            s = s[0:pos1] + "__instance__.renderBlock( '" + block + "' ) " + s[pos2+len2:]
            
            
            pos1 = s.find(delim1, 0)
            replace = (0 <= pos1)
            if replace: pos2 = s.find(delim2, pos1+len1)
    
    _G.allblocks = []    
    return [ s, blocks ] #[ s.replace("+ '' +", '+'), blocks ]

def parseString(s, q, i, l):
    string = q
    escaped = False
    ch = ''
    while ( i < l ):
        ch = s[i]
        i += 1
        string += ch
        if ( q == ch and not escaped ):  break
        escaped = (not escaped and '\\' == ch)
    return string


def parseVariable(s, i, l, pre='VARSTR'):
    global _G
    
    if ( _G.ALPHA.match(s[i]) ):
    
        cnt = 0
        strings = {}
        variables = []
        space = 0
        
        
        # main variable
        variable = s[i]
        i += 1
        while ( i < l and _G.ALPHANUM.match(s[i]) ):
        
            variable += s[i]
            i += 1
        
        
        variable_raw = variable
        # transform into tpl variable
        variable = "__instance__.data['" + variable + "']"
        _len = len(variable_raw)
        
        # extra space
        space = 0
        while ( i < l and _G.SPACE.match(s[i]) ):
        
            space += 1
            i += 1
        
        
        bracketcnt = 0
        
        # optional properties
        while ( i < l and ('.' == s[i] or '[' == s[i]) ):
        
            delim = s[i]
            i += 1
            
            # extra space
            while ( i < l and _G.SPACE.match(s[i]) ):
            
                space += 1
                i += 1
            
        
            # alpha-numeric dot property
            if ( '.' == delim ):
            
                # property
                property = ''
                while ( i < l and _G.ALPHANUM.match(s[i]) ):
                
                    property += s[i]
                    i += 1
                
                lp = len(property)
                if ( lp ):
                
                    # transform into tpl variable bracketed property
                    variable += "['" + property + "']"
                    _len += space + 1 + lp
                    space = 0
                
                else:
                
                    break
                
            
            
            # bracketed property
            elif ( '[' == delim ):
            
                bracketcnt += 1
                
                ch = s[i]
                
                # literal string property
                if ( '"' == ch or "'" == ch ):
                
                    property = parseString( s, ch, i+1, l )
                    cnt += 1
                    strid = "__##"+pre+str(cnt)+"##__"
                    strings[ strid ] = property
                    variable += delim + strid
                    lp = len(property)
                    i += lp
                    _len += space + 1 + lp
                    space = 0
                
                
                # numeric array property
                elif ( _G.NUM.match(ch) ):
                
                    property = s[i]
                    i += 1
                    while ( i < l and _G.NUM.match(s[i]) ):
                    
                        property += s[i]
                        i += 1
                    
                    variable += delim + property
                    lp = len(property)
                    _len += space + 1 + lp
                    space = 0
                
                
                # sub-variable property
                elif ( '$' == ch ):
                
                    sub = s[i+1:]
                    subvariables = parseVariable(sub, 0, len(sub), pre + '_' + str(cnt) + '_');
                    if ( subvariables ):
                    
                        # transform into tpl variable property
                        property = subvariables[-1]
                        variable += delim + property[0][0]
                        lp = property[1]
                        i += lp + 1
                        _len += space + 2 + lp
                        space = 0
                        variables = variables + subvariables
                    
                
                
                # close bracket
                elif ( ']' == ch ):
                
                    if ( bracketcnt > 0 ):
                    
                        bracketcnt -= 1
                        variable += delim + s[i]
                        i += 1
                        _len += space + 2
                        space = 0
                    
                    else:
                    
                        break
                    
                
                
                else:
                
                    break
                
                
                
                # extra space
                while ( i < l and _G.SPACE.match(s[i]) ):
                
                    space += 1
                    i += 1
                
        
                # close bracket
                if ( ']' == s[i] ):
                
                    if ( bracketcnt > 0 ):
                    
                        bracketcnt -= 1
                        variable += s[i]
                        i += 1
                        _len += space + 1
                        space = 0
                    
                    else:
                    
                        break
                    
                
            
            
            # extra space
            while ( i < l and _G.SPACE.match(s[i]) ):
            
                space += 1
                i += 1
            
        
        
        variables.append( [[variable, variable_raw], _len, strings] )
        return variables
    
    return None


# static
def parse(tpl, withblocks=True):
    global _G
    
    def funcReplace(m):
        plugin = m.group(2) 
        if plugin and plugin in _G.plugins: 
            return 'Contemplate.plugin_' + plugin 
        else: 
            return 'Contemplate.' + m.group(1)
    
    parts = split( tpl )
    l = len(parts)
    isTag = False
    parsed = ''
    
    for i in range(l):
        s = parts[i]
        
        if isTag:
            
            tag = "\t" + re.sub( _G.regExps['specials'], " ", s ) + "\v" # replace special chars
            
            # parse each template tag section accurately
            # refined parsing
            count = len( tag )
            index = 0
            ch = ''
            out = ''
            cnt = 0
            variables = {}
            strings = {}
            while ( index < count ):
            
                ch = tag[index]
                index  += 1
                
                # parse mainly literal strings and variables
                
                # literal string
                if ( '"' == ch or "'" == ch ):
                
                    tok = parseString( tag, ch, index, count )
                    cnt += 1
                    id = "__##STR" + str(cnt) + "##__"
                    strings[ id ] = tok
                    out += id
                    index += len(tok)-1
                
                # variable
                elif ( '$' == ch ):
                
                    tok = parseVariable(tag, index, count)
                    if ( tok ):
                    
                        for tokv in tok:
                            cnt += 1
                            id = "__##VAR" + str(cnt) + "##__"
                            variables[ id ] = tokv[ 0 ]
                            strings.update( tokv[ 2 ] )
                        out += id
                        index += tokv[ 1 ]
                    
                    else:
                    
                        out += '$'
                    
                
                # rest, bypass
                else:
                
                    out += ch
                
            
            tag = out
                
            # fix literal data notation python-style
            tag = tag.replace('true', 'True').replace('false', 'False').replace('null', 'None').replace(' && ', ' and ').replace(' || ', ' or ').replace(' ! ', ' not ')
            
            tag = re.sub(_G.regExps['controls'], parseControlConstructs, tag)

            tag = re.sub( _G.regExps['functions'], funcReplace, tag )
            
            tag = re.sub( _G.regExps['replacements'], r"' + str( \1 ) + '", tag )
            
            for (id,variable) in variables.items():  
                tag = tag.replace( id+'__RAW__', variable[1] )
                tag = tag.replace( id, variable[0] )
            
            for (id,string) in strings.items():  
                tag = tag.replace( id, string )
            
            tag = tag.replace( "\t", _G.tplStart ).replace( "\v", padLines(_G.tplEnd) )
            
            s = tag
            isTag = False
            
        else:
            
            if _G.escape:
                s = s.replace( "\\", "\\\\" )  # escape escapes
                
            s = s.replace( "'", "\\'" )  # escape single quotes accurately (used by parse function)
            
            s = s.replace( "\n", _G.preserveLines ) # preserve lines
            #s = re.sub(_G.NL, _G.preserveLines, s) # preserve lines
            
            isTag = True
        
        parsed += s
    
    if withblocks: return parseBlocks(parsed)
    
    return parsed #.replace( "+ '' +", '+' ) # remove redundant code

# static
def getCachedTemplateName(id):
    return id.replace('-', '_').replace(' ', '_') + '_tpl' + '.py'

# static
def getCachedTemplateClass(id):
    return 'Contemplate_' + id.replace('-', '_').replace(' ', '_') + '_Cached'

# static
def createTemplateRenderFunction(id, seps=None):
    global _G
    resetState()
    
    blocks = parse(getSeparators( Contemplate.getTemplateContents(id), seps ))
    
    if _G.extends:
        func = _G.TFUNC1
    
    else:
        func = _G.TFUNC2.replace( '__{{CODE}}__', "__p__ += '" + blocks[0] + "'")
    
    _G.funcId += 1
    
    funcName = '_contemplateFn' + str(_G.funcId)
    fn = createFunction(funcName, '__instance__=None', padLines(func, 1), {'Contemplate': Contemplate})
    
    blockfns = {}
    for b,bc in blocks[1].items():
        funcName = '_contemplateBlockFn_' + b + '_' + str(_G.funcId)
        blockfns[b] = createFunction(funcName, '__instance__=None', padLines(bc, 1), {'Contemplate': Contemplate})
    
    return [ fn, blockfns]

# static
def createCachedTemplate(id, filename, classname, seps=None):
    global _G
    resetState()
    
    blocks = parse(getSeparators( Contemplate.getTemplateContents(id), seps ))
    
    # tpl-defined blocks
    sblocks = ''
    for b,bc in blocks[1].items():
        sblocks += _G.TEOL + _G.tplBlockCode.replace('__{{BLOCK}}__', b).replace('__{{BLOCKMETHOD}}__', "_blockfn_"+b).replace('__{{BLOCKMETHODCODE}}__', padLines(bc, 1))
    
    # tpl render code
    if _G.extends:
        parentCode = "self.setParent( '"+_G.extends+"' )"
        renderCode = _G.RCODE1
    
    else:
        parentCode = ''
        renderCode = _G.RCODE2.replace( '__{{CODE}}__', "__p__ += '" + blocks[0] + "'" )
    
    if _G.tplPrefixCode:
        prefixCode = _G.tplPrefixCode
    else:
        prefixCode = ''
        
    # generate tpl class
    classCode = _G.tplClassCode.replace('__{{PREFIX_CODE}}__', prefixCode).replace('__{{IMPORTS}}__', '').replace('__{{ID}}__', id).replace('__{{CLASSNAME}}__', classname).replace('__{{PARENTCODE}}__', padLines(parentCode, 3)).replace('__{{BLOCKS}}__', padLines(sblocks, 2)).replace('__{{RENDERCODE}}__', padLines(renderCode, 4))
    
    return Contemplate.write(filename, classCode)

# static
def getCachedTemplate(id, options=dict()):
    global _G
    # inline templates saved only in-memory
    if id in _G.inlines:
        # dynamic in-memory caching during page-request
        tpl = Contemplate()
        tpl.setId( id )
        fns = createTemplateRenderFunction(id, options['separators'])
        tpl.setRenderFunction( fns[0] )
        tpl.setBlocks( fns[1] )
        if _G.extends: tpl.setParent( Contemplate.tpl(_G.extends) )
        return tpl
    
    CM = _G.cacheMode
    
    if True != options['autoUpdate'] and CM == Contemplate.CACHE_TO_DISK_NOUPDATE:
    
        cachedTplFile = getCachedTemplateName(id)
        cachedTplPath = os.path.join(_G.cacheDir, cachedTplFile)
        cachedTplClass = getCachedTemplateClass(id)
        if not os.path.isfile(cachedTplPath):
            # if not exist, create it
            createCachedTemplate(id, cachedTplPath, cachedTplClass, options['separators'])
        if os.path.isfile(cachedTplPath):
            tpl = include(cachedTplFile, cachedTplClass)()
            tpl.setId( id )
            return tpl
        return None

    
    elif True == options['autoUpdate'] or CM == Contemplate.CACHE_TO_DISK_AUTOUPDATE:
    
        cachedTplFile = getCachedTemplateName(id)
        cachedTplPath = os.path.join(_G.cacheDir, cachedTplFile)
        cachedTplClass = getCachedTemplateClass(id)
        if not os.path.isfile(cachedTplPath) or (os.path.getmtime(cachedTplPath) <= os.path.getmtime(_G.templates[id])):
            # if tpl not exist or is out-of-sync (re-)create it
            createCachedTemplate(id, cachedTplPath, cachedTplClass, options['separators'])
        if os.path.isfile(cachedTplPath):
            tpl = include(cachedTplFile, cachedTplClass)()
            tpl.setId( id )
            return tpl
        return None
    
    else:
    
        # dynamic in-memory caching during page-request
        tpl = Contemplate()
        tpl.setId( id )
        fns = createTemplateRenderFunction(id, options['separators'])
        tpl.setRenderFunction( fns[0] )
        tpl.setBlocks( fns[1] )
        if _G.extends: tpl.setParent( Contemplate.tpl(_G.extends) )
        return tpl
    
    return None

# static
def setCachedTemplate(filename, tplContents): 
    return Contemplate.write(filename, tplContents)

# static
def _get_ordinal_suffix(n):
    # adapted from http://brandonwamboldt.ca/python-php-date-class-335/
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

# static
def _get_php_date(format, time):
    # http://php.net/manual/en/datetime.formats.date.php
    # http://strftime.org/
    # adapted from http://brandonwamboldt.ca/python-php-date-class-335/
    time  = datetime.datetime.fromtimestamp(time)
    timeStr = ''

    replacements = {}

    """ Day """
    replacements['d'] = str( time.day ).zfill(2)
    replacements['D'] = calendar.day_abbr[ time.weekday() ]
    replacements['j'] = str( time.day )
    replacements['l'] = calendar.day_name[ time.weekday() ]
    replacements['S'] = _get_ordinal_suffix( time.day )
    replacements['w'] = str( time.weekday() )
    replacements['z'] = str( time.timetuple().tm_yday )
    
    """ Week """
    replacements['W'] = str( time.isocalendar()[1] )
    
    """ Month """
    replacements['F'] = calendar.month_name[ time.month ]
    replacements['m'] = str( time.month ).zfill(2)
    replacements['M'] = calendar.month_abbr[ time.month ]
    replacements['n'] = str( time.month )
    replacements['t'] = str( calendar.monthrange(time.year, time.month)[1] )
    
    """ Year """
    replacements['L'] = str(int( calendar.isleap(time.year) ))
    replacements['Y'] = str( time.year )
    replacements['y'] = str( time.year )[2:]
    
    """ Time """
    replacements['a'] = time.strftime("%p").lower()
    replacements['A'] = time.strftime("%p")
    replacements['g'] = str( int(time.strftime("%I")) )
    replacements['G'] = str( int(time.strftime("%H")) )
    replacements['h'] = time.strftime("%I")
    replacements['H'] = time.strftime("%H")
    replacements['i'] = str( time.minute ).zfill(2)
    replacements['s'] = str( time.second ).zfill(2)
    replacements['u'] = str( time.microsecond )
    
    """ Timezone """
    replacements['e'] = "" #_self.get_timezone()
    replacements['I'] = str( time.dst() )
    
    #for regex, replace in replacements.items():
    #    format = format.replace(regex, replace)
    newformat = ''
    for c in format:
        if c in replacements:
            newformat += replacements[c]
        else:
            newformat += c

    return newformat
    
# static
def _localized_date(locale, format, timestamp):
    txt_words = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sun", "Mon", "Tues", "Wednes", "Thurs", "Fri", "Satur", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    date = _get_php_date(format, timestamp)
    
    # localize days/months
    for word in txt_words: 
        if word in locale: date = date.replace(word, locale[word])
        
    # return localized date
    return date

# static
def resetState():
    # reset state
    global _G
    _G.loops = 0 
    _G.ifs = 0 
    _G.loopifs = 0
    _G.blockcnt = 0 
    _G.blocks = []  
    _G.allblocks = [] 
    _G.extends = None
    _G.level = 0
    _G.id = 0
    #_G.funcId = 0

# static
def pushState():
    # push state
    global _G
    _G.stack.append([_G.loops, _G.ifs, _G.loopifs, _G.level,
    _G.blockcnt, _G.blocks,  _G.allblocks,  _G.extends])

# static
def popState():
    # pop state
    global _G
    t = _G.stack.pop()
    _G.loops = t[0] 
    _G.ifs = t[1] 
    _G.loopifs = t[2] 
    _G.level = t[3]
    _G.blockcnt = t[4] 
    _G.blocks = t[5]  
    _G.allblocks = t[6]  
    _G.extends = t[7]

# static
def padLines(lines, level=None):
    global _G
    if level is None:  level = _G.level
    
    if level >= 0:
        pad = _G.pad * level
        
        lines = re.split(_G.NEWLINE, lines)
        lenlines = len(lines)
        
        for i in range(lenlines):
            lines[i] = pad + lines[i]
        
        lines = _G.TEOL.join(lines)
    
    return lines

#
#  Auxilliary methods 
# (mostly methods to simulate php-like functionality needed by the engine)
#
# static
def include(filename, classname, doReload=False):
    # http://www.php2python.com/wiki/function.include/
    # http://docs.python.org/dev/3.0/whatsnew/3.0.html
    # http://stackoverflow.com/questions/4821104/python-dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported
    
    #_locals_ = {'Contemplate': Contemplate}
    #_globals_ = {'Contemplate': Contemplate}
    #if 'execfile' in globals():
    #    # Python 2.x
    #    execfile(filename, _globals_, _locals_)
    #    return _locals_[classname]
    #else:
    #    # Python 3.x
    #    exec(Contemplate.read(filename), _globals_, _locals_)
    #    return _locals_[classname]
    
    # http://docs.python.org/2/library/imp.html
    # http://docs.python.org/2/library/functions.html#__import__
    # http://docs.python.org/3/library/functions.html#__import__
    # http://stackoverflow.com/questions/301134/dynamic-module-import-in-python
    # http://stackoverflow.com/questions/11108628/python-dynamic-from-import
    # also: http://code.activestate.com/recipes/473888-lazy-module-imports/
    # using import instead of execfile, usually takes advantage of Python cached compiled code
    
    global _G
    getTplClass = None
    directory = _G.cacheDir
    # add the dynamic import path to sys
    os.sys.path.append(directory)
    currentcwd = os.getcwd()
    os.chdir(directory)   # change working directory so we know import will work
    
    if os.path.exists(filename):
        
        modname = filename[:-3]  # remove .py extension
        mod = __import__(modname)
        if doReload: reload(mod) # Might be out of date
        # a trick in-order to pass the Contemplate super-class in a cross-module way
        getTplClass = getattr( mod, '__getTplClass__' )
    
    # restore current dir
    os.chdir(currentcwd)
    # remove the dynamic import path from sys
    del os.sys.path[-1]
    
    # return the tplClass if found
    if getTplClass:  return getTplClass(Contemplate)
    return None

# static
def createFunction(funcName, args, sourceCode, additional_symbols=dict()):
    # http://code.activestate.com/recipes/550804-create-a-restricted-python-function-from-a-string/

    # The list of symbols that are included by default in the generated
    # function's environment
    SAFE_SYMBOLS = [
        "list", "dict", "enumerate", "tuple", "set", "long", "float", "object",
        "bool", "callable", "True", "False", "dir",
        "frozenset", "getattr", "hasattr", "abs", "cmp", "complex",
        "divmod", "id", "pow", "round", "slice", "vars",
        "hash", "hex", "int", "isinstance", "issubclass", "len",
        "map", "filter", "max", "min", "oct", "chr", "ord", "range",
        "reduce", "repr", "str", "type", "zip", "xrange", "None",
        "Exception", "KeyboardInterrupt"
    ]
    
    # Also add the standard exceptions
    __bi = __builtins__
    if type(__bi) is not dict:
        __bi = __bi.__dict__
    for k in __bi:
        if k.endswith("Error") or k.endswith("Warning"):
            SAFE_SYMBOLS.append(k)
    del __bi
    
    # Include the sourcecode as the code of a function funcName:
    s = "def " + funcName + "(%s):\n" % args
    s += sourceCode # this should be already properly padded

    # Byte-compilation (optional)
    byteCode = compile(s, "<string>", 'exec')  

    # Setup the local and global dictionaries of the execution
    # environment for __TheFunction__
    bis   = dict() # builtins
    globs = dict()
    locs  = dict()

    # Setup a standard-compatible python environment
    bis["locals"]  = lambda: locs
    bis["globals"] = lambda: globs
    globs["__builtins__"] = bis
    globs["__name__"] = "SUBENV"
    globs["__doc__"] = sourceCode

    # Determine how the __builtins__ dictionary should be accessed
    if type(__builtins__) is dict:
        bi_dict = __builtins__
    else:
        bi_dict = __builtins__.__dict__

    # Include the safe symbols
    for k in SAFE_SYMBOLS:
        
        # try from current locals
        try:
          locs[k] = locals()[k]
          continue
        except KeyError:
          pass
        
        # Try from globals
        try:
          globs[k] = globals()[k]
          continue
        except KeyError:
          pass
        
        # Try from builtins
        try:
          bis[k] = bi_dict[k]
        except KeyError:
          # Symbol not available anywhere: silently ignored
          pass

    # Include the symbols added by the caller, in the globals dictionary
    globs.update(additional_symbols)

    # Finally execute the Function statement:
    eval(byteCode, globs, locs)
    
    # As a result, the function is defined as the item funcName
    # in the locals dictionary
    fct = locs[funcName]
    # Attach the function to the globals so that it can be recursive
    del locs[funcName]
    globs[funcName] = fct
    
    # Attach the actual source code to the docstring
    fct.__doc__ = sourceCode
    
    # return the compiled function object
    return fct


#
# The Contemplate Engine Main Python Class
#
class Contemplate:
    """
    Contemplate Template Engine for Python,
    https://github.com/foo123/Contemplate
    """
    
    # constants (not real constants in Python)
    VERSION = "0.6.3"
    
    CACHE_TO_DISK_NONE = 0
    CACHE_TO_DISK_AUTOUPDATE = 2
    CACHE_TO_DISK_NOUPDATE = 4
    
    # set file encoding if needed, here (eg 'utf8')
    ENCODING = 'utf-8'
    
    #
    #  Instance template methods (for in-memory only templates)
    #
    def __init__(self, id=None, renderFunc=None):
        self.id = None
        self.data = None
        self._renderFunction = None
        self._parent = None
        self._blocks = None
        
        if id is not None:   
            self.id = id 
            self._renderFunction = renderFunc
    
    def setId(self, id=None):
        if id is not None: self.id = id
        
        return self
    
    def setParent(self, parent): 
        if parent:
            if isinstance(parent, str):
                self._parent = Contemplate.tpl( parent )
            else:
                self._parent = parent 
        
        return self
    
    def setBlocks(self, blocks): 
        if not self._blocks: self._blocks = {} 
        self._blocks = Contemplate.merge(self._blocks, blocks)
        
        return self
    
    def setRenderFunction(self, renderFunc=None): 
        if renderFunc: self._renderFunction = renderFunc
        
        return self
    
    def renderBlock(self, block, __instance__=None):
        if ( not __instance__ ): __instance__ = self
        
        if (self._blocks is not None) and (block in self._blocks):
            blockfunc = self._blocks[block]
            return blockfunc( __instance__ )
        
        elif self._parent is not None:
            return self._parent.renderBlock(block, __instance__)
        
        return ''
        
    
    def render(self, data, __instance__=None):
        __p__ = ''
        if ( not __instance__ ): __instance__ = self
        
        if self._parent is not None:  
            __p__ = self._parent.render(data, __instance__)
        
        elif self._renderFunction is not None: 
            # dynamic function
            __instance__.data = Contemplate.data( data )
            renderFunction = self._renderFunction
            __p__ = renderFunction( __instance__ )
        
        self.data = None
        return __p__
    
    #
    #
    #
    
    # static
    def init():
        
        global _G
        
        if _G.isInited: return
            
        _G.stack = []
        
        # pre-compute the needed regular expressions
        _G.regExps['specials'] = re.compile(r'[\n\r\v\t]')
        
        _G.regExps['replacements'] = re.compile(r'\t[ ]*(.*?)[ ]*\v')
        
        _G.regExps['controls'] = re.compile(r'\t[ ]*%(' + '|'.join(_G.controlConstructs) + ')[ ]*\((.*)\)')
        _G.regExps['controls2'] = re.compile(r'%(' + '|'.join(_G.controlConstructs) + ')[ ]*\((.*)\)')
        
        _G.regExps['functions'] = re.compile(r'%(' + '|'.join(_G.funcs) + ')')
            
        _G.NEWLINE = re.compile(r'\n\r|\r\n|\n|\r')
        _G.NL = re.compile(r'\n')
        
        _G.ALPHA = re.compile( _G.ALPHA )
        _G.NUM = re.compile( _G.NUM )
        _G.ALPHANUM = re.compile( _G.ALPHANUM )
        _G.SPACE = re.compile( _G.SPACE )
        
        _G.preserveLines = _G.preserveLinesDefault
        
        _G.tplStart = "' " + _G.TEOL
        _G.tplEnd = _G.TEOL + "__p__ += '"
        
        _G.isInited = True
    
    #
    # Main template static methods
    #
    
    # add custom plugins as template functions
    def addPlugin(name, handler):
        global _G
        plugin_name = 'plugin_' + str(name)
        setattr(Contemplate, plugin_name, handler)
        _G.plugins[ plugin_name ] = True
    
    # static
    def setPrefixCode(preCode=None):
        global _G
        if preCode:
            _G.tplPrefixCode = str(preCode)
    
    # static
    def setLocaleStrings(l): 
        global _G
        _G.locale = Contemplate.merge(_G.locale, l)
    
    # static
    def clearLocaleStrings(): 
        global _G
        _G.locale = {}
    
    # static
    def setPlurals(plurals): 
        global _G
        for singular in plurals:
            if plurals[ singular ] is None: 
                # auto plural
                plurals[ singular ] = str(singular) + 's'
        _G.plurals = Contemplate.merge(_G.plurals, plurals)
    
    # static
    def clearPlurals(): 
        global _G
        _G.plurals = {}
    
    # static
    def setTemplateSeparators(seps=None):
        global _G
        if seps:
            if 'left' in seps: _G.leftTplSep = str(seps['left'])
            if 'right' in seps: _G.rightTplSep = str(seps['right'])
    
    # static
    def setPreserveLines(bool=True): 
        global _G
        if bool:  
            _G.preserveLines = _G.preserveLinesDefault
        else: 
            _G.preserveLines = ''
    
    # static
    def setCacheDir(dir): 
        global _G
        _self = Contemplate
        _dir = _G.cacheDir = os.path.abspath(dir)
        
        initPyFile = os.path.join(_dir, '__init__.py')
        if not os.path.exists(initPyFile):
            _initPy_ = """\
# added by Contemplate.py Engine
# dummy Python __init__.py file
# used with Contemplate 'import'
# to include cached templates as modules, for optimization
"""
            _self.write(initPyFile, _initPy_)
            
        #if _dir not in os.sys.path:
        #    # allow to use 'import' in order to include cached templates
        #    os.sys.path.append(_dir)

    
    # static
    def setCacheMode(mode): 
        global _G
        _G.cacheMode = mode
    
    # static
    def clearCache(all=False): 
        global _G
        _G.cache = {}
        if all: _G.partials = {}
    
    # add templates manually
    # static
    def add(tpls, tplStr=None):
        global _G
        
        if isinstance(tpls, dict):
            _inlines = {}
            for tplID in tpls:
                if isinstance(tpls[ tplID ], (list, tuple)):
                    # unified way to add tpls both as reference and inline
                    # inline tpl, passed as array
                    if len( tpls[ tplID ][ 0 ] ):
                        _G.inlines[ tplID ] = tpls[ tplID ][ 0 ]
                    _inlines[ tplID ] = True
                    
            for tplID in _inlines: del tpls[ tplID ]
            _G.templates = Contemplate.merge(_G.templates, tpls)
        elif tpls and tplStr:
            _G.templates[tpls] = tplStr
    
    # add inline templates manually
    # static
    def addInline(tpls, tplStr=None):
        global _G
        
        if isinstance(tpls, dict):
            _G.inlines = Contemplate.merge(_G.inlines, tpls)
        elif tpls and tplStr:
            _G.inlines[tpls] = tplStr
        
    # return the requested template (with optional data)
    # static
    def tpl(id, data=None, options=None):
        global _G
        
        if not options: options = {}
        options = merge({
            'autoUpdate': False, 
            'refresh': False, 
            'escape': False,
            'separators': None
        }, options)
        
        if False == options['escape']: _G.escape = False
        else: _G.escape = True
        
        # Figure out if we're getting a template, or if we need to
        # load the template - and be sure to cache the result.
        if options['refresh'] or not (id in _G.cache): 
            
            _G.cache[ id ] = getCachedTemplate( id, options )
        
        tpl = _G.cache[ id ]
        
        # Provide some basic currying to the user
        if isinstance(data, dict): return str(tpl.render( data ))
        else: return tpl
    
    #
    # Basic template functions
    #
    
    # basic html escaping
    # static
    def html(s):
        # http://www.php2python.com/wiki/function.htmlentities/
        return __htmlent__.escape(s.encode('utf8'), __ENT_COMPAT__).encode('ascii', 'xmlcharrefreplace')
    
    # basic url escaping
    # static
    def url(s):
        # http://www.php2python.com/wiki/function.urlencode/
        return __urlencode__.quote_plus(s)
    
    # count items in array/list or object/dict
    # static
    def count(a):
        # http://www.php2python.com/wiki/function.count/
        return len(a)
    
    # check if (nested) keys exist in tpl variable
    def haskey(v, *args):
        if not v or not (isinstance(v, list) or isinstance(v, dict)): return False
        argslen = len(args)
        tmp = v
        for i in range(argslen):
        
            if args[i] not in tmp: return False
            tmp = tmp[args[i]]
        
        return True
        
    # quote
    # static
    def q(e):
        return "'" + e + "'"
    
    # double quote
    # static
    def dq(e):
        return '"' + e + '"'
    
    # to String
    # static
    def s(e):
        return str(e)
    
    # to Integer
    # static
    def n(e):
        return int(e)
    
    # to Float
    # static
    def f(e):
        return float(e)
    
    # http://www.php2python.com/wiki/function.addslashes/
    # static
    def addslashes(s):
        l = ["\\", '"', "'", "\0", ]
        s = str(s)
        for i in l:
            if i in s:  s = s.replace(i, '\\'+i)
        return s

    # http://www.php2python.com/wiki/function.stripslashes/
    # static
    def stripslashes(s):
        return stripslashes(s) 
    
    # Concatenate strings/vars
    # static
    def concat(*args):
        return ''.join(args)
        
    # Trim strings in templates
    # static
    def trim(s, charlist=None):
        if charlist: return s.strip(charlist)
        else: return s.strip()
    
    # static
    def ltrim(s, charlist=None):
        if charlist: return s.lstrip(charlist)
        else: return s.lstrip()
    
    # static
    def rtrim(s, charlist=None):
        if charlist: return s.rstrip(charlist)
        else: return s.rstrip()
    
    def ucfirst(s):
        return s[0].upper() + s[1:]#.lower()
        
    def lcfirst(s):
        return s[0].lower() + s[1:]#.upper()
        
    def lowercase(s):
        return str(s).lower()
    
    def uppercase(s):
        return str(s).upper()
    
    def camelcase(s, sep="_", capitalizeFirst=False):
        _self = Contemplate
        sep = str(sep)
        if capitalizeFirst:
            return "".join( map( _self.ucfirst, str(s).split( sep ) ) )
        else:
            return _self.lcfirst( "".join( map( _self.ucfirst, str(s).split( sep ) ) ) )
    
    def snakecase(s, sep="_"):
        sep = str(sep)
        return re.sub( r'([A-Z])', lambda m: sep + m.group(1), str(s) ).lower()
    
    # Sprintf in templates
    # static
    def sprintf(format, *args):
        numargs = len(args)
        if numargs>0:
            #format = args.pop(0)
            return format % args
        return ''
    
    #
    #  Localization functions
    #
    
    # current time in seconds
    # time, now
    # static
    def time():
        return int(time.time())
    
    # formatted date
    # static
    def date(format, time=None):
        if time is None: time = Contemplate.time() 
        return _get_php_date(format, time)
    
    # localized formatted date
    # static
    def ldate(format, time=None): 
        global _G
        if time is None: time = Contemplate.time() 
        return _localized_date(_G.locale, format, time)
        
    # locale, l
    # static
    def locale(e): 
        global _G
        if (e in _G.locale):
            return _G.locale[e]
        else:
            return e
    
    # pluralise
    def pluralise(singular, count): 
        global _G
        if (singular in _G.plurals):
            if (1 != count): return _G.plurals[singular]
            else: return singular
        return singular
    
    # generate a uuid
    def uuid(namespace='UUID'):
        global _G
        _G.uuid += 1
        return '_'.join( [ str(namespace), str(_G.uuid), str(int(time.time())) ] )
    
    #
    #  HTML elements
    #
    
    # html table
    # static
    def htmltable(data, options={}):
        _self = Contemplate
        # clone data to avoid mess-ups
        data = _self.merge({}, data)
        options = _self.merge({}, options)
        o='' 
        
        o="<table"
        
        if 'id' in options:
            o+=" id='"+str(options['id'])+"'"
        if 'class' in options:
            o+=" class='"+str(options['class'])+"'"
        if 'style' in options:
            o+=" style='"+str(options['style'])+"'"
        if 'data' in options:
            for k,v in options['data'].items():
                o+=" data-"+str(k)+"='"+str(v)+"'"
            
        o+=">"
            
        tk=''
        if ('header' in options) or ('footer' in options):
            tk="<td>"+'</td><td>'.join(data.keys())+"</td>"
            
        header=''
        if ('header' in options) and options['header']:
            header="<thead><tr>"+tk+"</tr></thead>"
            
        footer='';
        if ('footer' in options) and options['footer']:
            footer="<tfoot><tr>"+tk+"</tr></tfoot>"
        
        o+=header
        
        # get data rows
        vals=data.values()
        
        maxCol=0
        for i,col in  enumerate(vals):
            
            if not isinstance(col, list):  l=1
            else: l=len(col)
            
            if l>maxCol: maxCol=l
            
            
            
        rows={}
        for i,col in enumerate(vals):
        
            if not isinstance(col, list): colvals=[col]
            else: colvals=col[:]
            l=len(colvals)
            
            for j in range(l):
            
                if j not in rows: rows[j]=[''] * maxCol
                
                rows[j][i]=str(colvals[j])
        
        
        if 'odd' in options:
            class_odd=str(options['odd'])
        else:
            class_odd='odd'
        if 'even' in options:
            class_even=str(options['even'])
        else:
            class_even='even'
            
        # render rows
        
        odd=False
        l=len(rows)
        for i in range(l):
        
            if odd:
                o+="<tr class='"+class_odd+"'><td>"+'</td><td>'.join(rows[i])+"</td></tr>"
                odd=False
            else:
                o+="<tr class='"+class_even+"'><td>"+'</td><td>'.join(rows[i])+"</td></tr>"
                odd=True
            
        del rows
        
        o+=footer
        o+="</table>"
        return o
    
    # html select
    # static
    def htmlselect(data, options={}):
        _self = Contemplate
        # clone data to avoid mess-ups
        data = _self.merge({}, data)
        options = _self.merge({}, options)
        o=''
        
        o="<select"
        
        if ('multiple' in options) and options['multiple']:
            o+=" multiple"
        if ('disabled' in options) and options['disabled']:
            o+=" disabled='disabled'"
        if 'name' in options:
            o+=" name='"+str(options['name'])+"'"
        if 'id' in options:
            o+=" id='"+str(options['id'])+"'"
        if 'class' in options:
            o+=" class='"+str(options['class'])+"'"
        if 'style' in options:
            o+=" style='"+str(options['style'])+"'"
        if 'data' in options:
            for k,v in options['data'].items():
                o+=" data-"+str(k)+"='"+str(v)+"'"
            
        
        o+=">"
        
        if 'selected' in options:
            if not isinstance(options['selected'], list): options['selected']=[options['selected']]
        else:
            options['selected']=[]
            
        if 'optgroups' in options:
            if not isinstance(options['optgroups'], list): options['optgroups']=[options['optgroups']]
        
    
        for k,v in data.items():
        
            if ('optgroups' in options) and (k in  options['optgroups']):
            
                o+="<optgroup label='"+str(k)+"'>"
                
                v1 = v
                if isinstance(v, str) or isinstance(v, int) or not hasattr(v, '__iter__'):  v1 = [v]
                
                for k2,v2 in ODict(v1).items():
                
                    if 'use_key' in options:  v2=k2
                    elif 'use_value' in options:   k2=v2
                        
                    if k2 in options['selected']:
                        o+="<option value='"+str(k2)+"' selected='selected'>"+str(v2)+"</option>"
                    else:
                        o+="<option value='"+str(k2)+"'>"+str(v2)+"</option>"
                    
                
                o+="</optgroup>"
            
            else:
            
                if 'use_key' in options: v=k
                elif 'use_value' in options:  k=v
                    
                if k in options['selected']:
                    o+="<option value='"+str(k)+"' selected='selected'>"+str(v)+"</option>"
                else:
                    o+="<option value='"+str(k)+"'>"+str(v)+"</option>"
            
        
        o+="</select>"
        return o
    
   # static
    def getTemplateContents(id):
        global _G
        if id in _G.inlines: 
            return _G.inlines[id]
        
        elif (id in _G.templates) and os.path.exists(_G.templates[id]): 
            return Contemplate.read(_G.templates[id])
        
        return ''
    
    # static
    def merge(m, *args): 
        numargs = len(args)
        if numargs < 1: return m
        
        merged = m
        
        for arg in args:
            # http://www.php2python.com/wiki/function.array-merge/
            merged = ODict(merged)
            merged.update(arg)
        
        return merged
    
    # static
    def data(data):
        if isinstance(data, list):
            # clone the data
            return data[:]
        else:
            # clone the dict
            cdata = ODict()
            
            for key in data.keys():
                newkey = key
                cdata[newkey] = data[key]
            
            return cdata
        
    # static
    def open(file, op):
        #if Contemplate.ENCODING: 
        #    f = open(file, op, encoding=Contemplate.ENCODING)
        #else: 
        #    f = open(file, op)
        #return f
        return open(file, op, -1, Contemplate.ENCODING)

    # static
    def read(file):
        buffer=''
        with Contemplate.open(file, 'r') as f:
            buffer = f.read()
        return buffer

    # static
    def write(file, text):
        with Contemplate.open(file, 'w') as f:
            f.write(text)



# aliases
Contemplate.now = Contemplate.time
Contemplate.l = Contemplate.locale

# init the engine on load
Contemplate.init()

# if used with 'import *'
__all__ = ['Contemplate']
