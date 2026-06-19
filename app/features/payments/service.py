import os
import razorpay
import hmac
import hashlib
import requests

from fastapi import HTTPException
from dotenv import load_dotenv


load_dotenv()


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")


if not RAZORPAY_KEY_ID or not RAZORPAY_SECRET:
    raise RuntimeError(
        "Razorpay keys missing"
    )



client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_SECRET
    )
)



def create_razorpay_order(amount: int):

    try:

        print("Creating Razorpay order")
        print("Amount:", amount)
        print("Key:", RAZORPAY_KEY_ID)



        order = client.order.create(
            {
                "amount": int(amount * 100),
                "currency": "INR",
                "receipt": "cart_payment",
            }
        )


        print("ORDER CREATED:", order)


        return {

            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]

        }


    except requests.exceptions.ConnectionError as e:

        print(
            "RAZORPAY CONNECTION ERROR:",
            e
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to connect to Razorpay"
        )


    except Exception as e:

        print(
            "RAZORPAY ERROR:",
            e
        )

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )




def verify_payment(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature
):


    generated_signature = hmac.new(

        bytes(
            RAZORPAY_SECRET,
            "utf-8"
        ),

        bytes(
            f"{razorpay_order_id}|{razorpay_payment_id}",
            "utf-8"
        ),

        hashlib.sha256

    ).hexdigest()



    print(
        "Generated:",
        generated_signature
    )

    print(
        "Received:",
        razorpay_signature
    )


    return (
        generated_signature ==
        razorpay_signature
    )