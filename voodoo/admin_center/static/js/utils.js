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

function printOrder(orderId) {
	var printWindow = window.open('/admin_center/order_print/' + orderId + '/');
	
	// printWindow.window.print();
	return false;
}