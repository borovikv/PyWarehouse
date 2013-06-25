function getCurrentSelection(){
	var selObj = window.getSelection(); 
	if (selObj.rangeCount > 0) {
		return selObj;
	} 
	return null;
}

function isElementNotCurrentTagName(elem, tagName){
    return elem && elem.tagName != tagName && elem.tagName != 'BODY' 
}

function countElem(elem, tagName, parentTagName){
	tagName = tagName.toUpperCase();
	parentTagName = parentTagName.toUpperCase();
	
	var i = 0;
    do {
		elem = elem.previousSibling;
		if(elem && elem.tagName === tagName) {
		    i++;
		}
    } while (isElementNotCurrentTagName(elem, parentTagName));
    return i;
}

function getElement(el, fromStart){
	fromStart = (fromStart == undefined || fromStart == null) ? true : false;
	var parent;
	parent = fromStart  ? getCurrentSelection().getRangeAt(0).startContainer 
				        : getCurrentSelection().getRangeAt(0).endContainer;
	
	while (isElementNotCurrentTagName(parent, el.toUpperCase())){
		parent = parent.parentNode;
	}
	if (parent.tagName != el.toUpperCase()) return null;
	
	return parent;
}

function getTableRow(){
    return countElem(getElement("tr"), "tr", "table");
}

function getTableCol(){
    return countElem(getElement("td"), "td", "tr");
}

function selectElement(element) {
	if (!element) return;
	var sel = getCurrentSelection()
	if (!sel) return;
	sel.removeAllRanges();
    var range = document.createRange();
    range.selectNodeContents(element);
    range.collapse(false);
    sel.addRange(range);
}

function insertNodeAtCaret(node) {
    var sel = getCurrentSelection();
    if (!sel) return;
    
    var range = sel.getRangeAt(0);
    range.collapse(false);
    range.insertNode(node);
    range = range.cloneRange();
    range.selectNodeContents(node);
    range.collapse(false);
    
    sel.removeAllRanges();
    sel.addRange(range);
}

function insertNodeAtCaret2(){
    var selection = getCurrentSelection();
    if (selection)
        selection.getRangeAt(0).insertNode($table.get(0))
}

function execCommand(command, arg1, arg2){
	document.execCommand(command, arg1, arg2);
}

function createElement(name, attrs){
	var e = document.createElement(name);
	for (var i in attrs) {
	  e.setAttribute(i, attrs[i]);
	};
	return e;
}

function getIcon(icon){
	return imgFolder + "/" +icon;
}

function getLocalIcon(icon){
	return "../_source/" + icon
}

var rgb2hex = function(rgb) {
    var rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    if (!rgb) return null;
    function hex(x) {
        return ("0" + parseInt(x).toString(16)).slice(-2);
    }
    return ("#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3])).toUpperCase();
}

