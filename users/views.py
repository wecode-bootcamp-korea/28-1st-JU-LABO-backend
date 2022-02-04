import json
import datetime

from django.views import View
from django.http  import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.models import User, Cart

class CartView(View):
    # @login_decorator
    def post(self, request):
        # user_id = request.user
        try:  
            data = json.loads(request.body)  
            user_id    = data['user_id']
            product_id = data['product_id']
            quantity   = data['quantity']

            cart, is_created = Cart.objects.get_or_create(
                user_id=user_id, product_id=product_id)

            cart.quantity = quantity
            cart.save()
            return JsonResponse({'message': '등록성공'}, status=200)
        except KeyError as k:
            return JsonResponse({'message': k}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User id Does Not Exist'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Product id Does Not Exist'}, status=400)


    # @login_decorator
    def get(self, request):

        # user_id = request.user
        try:
            user_id = 1
            
            items = Cart.objects.filter(user_id=user_id)
            
            results = [
                {
                    'product_name' : item.product.name,
                    'quantity'     : item.quantity,
                    'item_price'   : item.product.price * item.quantity,
                    'subcategory'  : item.product.categorysubcategory.subcategory.name,
                    'size'         : item.product.ml
                } 
                for item in items]

            total_price = 0
            for result in results:
                total_price += result['item_price']
            
            order_date = datetime.datetime.now()

            return JsonResponse({'results': results, 
                    'total_price': total_price, 
                    'order_date': order_date}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User id Does Not Exist'}, status=400)

    # @login_decorator
    def delete(self, request):
        # user_id = request.user
        try:
            data       = json.loads(request.body)
            user_id    = data['user_id']
            product_id = data['product_id']
            
            product = Cart.objects.get(user_id=user_id, product_id=product_id)
            product.delete()
            return JsonResponse({'message': '삭제성공'}, status=200)
        except KeyError as k:
            return JsonResponse({'message': k}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User id Does Not Exist'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Product id Does Not Exist'}, status=400)
