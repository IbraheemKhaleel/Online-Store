from django.urls import path


from base.views import products_views as views

urlpatterns = [
    path('', views.ProductsView, name='product'),
    path('<str:pk>', views.ProductView, name='product'),
    path('stocks/', views.ProductStocksView, name='product'),
    path('create-product/', views.createProduct, name='create-product'),
    path('update-product/<str:pk>', views.updateProduct, name='update-product'),
    path('buy-product/', views.PurchaseProductView, name='buy-product'),
    path('sales-report/', views.SalesReport, name='sales-report'),


]