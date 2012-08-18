$(document).ready(function(){
	window.document.designMode = "On";
})
$(document).ready(function(){
	function bold(){
		execCommand("bold", false, null);
	}
	function italic(){
		execCommand("italic", false, null);
	}
	function underline(){
		execCommand("underline", false, null);
	}
	function highlight(){
		var rgb2hex = function(rgb) {
		    var rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
		    if (!rgb) return null;
		    function hex(x) {
		        return ("0" + parseInt(x).toString(16)).slice(-2);
		    }
		    return ("#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3])).toUpperCase();
		}
		var testColor = function(){ 
			return rgb2hex($(this).css('background-color')) == color;
		}
		
		var color = '#FDFC8F' //"#FBEC5D"
		var $curent = $(getCurrentSelection().getRangeAt(0).startContainer)
		if ($curent.parents().filter(testColor).size()){
			execCommand("hiliteColor", false, "white");
		} else {
			execCommand("hiliteColor", false, color);
		}		
	}
	function oList(){
		execCommand("insertOrderedList", false, null);
	}
	function uList(){
		execCommand("insertUnorderedList", false, null);
	}
	function removeFormat(){
		execCommand("removeFormat", false, null);
	}
	function insertHR(){
		execCommand("insertHorizontalRule", false, null)
	}
	/////////////////////////////////////////////////////////////////////////////////
	// events
	/////////////////////////////////////////////////////////////////////////////////
	$("body").bind("onBold", bold)
			 .bind("onItalic",italic)
			 .bind("onUnderline",underline)
			 .bind("onHighlight",highlight)
			 .bind("onUList",uList)
			 .bind("onOList",oList)
			 .bind("onRemoveFormat",removeFormat)
			 .bind("insertHorizontalRule", insertHR);
	

});


