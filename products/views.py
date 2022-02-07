from django.views import View
from django.http  import JsonResponse

from .models      import Product, Image

class ProductGroupDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message':'product_id error'}, status=400)
            
        productgroup_id = Product.objects.get(id=product_id).productgroup_id

        if not Product.objects.filter(productgroup_id=productgroup_id).exists():
            return JsonResponse({'message':'productgroup_id error'}, status=400)

        product        = Product.objects.filter(id=product_id)
        other_products = Product.objects.filter(productgroup_id=productgroup_id).exclude(id=product_id)
        products       = product.union(other_products)

        results = [
            {
                'name'               : product.name,
                'category'           : product.categorysubcategory.category.name,
                'subcategory'        : product.categorysubcategory.subcategory.name,
                'ml'                 : product.ml,
                'price'              : product.price,
                'description'        : product.description,
                'image_urls'         : [image.image_url for image in Image.objects.filter(product_id=product.id)],
                'image_descriptions' : [
                    image.image_url.split('/')[-1].split('.')[0] 
                for image in Image.objects.filter(product_id=product.id)
                ]
            } for product in products
        ]
        mls    = sorted([result['ml'] for result in results])
        prices = sorted([result['price'] for result in results])
        return JsonResponse({'products': results, 'mls': mls, 'prices': prices}, status=200)