function update(type, altKey, ctrlKey, shiftKey, which, keyCode){	
	keys = {
		"altKey":altKey, 
		"ctrlKey":ctrlKey,
		"which": which,
		"keyCode": keyCode
	}
	e = createEvent(keys,type)
	$("body").trigger(e)
}
$(document).ready(function(){
	$("body")//
		     .bind("onTask", function(){generateKeyDown("body", createShortcut("3", true, true))})
		     .bind("onTag", function(){generateKeyDown("body", createShortcut("2", true, true))})

	
	
	/*
	 * insert_element
	 * task_and_tags
	 */
});