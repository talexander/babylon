
	<style type="text/css">

		body { -webkit-text-size-adjust:100%; }
		img { -ms-interpolation-mode:bicubic; }

		@media only screen and (max-width: 640px) {

		td[class~=rdb] { display:block !important; margin:0 !important; padding:0 !important; }
		span[class~=rdn] { display:none !important; }
		table[class~=rwf], td[class~=rwf], img[class~=rwf] { width:100% !important; }
		td[class~=rha], img[class~=rha] { height:auto !important; }
		table[class~=rwa], td[class~=rwa] { width:auto !important; }
		table[class~=rfn], td[class~=rfn] { font-size:15px !important; }
		table[class~=rfm], td[class~=rfm] { font-size:13px !important; }
		td[class~=sb_sub] { text-align:left !important; padding-left:27px; }
		td[class~=sb2] { margin-top:20px !important; margin-bottom:15px !important; }
		td[class~=soc2] { padding-top:10px !important; }
		}

	</style>
	<!--[if gte mso 9]>
	<style type="text/css">
	.btn1 { line-height:1em !important; padding:2px 0 3px 0 !important; }
	</style>
	<![endif]-->



<div bgcolor="#f3f3f3" style="font-family: Helvetica, Arial, sans-serif; font-size:13px; color:#333333; text-align:left; margin:0; padding:0; background: url('{{STATIC_URL}}/i/m/order/pat.jpg') repeat;">

<!-- html wrapper -->
<table class="wrh" width="100%" cellpadding="0" cellspacing="0" style="background: none; color:#000000; text-align:left;">


<!-- header -->
	<tr>
		<td class="lsd" height="38" bgcolor="#F26723" style="background-color:#F26723">&nbsp;&nbsp;</td>
		<td class="wrl" width="560" height="55" align="center" bgcolor="#F26723" style="background-color:#F26723">
			<h1>
				<a href="http://nitki-ulitki.ru/" target="_blank" style="font-size:18px; color:#ffffff; text-decoration:none;">
					<strong>
						<img src="{{STATIC_URL}}/i/m/order/logo_head.png" width="226" height="36" border="0" style="display:block;" alt="«Улиткина пряжа»" />
					</strong>
				</a>
			</h1>
		</td>
		<td class="lsd" height="38" bgcolor="#F26723" style="background-color:#F26723">&nbsp;&nbsp;</td>
	</tr>
<!-- /header -->

<!-- content -->
	<tr>
		<td class="lsd">&nbsp;&nbsp;</td>
		<td class="wrl" width="560" align="center">

    <!-- sep -->
    <table width="100%" cellpadding="0" cellspacing="0">
	    <tr><td><br /><br /><br /></td></tr>
    </table>
    <!-- sep -->

