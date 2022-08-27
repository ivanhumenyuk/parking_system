from app import db
from app.models import (
    Region,
    RegionLang,
    CountryRegion,
    CountryLang,
    Country,
    Order,
    Address,
    OrderProduct,
    OrderShipping,
    Fulfillment,
    FulfillmentProduct,
    Payment,
    PaymentOrder,
    Refund,
    RefundProduct,
)


# regions = []
# region_langs = []
# country_region = []
# db.session.rollback()
# # countries = Country.query.all()
# for country in Country.query.all():
#     db.session.add(Region(code=country.code))
# db.session.commit()
#
# for region in Region.query.all():
#     country = Country.query.filter_by(code=region.code).one_or_none()
#     if country:
#         for country_lang in CountryLang.query.filter_by(country_id=country.id).all():
#             region_langs.append(
#                 RegionLang(
#                     region_id=region.id,
#                     lang_id=country_lang.language_id,
#                     name=country_lang.name,
#                 )
#             )
# db.session.add_all(region_langs)
# db.session.commit()
#
# for region in Region.query.all():
#     country = Country.query.filter_by(code=region.code).one_or_none()
#     country_region.append(CountryRegion(country_id=country.id, region_id=region.id))
# db.session.add_all(country_region)
# db.session.commit()


db.session.add(
    address := Address(
        country_id=2,
        city="Kiev",
        state="Kiev",
        street1="Borshagovskaya",
        street2="135A",
        zip_code="064890",
        company="",
        user_id=2,
        email="123gog@gmail.com",
        phone="+380955279470",
        receiver_name="Eren Yeger",
    )
)
db.session.flush()
db.session.add(
    order := Order(
        user_id=2,
        fulfillment_due_date=2,
        type_id=2,
        product_cost=2080,
        address_id=address.id,
        order_status_id=2,
        currency_id=1,
        user_comment="User comment to current order",
        order_fulfillment_status_id=2,
        order_payment_status_id=1,
        delivery_date_est_max=3,
        delivery_date_est_min=2,
    )
)
db.session.flush()

db.session.add(
    order_product := OrderProduct(
        product_variation_id=2,
        product_id=1,
        order_id=order.id,
        price=1290,
        product_name="Product Name",
        processing_min=1,
        processing_max=5,
        delivery_cost=20,
        delivery_additional_item_cost=170,
        quantity=3,
    )
)
db.session.flush()
db.session.add(
    order_shipping := OrderShipping(
        delivery_type_id=2,
        shipping_cost=110,
        order_id=order.id
    )
)
db.session.flush()
db.session.add(
    fulfillment := Fulfillment(
        fulfillment_status_id=1,
        order_id=order.id
    )
)
db.session.flush()
db.session.add(
    fulfillment_product := FulfillmentProduct(
        fulfillment_id=fulfillment.id,
        order_product_id=order_product.id,
        quantity=1
    )
)

db.session.flush()
db.session.add(
    payment := Payment(
        payment_status_id=1,
        payment_provider_id=2,
        amount=1200,
        transaction="Transaction text",
        user_id="Payment user id",
    )
)
db.session.flush()
db.session.add(
    payment_order := PaymentOrder(
        payment_id=payment.id,
        order_id=order.id,
    )
)
db.session.flush()
db.session.add(
    refund := Refund(
        order_id=order.id,
        refund_status_id=1,
    )
)
db.session.flush()
db.session.add(
    refund_product := RefundProduct(
        refund_id=refund.id,
        order_product_id=order_product.id,
        quantity=2,
    )
)


db.session.commit()
