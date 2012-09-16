/**
 * @author vladimir
 */
$(document).ready(function(){
	/////////////////////////////////////////////////////////////////////////////////
	// Events
	/////////////////////////////////////////////////////////////////////////////////
	$(document).bind('onDeleteTask', function(){
		var $start = getJQStartElement();
		if (!$start) return;
		if ($start.parents().is('.Task')){
			$start.parents('.Task').remove();
		}
	})
	$(document).bind('onTask', function(){
		currentSelection = getCurrentSelection();
		if(currentSelection == null) return null;
		var $start = getJQStartElement(currentSelection);
		if (!$start) return;
		if ($start.parents().is(".TaskGroup")) return false;
		
		addElement(currentSelection, createTask, wrapTask, "taskGroup", "text");
	})
	$(document).bind('onTag', function(){
		currentSelection = getCurrentSelection();
		if(currentSelection == null) return null;
		// var $start = getJQStartElement(currentSelection);
		// if (!$start) return;
		// if ($start.parents().is(".TaskGroup")) return false;
		
		addElement(currentSelection, createTag, wrapTag, "tag", "text");
	})
	
	$("body").keydown(function(event){
		var $start = getJQStartElement();
		if (!$start) return;
		
		//---------------------------------------------------------------------------
		if ($start.is(".CheckBox") && !testKey("arrowLeft", event) && !testKey("arrowRight", event)){	
			return false;
		} 
		if (($start.is(".TaskText") || $start.parents().is(".TaskText")) && testKey("enter", event) && !event.shiftKey){
			insertTaskAfter($start);
			event.preventDefault();
		} 
		
		if ($start.parents().is(".Tag") && (testKey("enter", event) || testKey("spaces", event))){
			var spaces = document.createTextNode(" ");
			$start.parents(".Tag").after($(spaces));
			selectElement(spaces);
			return false;
		}
	});
	
	$("body").click(function(event){
		var $currentTarget  = $(event.target);
		
		
		if ($currentTarget.is("img.Chek_Task")){
			if ($currentTarget.attr("src") == getLocalIcon("unchecked.png")){
				$table = $currentTarget.attr("src", getLocalIcon("checked.png"))
							  .parents("tr").addClass("TaskDone")
							  .parents("table");
				if (!$table.children('tbody.ToDo').size()){
					!$table.children('tbody').addClass("ToDo");
				}
				if (!$table.children('tbody.Done').size()){
					!$table.append('<tbody class="Done">');
				}
				
				$table.children('tbody.Done').prepend($table.find('tbody.ToDo > tr.TaskDone'));
				
				
			} else {
				$currentTarget.attr("src", getLocalIcon("unchecked.png"))
							  .parents("tr")
							  .removeClass("TaskDone").addClass("Do")
							  .appendTo($('tbody.ToDo'));
				
			}
		} 
	});
	/////////////////////////////////////////////////////////////////////////////////
	// Functions for create task and tag
	/////////////////////////////////////////////////////////////////////////////////
	function createTask(){
		var task = {"task": createElement("tr", {"class":"Task"}),
					"checkBox": createElement("td", {"class": "CheckBox"}),
					"check": createElement("img", {"src": getLocalIcon("unchecked.png"), "class": "Chek_Task"}),
					"text": createElement("td", {"class":"TaskText"}),
					//"time": createElement("input", {"type":"date","class":"TaskTime"}),
					"priority": createElement("td", {"class":"TaskPriority"})
				};
		
		task["task"].appendChild(task["checkBox"])
		task["task"].appendChild(task["text"])
		task["task"].appendChild(task["priority"])
		task["checkBox"].appendChild(task["check"])
		task["taskGroup"] = $("<table>").addClass("TaskGroup")
										  .html(task["task"])
										  .get(0);
		
		return task;
	}
	
	function createTag(){
		var tag = {"tag": createElement("span", {"class":"Tag"}),
				   "text": createElement("span", {"class":"TagText"})
					};
		tag.text.innerHTML = "@"
		for(var i in tag){
			if(i == "tag") continue;
			tag["tag"].appendChild(tag[i]);
		}
		return tag;
	}
	
	/////////////////////////////////////////////////////////////////////////////////
	// 
	/////////////////////////////////////////////////////////////////////////////////
	function addElement(selection,  creator, wrapper, elem, selectAfter){ 
		if (selection == ""){
			var e = creator();
			insertNodeAtCaret(e[elem]);
			selectElement(e[selectAfter]);
		} else {
			wrapper(selection);
		}
	}
	
	function wrapTask(selection){
		execCommand("insertUnorderedList", false, "");
		var ul = getElement("ul");
		var taskGroup = createTask();
		$(taskGroup["taskGroup"]).empty();
		
		var $uls = $(ul)
		$uls.addClass("TaskGroup").children("li").each(function(index){
			var task = createTask();
			$(task["text"]).append($(this).contents());
			$(taskGroup["taskGroup"]).append($(task["task"]));				
		});
		$uls.after($(taskGroup["taskGroup"])).remove();
	}
	
	function wrapTag(selection){
		var range = selection.getRangeAt(0);
		var span = createElement("span", {});
		var currentSelection = "" + selection;
		if (!currentSelection.trim()) return;
		
		currentSelection = currentSelection.split(/[\s,\.;]/);
	
		for (var i in currentSelection){
			var text = currentSelection[i].trim();
			if (!text) continue;
			
			tag = createTag();
			tag["text"].appendChild(document.createTextNode(text));
			span.appendChild(tag["tag"]);
			span.appendChild(document.createTextNode(" "));
		}
		range.extractContents();
		range.insertNode(span)
		$span = $(span);
		$span.contents().insertAfter($span);
		$span.remove();
	}
	
	function insertTaskAfter($currentElement){
		task = createTask();
		$currentElement.parents(".Task").after($(task["task"]));
		selectElement(task["text"])
	}
	function getJQStartElement(currentSelection){
		if(!currentSelection){
			currentSelection = getCurrentSelection();
			if(currentSelection == null) return null;
		}
		var $start = $(currentSelection.getRangeAt(0).startContainer);
		return $start;
	}
	
});
