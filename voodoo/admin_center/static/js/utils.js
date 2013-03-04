function deleteAjax(item_id, model_name) {
    if (confirm("Вы уверены, что хотите удалить?")) {
        $.ajax({
            url: "delete/" + model_name + "/" + item_id +"/",
            type: "POST",
            success: function() {
                $('#row_id_' + item_id).remove();
            }
        });
	}
}

function deleteOrderItemAjax(item_id, row_id) {
	if (confirm("Удалить запчасть?")) {
		$.ajax({
		    url: "/admin_center/item_delete/"+ item_id +"/",
		    type: "POST",
		    success: function() {
		    	$('#row_id_' + row_id).remove();
		    }
		});
	}
}

function deleteOrderAjax(item_id) {
	if (confirm("Удалить заказ?")) {
		$.ajax({
		    url: "order_delete/"+ item_id +"/",
		    type: "POST",
		    success: function() {
		    	$('#row_id_' + item_id).remove();
		    }
		});
	}
}

function printOrder(row, orderId) {
	var printWindow = window.open();
	printWindow.document.write('Не нужно в меня тыкать, я ещё маленькая.');
	printWindow.window.print();

	printWindow.document.close();
}