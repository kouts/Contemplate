<?php 
/* Contemplate cached template 'demo' */ 
if (!class_exists('Contemplate_demo_Cached')) { final class Contemplate_demo_Cached extends Contemplate { public function __construct($id=null, $_r=null) { $this->id=null; $this->data=null; $this->_renderFunction=null; $this->_parent=null;  $this->_blocks=null; $this->id=$id; $this->setParent(Contemplate::tpl('base')); } private function _blockfn_Block3($__instance__) { $__p__ = ''; extract($__instance__->data);    $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '    <strong>Block3 is overriden by the demo template</strong>' . PHP_EOL . '' . PHP_EOL . '    <br /><br />' . PHP_EOL . '    ' . PHP_EOL . '    '; if (!empty($users)) { foreach ($users as $i=>$usergroup) { $__instance->data['i']=$i; $__instance->data['usergroup']=$usergroup;   $__p__ .= '' . PHP_EOL . '        <!-- call a (sub-)template -->' . PHP_EOL . '        ' . Contemplate::tpl("sub",  array("i"=>$i, "usergroup"=>$usergroup));   $__p__ .= '' . PHP_EOL . '    '; } }   $__p__ .= '' . PHP_EOL . '' . PHP_EOL . ' '; return $__p__;} private function _blockfn_Block2($__instance__) { $__p__ = ''; extract($__instance__->data);    $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '    <strong>Block2 is overriden by the demo template</strong>' . PHP_EOL . '' . PHP_EOL . '    <br /><br />' . PHP_EOL . '' . PHP_EOL . '    <strong>A table</strong><br />' . PHP_EOL . '    ' . Contemplate::htmltable($table_data, $table_options);   $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '    <br /><br />' . PHP_EOL . '    ' . PHP_EOL . '    <strong>A select box</strong><br />' . PHP_EOL . '    ' . Contemplate::htmlselect($select_data, $select_options);   $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '    <br /><br />' . PHP_EOL . '    ' . PHP_EOL . '    <strong>A table with alternative format</strong><br />' . PHP_EOL . '    ' . Contemplate::htmltable($table_data, array("header"=>true));   $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '    <br /><br />' . PHP_EOL . '    ' . PHP_EOL . '    <strong>A select box with alternative format</strong><br />' . PHP_EOL . '    ' . Contemplate::htmlselect($select_data, array(            "optgroups"=>array("group1", "group2", "group3"),            "selected"=>3,            "multiple"=>false,            "style"=>"width:200px;"        ));   $__p__ .= '' . PHP_EOL . '    ' . PHP_EOL . '    <br /><br />' . PHP_EOL . '    <!-- include a (sub-)template file -->' . PHP_EOL . '     <!-- print a localized date php-style -->' . PHP_EOL . '<strong>A (localized) date, PHP-style</strong><br />' . PHP_EOL . '' . ( Contemplate::ldate("M, d", Contemplate::now()) ) . '' . PHP_EOL . '';   $__p__ .= '' . PHP_EOL . '' . PHP_EOL . ' '; return $__p__;}public function renderBlock($block, $__instance__=null) { if(!$__instance__) $__instance__=$this; if (method_exists($this, '_blockfn_'.$block)) { return call_user_func(array($this, '_blockfn_'.$block), $__instance__); } elseif ($this->_parent) { return $this->_parent->renderBlock($block, $__instance__); } return ''; } public function render($__data__, $__instance__=null) { $__p__ = ''; if(!$__instance__) $__instance__=$this; if ($this->_parent) {$__p__=$this->_parent->render($__data__, $__instance__);} else { $__instance__->data=Contemplate::o2a((array)$__data__); extract($__instance__->data); $__p__ .= '<!-- extends/inherits the base template -->' . PHP_EOL . '';   $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '' . PHP_EOL . '' .   $__instance__->renderBlock('Block2');    $__p__ .= '' . PHP_EOL . '' . PHP_EOL . '' .   $__instance__->renderBlock('Block3');    $__p__ .= '' . PHP_EOL . '';} $this->data=null; return $__p__;} } }