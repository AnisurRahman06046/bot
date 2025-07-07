# import requests

# PHONE_NUMBER_ID = "681336028399916"
# ACCESS_TOKEN = "EAARYZCL8oasQBPHsiBk36jqZCIDfwxXXVpO5clwTWUZCHfRbRz7eDiZB9ZBXTP50u09NgYg8qUMzGvr4b7ZCkPnr4XzRRiAmXZAPwkZBqEy1GVXOlreF0oKbcZBdMbZBTerJ3kydZC9ZAMivJcf9FYgmjglbIXqvuPNMYCb6tCNL6N6ZCX0VzOaqqSx9ZCMkP084NnT9eXSKDZCj6ZClFH8ZBZAHJYHU1ZBHrUzg6SWMF6UssbxPH248GGOXgZDZD"


# def send_whatsapp_message(recipient_number: str, message_text: str):
#     url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,
#         "type": "text",
#         "text": {"body": message_text},
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print("Send Response:", response.status_code)
#     print(response.json())
#     return response


# def send_whatsapp_buttons(recipient_number: str):
#     url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,
#         "type": "interactive",
#         "interactive": {
#             "type": "button",
#             "body": {"text": "👋 Welcome to WhatsApp Shop!\nPlease choose an option:"},
#             "action": {
#                 "buttons": [
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "browse_products",
#                             "title": "🛍 Browse Products",
#                         },
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {"id": "view_cart", "title": "🛒 View Cart"},
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {"id": "place_order", "title": "📦 Place Order"},
#                     },
#                 ]
#             },
#         },
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print("Send Response:", response.status_code)
#     print(response.json())
#     return response


# def send_product_list(recipient_number: str):
#     url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json",
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,
#         "type": "interactive",
#         "interactive": {
#             "type": "list",
#             "header": {"type": "text", "text": "🛍 Product Catalog"},
#             "body": {"text": "Please select a product to view details:"},
#             "footer": {"text": "Tap a product below"},
#             "action": {
#                 "button": "View Products",
#                 "sections": [
#                     {
#                         "title": "Available Products",
#                         "rows": [
#                             {
#                                 "id": "airpods_pro",
#                                 "title": "🎧 AirPods Pro",
#                                 "description": "$249 - Noise Cancelling",
#                             },
#                             {
#                                 "id": "samsung_watch",
#                                 "title": "⌚ Samsung Galaxy Watch",
#                                 "description": "$199 - AMOLED Display",
#                             },
#                             {
#                                 "id": "jbl_headphones",
#                                 "title": "🎶 JBL Tune 760NC",
#                                 "description": "$129 - Bluetooth 5.0",
#                             },
#                             {
#                                 "id": "bose_qc45",
#                                 "title": "🎧 Bose QC 45",
#                                 "description": "$299 - Premium Audio",
#                             },
#                         ],
#                     }
#                 ],
#             },
#         },
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print("Send Response:", response.status_code)
#     print(response.json())
#     return response


import requests


def send_dynamic_whatsapp_message(recipient_number: str, message_text: str, shop):
    url = f"https://graph.facebook.com/v19.0/{shop.phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {shop.access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {"body": message_text},
    }
    return requests.post(url, json=payload, headers=headers)


def send_dynamic_buttons(recipient_number: str, shop):
    url = f"https://graph.facebook.com/v19.0/{shop.phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {shop.access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "👋 Welcome to WhatsApp Shop!\nPlease choose an option:"},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "browse_products",
                            "title": "🛍 Browse Products",
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {"id": "view_cart", "title": "🛒 View Cart"},
                    },
                    {
                        "type": "reply",
                        "reply": {"id": "place_order", "title": "📦 Place Order"},
                    },
                ]
            },
        },
    }
    return requests.post(url, json=payload, headers=headers)


def send_dynamic_product_list(recipient_number: str, shop):
    url = f"https://graph.facebook.com/v19.0/{shop.phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {shop.access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "🛍 Product Catalog"},
            "body": {"text": "Please select a product to view details:"},
            "footer": {"text": "Tap a product below"},
            "action": {
                "button": "View Products",
                "sections": [
                    {
                        "title": "Available Products",
                        "rows": [
                            {
                                "id": "airpods_pro",
                                "title": "🎧 AirPods Pro",
                                "description": "$249 - Noise Cancelling",
                            },
                            {
                                "id": "samsung_watch",
                                "title": "⌚ Samsung Galaxy Watch",
                                "description": "$199 - AMOLED Display",
                            },
                            {
                                "id": "jbl_headphones",
                                "title": "🎶 JBL Tune 760NC",
                                "description": "$129 - Bluetooth 5.0",
                            },
                            {
                                "id": "bose_qc45",
                                "title": "🎧 Bose QC 45",
                                "description": "$299 - Premium Audio",
                            },
                        ],
                    }
                ],
            },
        },
    }
    return requests.post(url, json=payload, headers=headers)
