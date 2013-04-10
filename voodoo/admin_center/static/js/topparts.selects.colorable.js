function makeElementColorable(el) {
	if ($(el).val() == 'Сообщен') {
		$(el).css({'color': 'black', 'font-weight':'bold' });
	}
	
	if ($(el).val() == 'Оформлен') {
		$(el).css({'color': 'orange', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 'Заказан') {
		$(el).css({'color': 'green', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 'Доставлен') {
		$(el).css({'color': 'blue', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 'Отказ') {
		$(el).css({'color': 'red', 'font-weight':'bold'});
	}
}

function makeOrderItemStatusesColorable(select) {
	select.each(function() {
		makeElementColorable(this);
	});
}

function makeOrderStatusSelectElementColorable(el) {
	if ($(el).val() == 1 || $(el).text() == 'Принят') {
		$(el).css({'color': 'black', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 2 ||$(el).text() == 'Обработан') {
		$(el).css({'color': 'green', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 3 ||$(el).text() == 'Закрыт') {
		$(el).css({'color': 'red', 'font-weight':'bold'});
	}
}

function makeOrderStatusSelectColorable(select) {
	select.each(function() {
		makeOrderStatusSelectElementColorable(this);	});
}

function makeCurrencySelectColorable(select) {
	select.each(function() {
		makeCurrencyElementColorable(this);
	});
}

function makeCurrencyElementColorable(el) {
	if ($(el).val() == 'UAH') {
		$(el).css({'color': 'orange', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 'USD') {
		$(el).css({'color': 'green', 'font-weight':'bold'});
	}
	
	if ($(el).val() == 'EUR') {
		$(el).css({'color': 'blue', 'font-weight':'bold'});
	}
}