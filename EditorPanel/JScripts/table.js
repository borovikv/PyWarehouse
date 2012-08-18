$(document).ready(function(){
	var $curentTable;
	var imgArrowRight = getIcon("Arrow right.png");
	var imgArrowLeft = getIcon("Arrow left.png");
	var imgArrowUp = getIcon("Arrow up.png");
	var imgArrowDown = getIcon("Arrow down.png");
	var imgDelete = getIcon("Delete.png");

	var addColBefore = createItem(imgArrowLeft, insertCol, "before", "col");
	var addColAfter  = createItem(imgArrowRight, insertCol, "after", "col");
	var addRowBefore = createItem(imgArrowUp, insertRow, "before", "row");
	var addRowAfter  = createItem(imgArrowDown, insertRow, "after", "row");
	var removeCol = createItem(imgDelete, del, "col", "col");
	var removeRow = createItem(imgDelete, del, "row", "row");
	
	var hColBar = createBar("hColBar", [addColBefore, removeCol, addColAfter])
	var vRowBar = createBar("vRowBar", [addRowBefore, removeRow, addRowAfter])	
	
	///////////////////////////////////////////////////////////////////////////////////
	// events
	///////////////////////////////////////////////////////////////////////////////////
	$("body").click(function(event){
		var $currentTarget  = $(event.target);
		if($currentTarget.is("td") && !$currentTarget.parent().is(".Task")){
			$curentTable = $currentTarget.parents("table");
			showBar($currentTarget);
		} else if (!$currentTarget.parents("div").is("#hColBar,#vRowBar")){
			hColBar.hide();
			vRowBar.hide();
		}	
	})	
	$("body").bind("onCreateTable", function(){
				createTable(ROW_COL);
			})
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
	
	$("body").keydown(function(event){
		if (!test("table")) return;
		if(testKey("arrowUp", event)){
		// arrow up
			var elem = getElement("td").parentNode.previousSibling;
			if (elem)
				selectElement(elem.childNodes[getTablePos()["col"]])	
			return false;		
		} else if(testKey("arrowDown", event)){
		// arraw down
			var elem = getElement("td").parentNode.nextSibling;
			if (elem)
				selectElement(elem.childNodes[getTablePos()["col"]])	
			return false;
		}
	});
	
	
	///////////////////////////////////////////////////////////////////////////////
	// interface creation
	///////////////////////////////////////////////////////////////////////////////
	function createItem(imgSrc, func, arg, what){
		return $("<img>")
				.attr("src", imgSrc)
				.addClass("Item")
				.click(function(){
					
					var index = $(document).data(what);
					func(index, arg);
				})
	}
	
	function createBar(id, items){
		var bar = $("<div id='" + id +"'>").attr("__service", true);
		for(var i in items){
			bar.append(items[i]);
		}
		bar.prependTo('body');
		
		return bar;
	}
	
	function showBar(currentTD){
		var parentRow = currentTD.parent("tr");
		var position = currentTD.position()
		var index = {"col":-1, "row": -1};
		
		if(parentRow.is(":first-child") || parentRow.is(":last-child")){
			var top = 0;
			if(currentTD.parent("tr").is(":first-child"))
				top = position.top - hColBar.height();
			else
				top = position.top + currentTD.height()
			var left = position.left + currentTD.width() / 2 - hColBar.width() / 2;
			hColBar.css({"top":top, "left":left}).show();
			
			index["col"] = parentRow.children().index(currentTD);
		}
		if(currentTD.is(":first-child") || currentTD.is(":last-child")){
			var top = position.top + currentTD.height() / 2 - vRowBar.height() / 2;
			var left = 0;
			if (currentTD.is(":first-child"))
				left = position.left - vRowBar.width() ;
			else
				left = position.left + currentTD.width() ;
			vRowBar.css({"top":top, "left":left}).show();
			
			index["row"] = parentRow.parent().children().index(parentRow);
		}
		$(document).data("row", index["row"]);
		$(document).data("col", index["col"]);
	}

	////////////////////////////////////////////////////////////////////////////////////////
	// Table Section
	///////////////////////////////////////////////////////////////////////////////////////
	function getRowAndCol(str){
		var table = Object()
		if (!str){
			table.row = 1
			table.col = 1
		} else {
			row_col = str.split(/[\D]/);
			table.row = parseInt(row_col[0]);
			table.col = parseInt(row_col[1]);
		}
		return table;
	}
	function createTable(str_row_col){
		var row_col = getRowAndCol(str_row_col);
		var row = row_col["row"];
		var col = row_col["col"];
		
		var $table = $("<table>");
		for (var i=0; i < row; i++) {
			var tr = $("<tr>").appendTo($table);
			for (var j=0; j < col; j++) {
			  var td = $("<td>").appendTo(tr);
			};
		};	
		var selection = getCurrentSelection();
		if (selection)
			selection.getRangeAt(0).insertNode($table.get(0))
		return $table;
	}
	
	function insertCol(pos, where){
		$($curentTable).find("tr").each(function(){
			var $col = $(this).children("td").eq(pos);
			if (where == "before")
				$($col).before($("<td>"));
			else if (where == "after")
				$($col).after($("<td>"));		
		});
	}
	
	function insertRow(pos, where){
		var $row = $($curentTable).find("tr").eq(pos);
		var $newRow = $($row).clone().children("td").empty().end();
		
		if (where == "before")
			$($newRow).insertBefore($row);
		else if (where == "after")
			$($newRow).insertAfter($row);		  
	}
	
	function del(pos, what){
		//alert($($curentTable).find("tr").contents().filter("td:nth-child(" + pos +")").size())
		
		if(what == "col"){
			//$($curentTable).find("tr").contents().filter("td:nth-child(" + pos +")").remove()
			$($curentTable).find("tr").each(function(){
				
				$(this).children("td").eq(pos).remove();
				if ($(this).children("td").size() == 0) 
					$(this).remove();
			});
		} else if (what = "row")
			$($curentTable).find("tr").eq(pos).remove();
		
		if ($($curentTable).find("tr").size() == 0) {
			$($curentTable).remove();
		}
	}
	
	function tableOperation (operation, what, where) {
		
		if(!test("table") || $(getElement("table")).is(".TaskGroup")) return;
		
		$curentTable = $(getElement("table"));
		var pos = getTablePos()
		if (operation == "insert"){
			if (what == "row") {
				insertRow(pos[what], where)
			} else if (what == "col"){
				insertCol(pos[what], where);
			};	
		} else if (operation == "delete"){
			del(pos[what], what);
		}
	}
	
});


