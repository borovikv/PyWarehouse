/**
 * @author vladimir
 */
var taskCheckBox = '<div class="CheckBox Unchecked">'

function isCurElement(selector){
    var $curElem = $(getCurrentElement());
    return ($curElem.is(selector) || $curElem.parents().is(selector));
}

$(document).ready(function(){
	$(document).bind('onTask', function(){
		var $start = $(getCurrentElement());
		if ($start.parents().is(".TaskGroup")) return false;
		createTask();
	})

	$(document).bind('onDeleteTask', function(){
		$(getCurrentElement()).parents('.Task').remove();
	})
	
	$("body").click(function(event) {
	    var $currentTarget  = $(event.target);
        if ($currentTarget.is(".Task .CheckBox")){
	       toggleCheckTask($currentTarget);
        }
	})

	//--------------------------------------------------------------------------
	function createTask(){
		execCommand("insertUnorderedList", false, "");
		$(getElement("ul")).addClass("TaskGroup")
		      .children("li").addClass('Task')
		      .each(function(){
		          $(this).prepend($(taskCheckBox))
		      });
	}
		
	//--------------------------------------------------------------------------
	function toggleCheckTask(checkBox){
		if (isUnchecked(checkBox)){
            check(checkBox)			
		} else {
			uncheck(checkBox)
		}
	}
	function isUnchecked(checkBox){
	    return checkBox.hasClass('Unchecked');
	}
	
	function check(checkBox){
	    checkBox.removeClass('Unchecked').addClass('Checked').parents('.Task')
	                  .addClass("TaskDone")                 
	}
	
	function uncheck(checkBox){
	    checkBox.removeClass('Checked').addClass('Unchecked').parents('.Task')
					  .removeClass("TaskDone")
	}	
	
});

$.fn.onEnter = function(){
    if (isCurElement('.Task')){
        var $task = $('<li class="Task">')
            .append($(taskCheckBox))
            .append($('<br>'));
	    
	    getCurrentTask().after($task)
	    return false;
    }    
	function getCurrentTask(){
	    var $curElem = $(getCurrentElement());
        if ($curElem.is(".Task")){
            return $curElem;
        } else {
            return $curElem.parents('.Task')
        }  
	}
}
$.fn.onKeyPressed = function(key){
    if (isCurElement('.Task .CheckBox')){
        return false;
    }
    return true;
}