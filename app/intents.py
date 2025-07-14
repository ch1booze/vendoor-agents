from enum import StrEnum


class CustomerIntent(StrEnum):
    GREETING = "greeting"
    INQUIRE_ABOUT_PRODUCTS = "inquire_about_products"
    CHECK_PRODUCT_AVAILABILITY = "check_product_availability"
    ASK_FOR_PRICE = "ask_for_price"
    REQUEST_PRODUCT_DETAILS = "request_product_details"

    PLACE_ORDER = "place_order"
    MODIFY_ORDER = "modify_order"
    VIEW_CART = "view_cart"
    INITIATE_CHECKOUT = "initiate_checkout"
    INQUIRE_ABOUT_PAYMENT = "inquire_about_payment"
    INQUIRE_ABOUT_DELIVERY = "inquire_about_delivery"
    CHECK_ORDER_STATUS = "check_order_status"
    CANCEL_ORDER = "cancel_order"

    REQUEST_HUMAN_AGENT = "request_human_agent"


customer_intent_explanations = {
    CustomerIntent.GREETING: "The customer is initiating a conversation with a greeting. Examples: 'Hello', 'Hi', 'Good morning'",
    CustomerIntent.INQUIRE_ABOUT_PRODUCTS: "The customer is asking general questions about the products available. Examples: 'What products do you offer?', 'Can you tell me about your products?'",
    CustomerIntent.CHECK_PRODUCT_AVAILABILITY: "The customer is checking if a specific product is in stock or available. Examples: 'Is this product available?', 'Do you have this item in stock?'",
    CustomerIntent.ASK_FOR_PRICE: "The customer is asking for the price of a specific product. Examples: 'How much does this cost?', 'What is the price of this item?'",
    CustomerIntent.REQUEST_PRODUCT_DETAILS: "The customer is requesting more detailed information about a specific product. Examples: 'Can you give me more details about this product?', 'What are the specifications of this item?'",
    CustomerIntent.PLACE_ORDER: "The customer is indicating that they want to place an order for a product. Examples: 'I would like to place an order.', 'How can I order this item?'",
    CustomerIntent.MODIFY_ORDER: "The customer wants to make changes to an existing order. Examples: 'I need to change my order.', 'Can I update my order details?'",
    CustomerIntent.VIEW_CART: "The customer wants to view the items in their shopping cart. Examples: 'Can I see my cart?', 'What items are in my cart?'",
    CustomerIntent.INITIATE_CHECKOUT: "The customer is ready to proceed to checkout to complete their purchase. Examples: 'I want to checkout.', 'How do I proceed to checkout?'",
    CustomerIntent.INQUIRE_ABOUT_PAYMENT: "The customer is asking about payment methods or payment-related questions. Examples: 'What payment methods do you accept?', 'How can I pay for my order?'",
    CustomerIntent.INQUIRE_ABOUT_DELIVERY: "The customer is asking about delivery options, times, or costs. Examples: 'What are my delivery options?', 'How long will delivery take?'",
    CustomerIntent.CHECK_ORDER_STATUS: "The customer wants to know the current status of their order. Examples: 'What is the status of my order?', 'Has my order been shipped?'",
    CustomerIntent.CANCEL_ORDER: "The customer wants to cancel an existing order. Examples: 'I need to cancel my order.', 'How can I cancel my order?'",
    CustomerIntent.REQUEST_HUMAN_AGENT: "The customer wants to speak to a human agent for assistance. Examples: 'Can I speak to a human agent?', 'I need to talk to a customer service representative.'",
}
