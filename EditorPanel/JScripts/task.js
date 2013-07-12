/**
 * @author vladimir
 */

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
	    
	    var isTask = $currentTarget.is(".Task,.TaskDone") || $currentTarget.parents().is('.TaskGroup');
        if ( isTask && event.pageX < $currentTarget.position().left ){
            
            if ( !$currentTarget.hasClass('Task') 
              && !$currentTarget.hasClass('TaskDone') ){
                $currentTarget.addClass('Task');
            }
            $currentTarget.toggleClass("Task").toggleClass("TaskDone")
        }
	})

	//--------------------------------------------------------------------------
	function createTask(){
		execCommand("insertUnorderedList", false, "");
		$(getElement("ul")).addClass("TaskGroup")
		      .children("li").addClass('Task')
	}		
});
