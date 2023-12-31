from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from .serializers import *
import stripe
import string
import random

stripe.api_key = "sk_test_1srueIi8nRsob787g1O3pS0z00NR4rSjbb"


# Create your views here.

class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        product_id = request.data['id']
        product_obj = Product.objects.get(id=product_id)
        incomplete_cart = Cart.objects.filter(
            customer=request.user.profile).filter(complete=False).first()

        try:
            if incomplete_cart:
                this_product_in_cart = incomplete_cart.cartproduct_set.filter(
                    product=product_obj)
                if this_product_in_cart.exists():
                    cart_product = CartProduct.objects.filter(
                        product=product_obj).filter(cart__complete=False).first()
                    cart_product.quantity += 1
                    cart_product.subtotal += product_obj.selling_price
                    cart_product.save()
                    incomplete_cart.total += product_obj.selling_price
                    incomplete_cart.save()
                else:
                    new_cart_product = CartProduct.objects.create(
                        cart=incomplete_cart,
                        price=product_obj.selling_price,
                        quantity=1,
                        subtotal=product_obj.selling_price
                    )
                    new_cart_product.product.add(product_obj)
                    incomplete_cart.total += product_obj.selling_price
                    incomplete_cart.save()
            else:
                Cart.objects.create(
                    customer=request.user.profile, total=0, complete=False)
                new_cart = Cart.objects.filter(
                    customer=request.user.profile).filter(complete=False).first()
                new_cart_product = CartProduct.objects.create(
                    cart=new_cart,
                    price=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
                new_cart_product.product.add(product_obj)
                new_cart.total += product_obj.selling_price
                new_cart.save()

            message = {
                'error': False, 'message': "Product added to Cart", "productid": product_id}

        except Exception as e:
            print(e)
            message = {
                'error': True, 'message': "Product Not added to Cart! Something went Wrong"}

        return Response(message)


class MyCart(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        query = Cart.objects.filter(customer=request.user.profile)
        serializers = CartSerializer(query, many=True)
        all_data = []
        for cart in serializers.data:
            cart_product = CartProduct.objects.filter(cart=cart["id"])
            cart_product_serializer = CartProductSerializer(
                cart_product, many=True)
            cart["cart_product"] = cart_product_serializer.data
            all_data.append(cart)
        return Response(all_data)


class UpdateCartProduct(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cp_obj = CartProduct.objects.get(id=request.data["id"])
        cart_obj = cp_obj.cart

        cp_obj.quantity += 1
        cp_obj.subtotal += cp_obj.price
        cp_obj.save()

        cart_obj.total += cp_obj.price
        cart_obj.save()
        return Response({"message": "CartProduct Add Update", "product": request.data['id']})


class EditCartProduct(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cp_obj = CartProduct.objects.get(id=request.data["id"])
        cart_obj = cp_obj.cart

        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.price
        cp_obj.save()

        cart_obj.total -= cp_obj.price
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
        return Response({"message": "CartProduct Add Update", "product": request.data['id']})


class DeleteCartProduct(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cp_obj = CartProduct.objects.get(id=request.data['id'])
        cp_obj.delete()
        return Response({"message": "CartProduct Deleted", "product": request.data['id']})


class DeleteFullCart(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        try:
            card_obj = Cart.objects.get(id=request.data['id'])
            card_obj.delete()
            message = {"message": "Cart Deleted"}
        except Exception as e:
            print(e)
            message = {"message": "Something went wrong"}
        return Response(message)


class OrderViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        query = Order.objects.filter(cart__customer=request.user.profile)
        serializers = OrderSerializer(query, many=True)
        all_data = []
        for order in serializers.data:
            cart_product = CartProduct.objects.filter(
                cart_id=order['cart']['id'])
            cart_product_serializer = CartProductSerializer(
                cart_product, many=True)
            order['cart_product'] = cart_product_serializer.data
            all_data.append(order)
        return Response(all_data)

    def retrieve(self, request, pk=None):
        try:
            queryset = Order.objects.get(id=pk)
            serializers = OrderSerializer(queryset)
            data = serializers.data
            all_data = []
            cart_product_obj = CartProduct.objects.filter(
                cart_id=data['cart']['id'])
            cart_product_serializer = CartProductSerializer(
                cart_product_obj, many=True)
            data['cart_product'] = cart_product_serializer.data
            all_data.append(data)
            message = {"error": False, "data": all_data}
        except Exception as e:
            print(e)
            message = {"error": True, "data": "No data Found for This id"}

        return Response(message)

    def destroy(self, request, pk=None):
        try:
            order_obj = Order.objects.get(id=pk)
            cart_obj = Cart.objects.get(id=order_obj.cart.id)
            order_obj.delete()
            cart_obj.delete()
            message = {"error": False,
                       "message": "Order deleted", "order id": pk}
        except Exception as e:
            print(e)
            message = {"error": True, "message": "Order Not Found"}
        return Response(message)

    def create(self, request):
        print(request.data)
        cart_id = request.data["cartId"]
        cart_obj = Cart.objects.get(id=cart_id)
        address = request.data["address"]
        mobile = request.data["mobile"]
        email = request.data["email"]
        cart_obj.complete = True
        cart_obj.save()
        created_order = Order.objects.create(
            cart=cart_obj,
            address=address,
            mobile=mobile,
            email=email,
            total=cart_obj.total,
            discount=3,
        )

        return Response({"message": "Order Completed", "cart id": cart_id, "order id": created_order.id})


class AddAdressAPIView(generics.GenericAPIView):
    serializer_class = AddAdressSerializer

    def post(self, request):
        user = get_buyer(request)
        order_qs = Order.objects.filter(buyer=user, in_processing=False)

        if order_qs.exists():
            order = order_qs[0]

            if request.data['use_default']:
                address_qs = Address.objects.filter(
                    buyer=user, is_default=True)
                if address_qs.exists():
                    address = address_qs[0]
                    order.address = address
                    order.save()
                    return Response({'success:': 'user using the default adress'}, status=status.HTTP_200_OK)

                else:
                    return Response({'error:': 'user has no default address'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            address = serializer.save()
            address.buyer = user
            address.save()

            if request.data['is_default']:
                try:
                    prevouis_default = Address.objects.get(
                        buyer=user, is_default=True)
                    prevouis_default.is_default = False
                    prevouis_default.save()
                except:
                    pass
                address.is_default = True
                address.save()

            order.address = address
            order.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


def GenOrderNum():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class PaymentAPIView(generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        user = get_buyer(request)
        token = request.data['public_key']
        payment_method_id = request.data['payment_method_id']

        try:
            order = Order.objects.get(buyer=user, in_processing=False)
            amount = int(order.get_order_total() * 100)
            try:
                # check if this customer is aleaready exists in stripe
                customer_data = stripe.Customer.list(
                    email=user.email).data
                if len(customer_data) == 0:
                    # its mean that the customer is not exists
                    # creat customer btw the email should be passed from the front end as well ot get it from the acess token as i did now
                    customer = stripe.Customer.create(
                        email=user.email,
                        payment_method=payment_method_id
                    )
                else:
                    # get the customer
                    customer = customer_data[0]
                    extra_msg = "Customer already existed."
                # lets charg the custumer rn
                charge = stripe.PaymentIntent.create(
                    customer=customer,
                    payment_method=payment_method_id,
                    currency='usd',
                    amount=amount,
                    confirm=True
                )
                payment = Payment(
                    stripe_charge_id=charge['id'],
                    amount=order.get_order_total()
                )

                payment.save()

                ordered_items = order.products.all()
                for item in ordered_items:
                    item.ordered = True
                    item.save()

                order.payment = payment
                order.number = GenOrderNum()
                order.in_processing = True
                order.save()
                return Response({'success:': 'payment went great'}, status=status.HTTP_200_OK)
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                print('Status is: %s' % e.http_status)
                print('Type is: %s' % e.error.type)
                print('Code is: %s' % e.error.code)
                # param is '' in this case
                print('Param is: %s' % e.error.param)
                print('Message is: %s' % e.error.message)
                return Response({'error:': 'try again later'}, status=status.HTTP_400_BAD_REQUEST)

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                return Response({'error:': 'Rate limit error'}, status=status.HTTP_400_BAD_REQUEST)

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                return Response({'error:': 'invalid paramiters'}, status=status.HTTP_400_BAD_REQUEST)

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                return Response({'error:': 'not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                return Response({'error:': 'network error'}, status=status.HTTP_400_BAD_REQUEST)

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                return Response({'error:': 'something wents worng you will not charged please try again'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # send email to ouselves
                return Response({'error:': 'there is some thing to fix in our website you will not charged please try again later'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error:': 'No such order'}, status=status.HTTP_400_BAD_REQUEST)
