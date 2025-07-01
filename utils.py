import requests

PHONE_NUMBER_ID = "681336028399916"
ACCESS_TOKEN = "EAARYZCL8oasQBO2nZBvXlebzv1CiwOAvWo6LRAGsAfJhZCqsQ5MlGBkGXNyMXUqy3pCOBkXnwPWamhZC8DkyS6dq01lZAAgtq2JRiZCCkk4Sa2u8mkqcs5Tvd5dMCxTRJIrrRDdDCXqXZA9t9r7cZB4hyWpKmn2yAboeZCy1vZClAnFlbfpYQFw5CfnrPyOa2Q7GShLxpjIxeadwNY77ahLqJpAiCHcl1V5bclCcMthygdioYZD"

def send_whatsapp_message(recipient_number: str, message_text: str):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Send Response:", response.status_code)
    print(response.json())
    return response


def send_whatsapp_buttons(recipient_number: str):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "👋 Welcome to WhatsApp Shop!\nPlease choose an option:"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "browse_products",
                            "title": "🛍 Browse Products"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "view_cart",
                            "title": "🛒 View Cart"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "place_order",
                            "title": "📦 Place Order"
                        }
                    }
                ]
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Send Response:", response.status_code)
    print(response.json())
    return response


def send_product_list(recipient_number: str):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "🛍 Product Catalog"
            },
            "body": {
                "text": "Please select a product to view details:"
            },
            "footer": {
                "text": "Tap a product below"
            },
            "action": {
                "button": "View Products",
                "sections": [
                    {
                        "title": "Available Products",
                        "rows": [
                            {
                                "id": "airpods_pro",
                                "title": "🎧 AirPods Pro",
                                "description": "$249 - Noise Cancelling"
                            },
                            {
                                "id": "samsung_watch",
                                "title": "⌚ Samsung Galaxy Watch",
                                "description": "$199 - AMOLED Display"
                            },
                            {
                                "id": "jbl_headphones",
                                "title": "🎶 JBL Tune 760NC",
                                "description": "$129 - Bluetooth 5.0"
                            },
                            {
                                "id": "bose_qc45",
                                "title": "🎧 Bose QC 45",
                                "description": "$299 - Premium Audio"
                            }
                        ]
                    }
                ]
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Send Response:", response.status_code)
    print(response.json())
    return response
