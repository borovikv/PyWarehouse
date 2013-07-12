$(document).ready(function(){
	window.document.designMode = "On";

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
		var color = '#FDFC8F' //"#FBEC5D"
		var $curent = $(getCurrentSelection().getRangeAt(0).startContainer)
		var isHighlighted = $curent.parents()
		    .filter(function(){ 
    		    var background_color = $(this).css('background-color')
                return rgb2hex(background_color) == color;
        }).size();
		execCommand("hiliteColor", false, isHighlighted ? "white": color );
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

	function replace(event, what, text, newtext) {
	    switch( what ){
	        case 'all':
        	   $("body *").replaceText(new RegExp(text, 'g'), newtext);
	           break;
	        case 'first':
        	   $("body *").replaceText(new RegExp(text), newtext, false, true);
    	       break;
	    }
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
			 .bind("insertHorizontalRule", insertHR)
			 .bind("replace", replace);
});


