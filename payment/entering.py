from cryptomus import Client

PAYMENT_KEY = 'qd38AHmwZu9cIPVUDyfe3DZ2ezvWlkWuy5S2vv2jtoSJB8gC562ZFYfzeSphocBa8KTk3LB47cRTzzrNdb5CIRKbiTWSOy2AMettnI0YYPgI43aViJUnSbA0andEQsq8'
MERCHANT_UUID = 'e1c2e3c5-9e75-4438-a6f6-746a362d4bf6'

payment = Client.payment(PAYMENT_KEY, MERCHANT_UUID)




# Создание платежа
data_payment = {
    'amount': '10',
    'currency': 'USD',
    'network': 'tron',
    'order_id': '10',
    'url_return': 'https://example.com/return',
    'url_callback': 'https://example.com/callback',
    'is_payment_multiple': False,
    'lifetime': '7200',
    'to_currency': 'USDT'
};
# data_payment.update({"amount": '10'})

result = payment.create(data_payment)
result_url = result["url"]

# # Проверка платежа
# data = {
#     "uuid": "a7c0caec-a594-4aaa-b1c4-77d511857594",
#     "order_id": "1"
# }
# 
# result_p = payment.info(data)
# print(result_p["url"])