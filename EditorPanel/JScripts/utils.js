function countElem(elem, tagName, parentTagName){
	tagName = tagName.toUpperCase();
	parentTagName = parentTagName.toUpperCase();
	
	var i = 0;
    do {
		elem = elem.previousSibling;
		if(elem && elem.tagName === tagName)
			i++;
    } while (elem && elem.tagName != parentTagName && elem.tagName !='BODY');
    return i;
}
function getCurrentSelection(){
	var selObj = window.getSelection(); 
	if (selObj.rangeCount > 0)
	{
		return selObj;
	} else 
		return null;

}
function getElement(el, start){
	start = (start == undefined || start == null) ? true : false;
	
	el = el.toUpperCase();
	var parent;
	
	parent = start ? getCurrentSelection().getRangeAt(0).startContainer 
				   : getCurrentSelection().getRangeAt(0).endContainer;
	while (parent && parent.tagName != el && parent.tagName != 'BODY'){
		parent = parent.parentNode;
	}
	if (parent.tagName != el) return null;
	return parent;
}

function test(elem){
	elem = elem.toUpperCase();
	var e = getElement(elem)
	return e != null && e.tagName == elem; 
}

function getTablePos(){
	var col = countElem(getElement("td"), "td", "tr");
	var row = countElem(getElement("tr"), "tr", "table");
	return {"row": row, "col": col};
}
function selectElement(element) {
	if (!element) return;
    if (window.getSelection) {
        var sel = window.getSelection();
        sel.removeAllRanges();
        var range = document.createRange();
        range.selectNodeContents(element);
        range.collapse(false);
        sel.addRange(range);
        
    } else if (document.selection) {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(element);
        textRange.select();
    }
}

function insertNodeAtCaret(node) {
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var range = sel.getRangeAt(0);
            range.collapse(false);
            range.insertNode(node);
            
            range = range.cloneRange();
            range.selectNodeContents(node);
            range.collapse(false);
            sel.removeAllRanges();
            sel.addRange(range);
        }
    } else if (typeof document.selection != "undefined" && document.selection.type != "Control") {
        var html = (node.nodeType == 1) ? node.outerHTML : node.data;
        var id = "marker_" + ("" + Math.random()).slice(2);
        html += '<span id="' + id + '"></span>';
        var textRange = document.selection.createRange();
        textRange.collapse(false);
        textRange.pasteHTML(html);
        var markerSpan = document.getElementById(id);
        textRange.moveToElementText(markerSpan);
        textRange.select();
        markerSpan.parentNode.removeChild(markerSpan);
    }
}
function createEvent(keys, event){
	var press = jQuery.Event(event);
	for (var p in keys){
		press[p] = keys[p]
	}
	return press;
}
function generateKeyPress(target, keys){
	$(target).trigger(createEvent(keys, "keypress"));
}
function generateKeyDown(target, keys){
	$(target).trigger(createEvent(keys, "keydown"))
}
function execCommand(command, arg1, arg2){
	//window.document.designMode = "On";
	document.execCommand(command, arg1, arg2);
	//window.document.designMode = "Off";
}
function print(text){
	var str = "";
	for(var i in text){
		str += text[i] + ", ";
	}
	//console.log(str);
	alert(str)
}
function createElement(name, attrs){
	var e = document.createElement(name);
	for (var i in attrs) {
	  e.setAttribute(i, attrs[i]);
	};
	return e;
}
function testShortcut(shortcut, _event_, needCtrl){
	needCtrl = needCtrl != undefined && needCtrl;
	if (!needCtrl && !_event_.ctrlKey && !_event_.altKey) return false;
	
	var key = shortcut.split(" + ")[1];
	return testKey(key, _event_);
}

function testKey(key,_event_){
		key = key.toUpperCase();
		switch(key){
		case "2":
			return _event_.which == 50;
			break;
		case "3":
			return _event_.which == 51;
			break;
		case "8":
			return _event_.which == 56;
			break;
		case "9":
			return _event_.which == 57;
			break;
		case "ARROWLEFT":
			return _event_.keyCode == 37;
			break;
		case "ARROWUP":
			return _event_.keyCode == 38;
			break;
		case "ARROWDOWN":
			return _event_.keyCode == 40;
			break;
		case "ARROWRIGHT":
			return _event_.keyCode == 39;
			break;
		case "DELETE":
			return _event_.keyCode == 45;
			break;
		case "INSERT":
			return _event_.keyCode == 46;
			break;
		case "B":
			return _event_.which == 98;
			break;
		case "I":
			return _event_.which == 105;
			break;
		case "U":
			return _event_.which == 117;
			break;
		case "Q":
			return _event_.which == 113 || _event_.which == 1081;
			break;
		case "T":
			return _event_.which == 116 || _event_.which == 1077;
			break;
		case "H":
			return _event_.which == 104;
			break;
		case "R":
			return _event_.which == 114;
			break;
		case "_":
			return _event_.which == 95;
			break;
		case "ENTER":
			return _event_.keyCode == 13;
		case "BACKSPACE":
			return _event_.keyCode == 8;
			break;
		case "SPACES":
			return _event_.which == 32;
			break;
	}
	return false;
}
function createShortcut(key, altKey, ctrlKey){
	var shortcut = {"altKey":altKey, "ctrlKey":ctrlKey}
	key = key.toUpperCase();
	switch(key){
		case "2":
			shortcut["which"] = 50;
		break;
		case "3":
			shortcut["which"] = 51;
		break;
		case "8":
			shortcut["which"] = 56;
		break;
		case "9":
			shortcut["which"] = 57;
		break;
		case "ARROWLEFT":
			shortcut["keyCode"] = 37;
		break;
		case "ARROWUP":
			shortcut["keyCode"] = 38;
		break;
		case "ARROWDOWN":
			shortcut["keyCode"] = 40;
		break;
		case "ARROWRIGHT":
			shortcut["keyCode"] = 39;
		break;
		case "DELETE":
			shortcut["keyCode"] = 45;
		break;
		case "INSERT":
			shortcut["keyCode"] = 46;
		break;
		case "B":
			shortcut["which"] = 98;
		break;
		case "I":
			shortcut["which"] = 105;
		break;
		case "U":
			shortcut["which"] = 117;
		break;
		case "Q":
			shortcut["which"] = 113;
		break;
		case "T":
			shortcut["which"] = 116;
		break;
		case "H":
			shortcut["which"] = 104;
		break;
		case "R":
			shortcut["which"] = 114;
		break;
		case "_":
			shortcut["which"] = 95;
		break;
	}
	return shortcut;
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