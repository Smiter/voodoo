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