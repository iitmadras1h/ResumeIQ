from fastapi import FastAPI, Request
import razorpay

app = FastAPI()

client = razorpay.Client(auth=(
    "rzp_test_SSRER7EFytYsML",
    "LaeSPK56HLqC3IIoXLE8aLp5"
))

@app.post("/verify-payment")
async def verify_payment(request: Request):
    data = await request.json()
    payment_id = data.get("payment_id")

    try:
        payment = client.payment.fetch(payment_id)

        if payment["status"] == "captured":
            return {"status": "success"}
        else:
            return {"status": "failed"}

    except:
        return {"status": "failed"}