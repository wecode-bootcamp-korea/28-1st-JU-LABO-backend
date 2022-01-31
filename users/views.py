import json
import datetime

from django.views import View
from django.http  import JsonResponse
from django.db.models import F

from users.models import User, Cart

class CartView(View):
    def post(self, request):
        data = json.loads(request.body)

        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data['quantity']

        cart, is_created = Cart.objects.get_or_create(
            user_id=user_id, product_id=product_id)
            
        cart.quantity = quantity
        cart.save()

        return JsonResponse({'message': '등록성공'}, status=200)

    def get(self, request):
        # user_id = data['user_id']
        # data = json.loads(request.body)
        user_id = 1
        # user_id = data['user_id']
        
        items = Cart.objects.filter(user_id=user_id)
        
        results = [
            {
                'product_name' : item.product.name,
                'quantity' : item.quantity,
                'item_price' : item.product.price * item.quantity,
                'subcategory' : item.product.categorysubcategory.subcategory.name,
                'size' : item.product.ml
            } 
            for item in items]

        total_price = 0
        for result in results:
            total_price += result['item_price']
        
        order_date = datetime.datetime.now()

        return JsonResponse({'results': results, 
                    'total_price': total_price, 
                    'order_date': order_date}, status=200)