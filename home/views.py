from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseNotAllowed

class IndexView(APIView):
    def get(self, request):
        mens_categories = Category.objects.filter(gender='M')
        womens_categories = Category.objects.filter(gender='W')

        cart_item = CartItem.objects.all()

        cart_item_count = CartItem.objects.filter(name=request.user).count()
        
        cart_total_price = CartItem.objects.filter(name=request.user).aggregate(total_price=Sum('total_price'))['total_price']

        context = {
            'mens_categories': mens_categories,
            'womens_categories': womens_categories,
            'cart_item_count': cart_item_count,
            'cart_total_price': cart_total_price,
            'cart_item': cart_item,
        }
        return render(request, 'index.html', context)
    
class ProductView(APIView):
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product Added Successfully'}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Get category IDs from the request
        category_men_id = request.GET.get('category_men')
        category_women_id = request.GET.get('category_women')
        category_kids_id = request.GET.get('category_kids')

        # Filter products based on the selected category IDs
        if category_men_id:
            products = Product.objects.filter(category_id=category_men_id)
        elif category_women_id:
            products = Product.objects.filter(category_id=category_women_id)
        elif category_kids_id:
            products = Product.objects.filter(category_id=category_kids_id)
        else:
            products = Product.objects.all()

        mens_categories = Category.objects.filter(gender='M')
        womens_categories = Category.objects.filter(gender='W')
        kids_categories = Category.objects.filter(gender='K')

        serializer = ProductSerializer(products, many=True)

        cart_item = CartItem.objects.all()

        cart_item_count = CartItem.objects.filter(name=request.user).count()
        
        cart_total_price = CartItem.objects.filter(name=request.user).aggregate(total_price=Sum('total_price'))['total_price']

        return render(request, 'product.html', {'products': serializer.data,'mens_categories': mens_categories,
            'womens_categories': womens_categories,
            'kids_categories': kids_categories,'cart_item_count': cart_item_count,'cart_total_price': cart_total_price,'cart_item':cart_item})
    
    def put(self, request, id):
        try:
            cart = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'message':'Cart not fount'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            cart = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'message':'Cart not fount'},status=status.HTTP_404_NOT_FOUND)
        
        cart.delete()
        return Response({'message':'Cart deleted successfully'},status=status.HTTP_200_OK)
    
class CategoryView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category Added Successfully'}, status=status.HTTP_201_CREATED)  # Return 201 Created
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors with 400 Bad Request

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_200_OK)
    
class ProductDetailView(APIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        mens_categories = Category.objects.filter(gender='M')
        womens_categories = Category.objects.filter(gender='W')
        kids_categories = Category.objects.filter(gender='K')

        serializer = ProductSerializer(product)

        product = get_object_or_404(Product, pk=id)

        cart_item = CartItem.objects.all()
        
        cart_item_count = CartItem.objects.filter(name=request.user).count()
        
        cart_total_price = CartItem.objects.filter(name=request.user).aggregate(total_price=Sum('total_price'))['total_price']

        return render(request, 'details.html', {'product': serializer.data,'mens_categories': mens_categories,
            'womens_categories': womens_categories,
            'kids_categories': kids_categories,'cart_item_count': cart_item_count,'cart_total_price': cart_total_price,'cart_item':cart_item})

class AddToCart(APIView):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return redirect('error_page') 

        total_price = product.price * quantity
        
        existing_cart_item = CartItem.objects.filter(name=request.user, product=product).first()
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.total_price += total_price
            existing_cart_item.save()
        else:
            CartItem.objects.create(
                name=request.user, 
                product=product,
                price=product.price,
                quantity=quantity,
                total_price=total_price
            )

        messages.success(request, f'“{product.name}” has been added to your cart.')
        
        return redirect(request.META.get('HTTP_REFERER', '/'))

class RemoveItem(APIView):
    def get(self, request, id):
        try:
            cart_item = CartItem.objects.filter(id=id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
class ViewCart(APIView):
    def get(self,request):
        cart_item = CartItem.objects.all()
        cart_total = cart_item.aggregate(total=Sum('total_price'))['total']

        mens_categories = Category.objects.filter(gender='M')
        womens_categories = Category.objects.filter(gender='W')
        kids_categories = Category.objects.filter(gender='K')

        cart_item_count = CartItem.objects.filter(name=request.user).count()
        
        cart_total_price = CartItem.objects.filter(name=request.user).aggregate(total_price=Sum('total_price'))['total_price']

        context = {'cart_item':cart_item,'cart_total':cart_total,'mens_categories': mens_categories,
            'womens_categories': womens_categories,
            'kids_categories': kids_categories,'cart_item_count':cart_item_count,'cart_total_price': cart_total_price,}
        
        return render(request,'viewcart.html',context)
    
class UpdateCart(APIView):
    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if key.startswith('item_id_'):
                item_id = key.split('_')[-1]
                quantity_key = f'quantity_{item_id}'
                if quantity_key in request.POST:
                    try:
                        quantity = int(request.POST[quantity_key])
                        cart_item = CartItem.objects.get(id=item_id)
                        cart_item.quantity = quantity
                        cart_item.total_price = cart_item.price * quantity
                        cart_item.save()
                    except CartItem.DoesNotExist:
                        pass
                    except ValueError:
                        pass

        return redirect('view')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])
    
    


class RecommendedView(APIView):
    def post(self,request):
        serializer = RecommendedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Product added successfully'},status=status.HTTP_201_CREATED)
        else:
            print('Serializer error',serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)