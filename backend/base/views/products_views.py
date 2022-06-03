import pandas
from django.db.models import Sum, F
from django.forms import model_to_dict
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.helpers.decorators import admin_or_staff_login_required
from base.models import Product, PurchaseProduct
from base.serializers import ProductSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProductsView(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProductView(request, pk):
    product = Product.objects.filter(id=pk).first()
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
@admin_or_staff_login_required
def ProductStocksView(request):
    try:
        stocks = Product.objects.filter(is_delete=False).values('name', 'countInStock')
        return Response({
            'message': 'Successfully fetched stocks_list',
            'status_code': 200,
            'data': stocks
        })
    except Exception as e:
        return Response({
            'message': str(e),
            'status_code': 400,
            'data': []
        })


@api_view(['POST'])
@admin_or_staff_login_required
def createProduct(request):
    try:
        data = request.data
        if data['selling_price'] < data['purchase_price']:
            return Response({
                'message': 'Selling price should be greater than purchasing price',
                'status_code': 401,
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Successfully created the product',
            'status_code': 200,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'message': str(e),
            'status_code': 400,
            'data': []
        })


@api_view(['PATCH'])
@admin_or_staff_login_required
def updateProduct(request, pk):
    data = request.data
    try:
        product_obj = Product.objects.get(id=pk)
        serializer = ProductSerializer(product_obj, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Successfully updated the product',
            'status_code': 200,
            'data': serializer.data
        })
    except Product.DoesNotExist as e:
        return Response({
            'message': str(e),
            'status_code': 400,
            'data': []
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'message': str(e),
            'status_code': 400,
            'data': []
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PurchaseProductView(request):
    purchase_product = PurchaseProduct.objects.create(user=request.user, product_id=request.data['product'],
                                                      is_paid=True)
    Product.objects.filter(id=request.data['product']).update(countInStock=F('countInStock') - 1)
    return Response({
        'message': 'Successfully purchased the product',
        'status_code': 200,
        'data': model_to_dict(purchase_product)
    })


@api_view(['GET'])
@admin_or_staff_login_required
def SalesReport(request):
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

