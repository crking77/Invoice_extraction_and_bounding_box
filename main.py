from google import genai
import pymupdf 
from pydantic import Field, BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client  = genai.Client(api_key=API_KEY)
file_sample = client.files.upload(file="./invoice.pdf",config=dict(mime_type="application/pdf"))

class BoundingBox(BaseModel):
    box: list[int] = Field(..., description="this is where return position [y_min, x_min,y_max,x_max]")
    page: int = Field(...,description="this is page number where information is found and start from 1 ")
class TotalAmoutnField(BoundingBox):
    value: float = Field(...,description="total amount of invoice")
class TaxAmoutnField(BoundingBox):
    value: float = Field(...,description="total tax amount of invoice")
class SenderAmountField(BoundingBox):
    name: str = Field(..., description="The name of sender from invoice")
class AccountAmoutnField(BoundingBox):
    account_no: str = Field(...,description="account number in invoice")
class InvoiceModel(BaseModel):
    total: TotalAmoutnField
    tax: TaxAmoutnField
    sender: SenderAmountField
    account: AccountAmoutnField
prompt = """extract information from invoice
return ONLY JSON that matches the provided schema.
if a field is missing set it to NULL (and box =[0,0,0,0])
"""
response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents= [file_sample,prompt],
    config= {
        "response_mime_type": "application/json",
        "response_schema" : InvoiceModel.model_json_schema()
    }
)
invoice = InvoiceModel.model_validate_json(response.text)
print(invoice.model_dump())
items_to_draw = [
    ("TOTAL", invoice.total.box, invoice.total.page),
    ("TAX", invoice.tax.box, invoice.tax.page),
    ("SENDER", invoice.sender.box, invoice.sender.page),
    ("ACCOUNT", invoice.account.box, invoice.account.page),
]
document = pymupdf.open("./invoice.pdf")
color = (1,0,0)
for name, box, page_no in items_to_draw:
    if box==[0,0,0,0] or page_no is None or not box:
        continue
    page = document[page_no-1]
    r = page.rect
    y0,x0,y1,x1 = box
    rect = pymupdf.Rect(
        x0/1000 * r.width,
        y0/1000 * r.height,
        x1/1000 * r.width,
        y1/1000 * r.height,
    )
    page.draw_rect(rect,color = color, width=2)
    page.insert_text((rect.x0, rect.y0-2),text = name,color = color)

document.save("output_invoice.pdf")
document.close()