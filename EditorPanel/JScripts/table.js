$(document).ready(function(){
	$("body").bind("onCreateTable", createTable)
			 .bind("onInsertColBefore", function(){
			 	tableOperation("insert", "col", "before");
				return false;
			 })
			 .bind("onInsertColAfter", function(){
			 	tableOperation("insert", "col", "after");
				return false;
			 })
			 .bind("onInsertRowBefore", function(){
			 	tableOperation("insert", "row", "before")
				return false;
			 })
			 .bind("onInsertRowAfter", function(){
			 	tableOperation("insert", "row", "after")
				return false;
			 })
			 .bind("onDeleteRow", function(){
			 	tableOperation("delete", "row");
				return false;
			 })
			 .bind("onDeleteCol", function(){
			 	tableOperation("delete", "col");
				return false;
			 });
	
	function createTable(event, row, col){
		var $table = $("<table>");
		for (var i=0; i < row; i++) {
			var tr = $("<tr>").appendTo($table);
			for (var j=0; j < col; j++) {
			  var td = $("<td>").appendTo(tr);
			};
		};	
		insertNodeAtCaret($table.get(0))
		return $table;
	}

	function tableOperation (operation, what, where) {
		var table = getElement("table");
		if(!table || $(table).is(".TaskGroup")) return;
		if (operation == "insert"){
		    tableInsert(table, what, where);
		} else if (operation == "delete"){
			tableDelete(table, what)
		}
	}
	
	function tableInsert(table, what, where){
		if (what == "row") {
			insertRow(table, getTableRow(), where)
		} else if (what == "col"){
			insertCol(table, getTableCol(), where);
		};	
	}
	
	function tableDelete(table, what){
	    if (what == "row") {
	        deleteRow(table, getTableRow())
	    } else if (what == 'col'){
	        deleteCol(table, getTableCol())
	    }
	}
	
	function insertCol(table, pos, where){
		$(table).find("tr").each(function(){
			var $col = $(this).children("td").eq(pos);
			if (where == "before")
				$col.before($("<td>"));
			else if (where == "after")
				$col.after($("<td>"));		
		});
	}
	
	function insertRow(table, pos, where){
		var $row = $(table).find("tr").eq(pos);
		var $newRow = $row.clone().children("td").empty().end();
		
		if (where == "before")
			$($newRow).insertBefore($row);
		else if (where == "after")
			$($newRow).insertAfter($row);		  
	}
	
	function deleteCol(table, pos){
		$(table).find("tr").each(function(){
			$(this).children("td").eq(pos).remove();
			if ($(this).children("td").size() == 0) 
				$(this).remove();
		});
		clearTable(table);
	}
	
	function deleteRow(table, pos){
		$(table).find("tr").eq(pos).remove();
		clearTable(table);
	}
	
	function clearTable(table){
		if ($(table).find("tr").size() == 0) {
			$(table).remove();
		}	    
	}
});

$.fn.onArrow = function(key){
    function selectCell( previous ){
        var curcell = getElement("td");
        if (!curcell) return true;
        var $currow = $(curcell).parents('tr');
        var $row = previous ? $currow.prev('tr') : $currow.next('tr');
        var col = getTableCol();
        var td = $row.children('td').eq(col).get(0);
        selectElement(td)   
        return false;
    }
    if (!getElement("table")) return true;
        if( key == 'ARROWUP' ){
            return selectCell(true)
        } else if( key == 'ARROWDOWN' ){
            return selectCell(false)           
        } 
        return true;
}
