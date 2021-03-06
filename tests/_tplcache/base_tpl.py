# -*- coding: UTF-8 -*-
# Contemplate cached template 'base'

# imports start here, if any

# imports end here
def __getTplClass__(Contemplate):
    # extends the main Contemplate.Template class
    class Contemplate_base_Cached(Contemplate.Template):
        'Contemplate cached template base'

        # constructor
        def __init__(self, id=None):
            # initialize internal vars
            self._renderer = None
            self._extends = None
            self._blocks = None
            self.id = None
            self.id = id
            
            # extend tpl assign code starts here
            
            # extend tpl assign code ends here

        # tpl-defined blocks render code starts here
        
        
        # tpl block render method for block 'Block3'
        def _blockfn_Block3(self, data, __i__):
            
            __p__ = ''
             
            __p__ += 'Base template Block3'
            return __p__
            
        
        
        # tpl block render method for block 'Block2'
        def _blockfn_Block2(self, data, __i__):
            
            __p__ = ''
             
            __p__ += 'Base template Block2'
            return __p__
            
        
        
        # tpl block render method for block 'Block12'
        def _blockfn_Block12(self, data, __i__):
            
            __p__ = ''
             
            __p__ += 'Base template nested Block12'
            return __p__
            
        
        
        # tpl block render method for block 'Block11'
        def _blockfn_Block11(self, data, __i__):
            
            __p__ = ''
             
            __p__ += 'Base template nested Block11'
            return __p__
            
        
        
        # tpl block render method for block 'Block1'
        def _blockfn_Block1(self, data, __i__):
            
            __p__ = ''
             
            __p__ += '' + "\n" + 'Base template Block1' + "\n" + '<br /><br />' + "\n" + '' +  __i__.renderBlock('Block11', data) 
            __p__ += '' + "\n" + '<br /><br />' + "\n" + '' +  __i__.renderBlock('Block12', data) 
            __p__ += '' + "\n" + '<br /><br />' + "\n" + ''
            return __p__
            
        
        # tpl-defined blocks render code ends here

        # render a tpl block method
        def renderBlock(self, block, data, __i__=None):
            if not __i__: __i__ = self
            method = '_blockfn_' + block
            if (hasattr(self, method) and callable(getattr(self, method))):
                return getattr(self, method)(data, __i__)
            elif self._extends:
                return self._extends.renderBlock(block, data, __i__)
            return ''
            
        # tpl render method
        def render(self, data, __i__=None):
            if  not __i__: __i__ = self
            __p__ = ''
            if self._extends:
                __p__ = self._extends.render(data, __i__)

            else:
                # tpl main render code starts here
                
                __p__ += '<!-- this is the base template -->' + "\n" + '' + "\n" + '<strong>This is the base template</strong>' + "\n" + '' + "\n" + '' + "\n" + '<br /><br /><br /><br />' + "\n" + '<strong>This is Block1</strong><br />' + "\n" + '' +  __i__.renderBlock('Block1', data) 
                __p__ += '' + "\n" + '' + "\n" + '<br /><br /><br /><br />' + "\n" + '<strong>This is Block2</strong><br />' + "\n" + '' +  __i__.renderBlock('Block2', data) 
                __p__ += '' + "\n" + '' + "\n" + '<br /><br /><br /><br />' + "\n" + '<strong>This is Block3</strong><br />' + "\n" + '' +  __i__.renderBlock('Block3', data) 
                __p__ += '' + "\n" + '' + "\n" + '' + "\n" + '<br /><br /><br /><br />' + "\n" + '<strong>This is Block2 Again</strong><br />' + "\n" + '' +  __i__.renderBlock('Block2', data) 
                __p__ += '' + "\n" + ''
                
                # tpl main render code ends here

            return __p__
    
    return Contemplate_base_Cached

# allow to 'import *'  from this file as a module
__all__ = ['__getTplClass__']
