import datetime

from flask import Flask, request

import gidrachDB
import tezariusDB

app = Flask('amo_crm')

orders = tezariusDB.Sales()


# {'account[subdomain]': '700622', 'account[id]': '29604535',
# 'account[_links][self]': 'https://700622.amocrm.ru', 'leads[add][0][id]': '35168771',
# 'leads[add][0][name]': 'Заказ #87856, +7 (919) 959-39-84', 'leads[add][0][status_id]': '50288839',
# 'leads[add][0][price]': '0', 'leads[add][0][responsible_user_id]': '9750914',
# 'leads[add][0][last_modified]': '1712331728', 'leads[add][0][modified_user_id]': '0',
# 'leads[add][0][created_user_id]': '0', 'leads[add][0][date_create]': '1712331728',
# 'leads[add][0][pipeline_id]': '5723341', 'leads[add][0][tags][0][id]': '276241',
# 'leads[add][0][tags][0][name]': 'xn--80afdp5b4b.xn--p1ai', 'leads[add][0][tags][1][id]': '276243',
# 'leads[add][0][tags][1][name]': 'myshop.ru', 'leads[add][0][account_id]': '29604535',
# 'leads[add][0][custom_fields][0][id]': '6099', 'leads[add][0][custom_fields][0][name]': '_ym_uid',
# 'leads[add][0][custom_fields][0][values][0][value]': '87856', 'leads[add][0][custom_fields][0][code]': '_YM_UID',
# 'leads[add][0][custom_fields][1][id]': '1425011', 'leads[add][0][custom_fields][1][name]': 'Город доставки',
# 'leads[add][0][custom_fields][1][values][0][value]': 'Тюменская область',
# 'leads[add][0][custom_fields][2][id]': '1402697',
# 'leads[add][0][custom_fields][2][name]': 'С какого сайта пришла заявка',
# 'leads[add][0][custom_fields][2][values][0][value]': 'xn--80afdp5b4b.xn--p1ai',
# 'leads[add][0][custom_fields][2][values][0][enum]': '918167', 'leads[add][0][custom_fields][3][id]': '1426025',
# 'leads[add][0][custom_fields][3][name]': 'Наша  цена', 'leads[add][0][custom_fields][3][values][0][value]': '280.00',
# 'leads[add][0][created_at]': '1712331728', 'leads[add][0][updated_at]': '1712331728'}
@app.route('/add_lead', methods=['GET', 'POST'])
def add_lead():
    lead_json = request.form.to_dict()
    custom_field_dict = {}
    for key, value in lead_json.items():
        if 'custom_fields' in key and 'name' in key:
            custom_field_index = key.split('[custom_fields][')[1].split('][')[0]
            custom_field_dict[value] = lead_json.get(f'leads[add][0][custom_fields][{custom_field_index}]'
                                                     f'[values][0][value]')
    order_id = custom_field_dict.get('_ym_uid')
    order = gidrachDB.get_order(int(order_id))
    customer_name = order.firstname + ('' if type(order.lastname) is None else ' ' + order.lastname)
    customer_phone = order.telephone
    customer_email = order.email
    customer_source = custom_field_dict.get('С какого сайта пришла заявка')
    note = order.comment
    date = datetime.datetime.strftime(order.date_added, '%Y-%m-%d %H:%M:%S')
    positions = []
    try:
        for pos in order.order_product:
            product_name = pos.name
            code = pos.product.sku
            brand = orders.get_product(pos.product.sku)['brand']
            cost = pos.price
            qty = pos.quantity

            positions.append({'name': product_name, 'code': code, 'brand': brand, 'cost': int(cost), 'qty': int(qty),
                              'date': date, 'note': note})
        result = orders.create_order(order_id, date, customer_name, customer_phone, customer_email, customer_source,
                                     note,
                                     positions)
        if result:
            orders_list = orders.get_order(result[0]['DocNumber'])
            items = []
            for item in orders_list:
                items.append(item['id'])
            order.tezarius_id = ','.join(items)
            gidrachDB.session.add(order)
            gidrachDB.session.commit()
    except Exception as e:
        print(e)

    return 'ok'


if __name__ == '__main__':
    app.run(port=5000, debug=False)
