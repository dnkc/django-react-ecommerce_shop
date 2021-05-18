from django.urls import path
from base.views import product_views as views



urlpatterns = [
    # path('', views.getRoutes, name="routes"),
    path('', views.getProducts, name="products"),
    path('create/', views.createProduct, name='product-create'),
    path('uploadimage/', views.uploadImage, name='product-image'),
    path('top/', views.getTopProducts, name='products-top'),

    path('<str:pk>/reviews/', views.createProductReview, name='create-review'),
    path('<str:pk>/', views.getProduct, name="product"),
    
    path('delete/<str:pk>/', views.deleteProduct, name='product-delete'),
    path('edit/<str:pk>/', views.updateProduct, name='product-edit')

]


