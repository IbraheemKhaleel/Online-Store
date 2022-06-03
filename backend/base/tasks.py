
from __future__ import absolute_import, unicode_literals


from celery import shared_task
from django.db.models import Sum, F
from django.http import HttpResponse

from base.models import PurchaseProduct
import pandas

@shared_task
def salesreport():
    sales_data = PurchaseProduct.objects.filter(is_paid=True).values('product__name').annotate(
        total_sales=Sum('product__selling_price'), countInStock=F('product__countInStock'))
    columns = [
        'product__name',
        'total_sales',
        'countInStock'
    ]
    df1 = pandas.DataFrame(sales_data, columns=columns)
    response = HttpResponse(content_type="text/ms-excel")
    response[
        "Content-Disposition"
    ] = 'attachment; filename="sales_report.xls"'
    df1.to_excel(response, sheet_name='sales report')
    return response