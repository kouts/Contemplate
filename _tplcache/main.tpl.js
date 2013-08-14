(function(root) { 
/* Contemplate cached template 'main' */ 
function Contemplate_main_Cached($id) { this.id=$id; this.data=null; var $parent=null, $blocks=null; this.setId=function($id) { if ($id) {this.id=$id;} return this; }; this.setParent=function(parent) { $parent=parent; return this; }; this.renderBlock=function(block) { $blocks={ };  if ($blocks[block]) return $blocks[block].call(this); else if ($parent) return $parent.renderBlock.call(this, block); return ''; }; this.render=function(data) { var $__p__ = ''; if ($parent) {$__p__ = $parent.render.call(this, data);} else {this.data = Contemplate.clonePHP(data); with(this.data) { $__p__ += '<!DOCTYPE html>' + "\n" + '<html>' + "\n" + '' + "\n" + '' + "\n" + '    <!-- PROOf Of CONCEPT' + "\n" + '    /*' + "\n" + '    *  Simple light-weight javascript templating engine (part of php templating engine)' + "\n" + '    *  @author: Nikos M.  http://nikos-web-development.netai.net/' + "\n" + '    *' + "\n" + '    *  @inspired by : Simple JavaScript Templating, John Resig - http://ejohn.org/ - MIT Licensed' + "\n" + '    *  http://ejohn.org/blog/javascript-micro-templating/' + "\n" + '    *' + "\n" + '    */' + "\n" + '    -->' + "\n" + '    ' + "\n" + '    <head>' + "\n" + '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' + "\n" + '        <script src="./src/Contemplate.js"></script>' + "\n" + '        <script type="text/html" id="sub_tpl">' + "\n" + '         ' + ( $templates["sub"] ) + '' + "\n" + '        </script>' + "\n" + '    </head>' + "\n" + '' + "\n" + '    <body>' + "\n" + '        ' + "\n" + '        PHP:' + "\n" + '        <div id="results_php">' + ( $render_php ) + '</div>' + "\n" + '        ' + "\n" + '        <hr />' + "\n" + '        ' + "\n" + '        JS:' + "\n" + '        <div id="results_js"></div>' + "\n" + '        <script>' + "\n" + '            /* set the template separators */' + "\n" + '            Contemplate.setTemplateSeparators("' + ( $sepleft ) + '", "' + ( $sepright ) + '");' + "\n" + '            /* add the templates (from the inline script tags) */' + "\n" + '            Contemplate.add({' + "\n" + '                "demo" : "./_tpls/demo.tpl.html", // load the template from this url' + "\n" + '                "sub" : "sub_tpl" // load the template from inside this DOM element' + "\n" + '            });' + "\n" + '            ' + "\n" + '            /* localize some strings */' + "\n" + '            Contemplate.setLocaleStrings({' + "\n" + '                "Jul" : "Ιουλ",' + "\n" + '                "Sep" : "Σεπτ"' + "\n" + '            });' + "\n" + '            var results = document.getElementById("results_js");' + "\n" + '            results.innerHTML = Contemplate.tpl(\'demo\', ' + ( $data_js ) + ');' + "\n" + '        </script>' + "\n" + '    ' + "\n" + '    </body>' + "\n" + '' + "\n" + '</html>'; }} this.data=null; return $__p__; }; }; if ('undefined' != typeof (module) && module.exports) {module.exports=Contemplate_main_Cached;} else if (typeof (exports) != 'undefined') {exports=Contemplate_main_Cached;}  else {root.Contemplate_main_Cached=Contemplate_main_Cached;} })(this);