<!-- inner content -->
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#ffffff">
	<tr>
		<td align="center" style="padding:20px; box-shadow:0 0 3px 1px #d7d7d7;">

	<!-- intro -->
	<table width="100%" cellpadding="0" cellspacing="15">
		<tr>
			<td class="rdb rwf" align="left" valign="top">
				<table width="100%" cellpadding="0" cellspacing="0" style="font-family:Arial, Helvetica, sans-serif; font-size:14px; color:#000000;">
					<tr>
						<td align="left">
                            {% if not admin %}
							<h2>Ваш заказ принят!</h2>
							    <strong style="font-size: 28px; font-weight: normal;">Номер вашего заказа <span style="color:#F26723; font-size:1.5em; padding:0 5px;">{{ order.code }}</span></strong> <br /><br /><br />
                            {% else %}
                                <strong style="font-size: 28px; font-weight: normal;">Заказ <span style="color:#F26723; font-size:1.5em; padding:0 5px;">{{ order.code }}</span></strong> <br /><br /><br />
                            {% endif%}
						</td>
					</tr>
					<tr>
						<td align="left">
							<table width="100%" cellpadding="0" cellspacing="0" style="border-top: 1px dotted #dadada; border-bottom: 1px dotted #dadada; padding:20px 0; text-align: center;">
								<tr>
									<th style="text-align: left; width: 50%; padding-top: 10px;">Наименование</th>
									<th style="text-align: center; width: 10%; padding-top: 10px;">Количество</th>
									<th style="text-align: center; width: 20%; padding-top: 10px;">Цена</th>
									<th style="text-align: center; width: 20%; padding-top: 10px;">Сумма</th>
                                    {% if admin %}
                                        <th style="text-align: center; width: 20%;">Остаток</th>
                                    {% endif %}
								</tr>

                                {% for item in order.products %}
                                <tr>
									<td style="text-align: left; padding: 10px 10px 10px 0;">
                                        {{ item.product.name }}
                                        <span style="color:#777; font-size:0.95em;">{{ item.product.consist.name }} {{item.product.length2weight}}</span>
                                        {% if item.sku %}
                                            <span style="font-size:0.95em;">{{ item.sku.vendor_colour }} </span>
                                        {% endif %}
                                    </td>
									<td>{{ item.amount }} шт.</td>
									<td>{{ item.price|stringformat:"0.2f" }} руб.</td>
									<td>{{item.summ|stringformat:"0.2f" }} руб.</td>
                                    {% if admin %}
                                    <td>
                                        {% if item.sku %}
                                            {{ item.sku.left_amount|default:"--" }}
                                        {% else %}
                                            {{ item.left_amount|default:"--" }}
                                        {% endif %}
                                    </td>
                                    {% endif %}
								</tr>
                                {% endfor %}
								<tr>
									<td style="text-align: left; width: 50%; padding-bottom: 10px;"><strong>Итого</strong></td>
									<td></td>
									<td></td>
									<td style="text-align: center; width: 20%; padding-bottom: 10px;"><strong>{{ order.getTotalSum|stringformat:"0.2f" }} руб.</strong></td>
								</tr>
							</table><br /><br />

							<h3 style="font-size: 28px; margin: 0; font-weight: normal; color: #bbb;">Персональные данные:</h3>

							<table width="100%" cellpadding="0" cellspacing="0" style="border-bottom: 1px dotted #dadada; padding:20px 0; text-align: left;">
								<tr>
									<td width="20%" style="padding:0 10px 10px 0;">Имя</td>
									<td style="padding:0 10px 10px 0;"><strong>{{order.fname}}</strong></td>
								</tr>
								<tr>
									<td style="padding:0 10px 10px 0;">Телефон</td>
									<td style="padding:0 10px 10px 0;"><strong>{{order.phone}}</strong></td>
								</tr>
							</table><br /><br />

							<h3 style="font-size: 28px; margin: 0; font-weight: normal; color: #bbb;">Доставка:</h3>

							<table width="100%" cellpadding="0" cellspacing="0" style="border-bottom: 1px dotted #dadada; padding:20px 0; text-align: left;">
								<tr>
									<td width="30%" style="padding:0 10px 10px 0;">Способ доставки</td>
									<td style="padding:0 10px 10px 0;"><strong>{{order.deliveryMethod }}</strong></td>
								</tr>
							</table><br /><br />

							<h3 style="font-size: 28px; margin: 0; font-weight: normal; color: #bbb;">Оплата:</h3>

							<table width="100%" cellpadding="0" cellspacing="0" style="border-bottom: 1px dotted #dadada; padding:20px 0; text-align: left;">
								<tr>
									<td width="30%" style="padding:0 10px 10px 0;">Способ оплаты</td>
									<td style="padding:0 10px 10px 0;"><strong>{{order.paymentMethod }}</strong></td>
								</tr>
							</table><br /><br />

                            <table width="100%" cellpadding="0" cellspacing="0" style="border-bottom: 1px dotted #dadada; padding:20px 0; text-align: left;">
								<tr>
									<td width="30%" style="padding:0 10px 10px 0;">Комментарий</td>
									<td style="padding:0 10px 10px 0;">{{order.comment }}</td>
								</tr>
							</table><br /><br />



						</td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
	<!-- /intro -->


<!-- separator -->
<table class="sep" width="100%" cellpadding="0" cellspacing="0"><tr><td height="15">&nbsp;</td></tr></table>
<!-- /separator -->

		</td>
	</tr>
</table>
<!-- /inner content -->

</td>
		<td class="lsd">&nbsp;&nbsp;</td>
	</tr>
<!-- /content -->

<!-- footer -->
	<tr>
		<td class="lsd">&nbsp;&nbsp;</td>
		<td class="wrl" width="560" align="center" style="padding-top:5px; padding-bottom:5px;">
			<table class="rfm" cellpadding="0" cellspacing="10" style="font-family:Arial, Helvetica, sans-serif; font-size:12px; color:#000000;">
				<tr>
					<td align="center">
					<a target="_blank" href="http://nitki-ulitki.ru/" style="color:#000000;">Главная</a> &nbsp;|&nbsp;
					<a target="_blank" href="http://nitki-ulitki.ru/" style="color:#000000;">О нас</a> &nbsp;|&nbsp;
					<a target="_blank" href="http://nitki-ulitki.ru/" style="color:#000000;">Контакты</a><br /><br />
					свяжитесь с нами по электронной почте: <a target="_blank" href="#" style="color:#000000;">contact@nitki-ulitki.ru</a> <br /><br />
					{% now "Y" %} г. «Улиткина пряжа». Все права защищены.</td>
				</tr>
			</table>
		</td>
		<td class="lsd">&nbsp;&nbsp;</td>
	</tr>
<!-- /footer -->

</table>
<!-- /html wrapper -->

</div>

