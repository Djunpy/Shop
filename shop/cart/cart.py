from decimal import Decimal
from django.conf import settings
from main.models import Product


class Cart(object):
    """Инициализация обьекта корзины. с помощью MIDDLEWARE текущ
    сессия становится доступна в объекте request"""
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохранение пустой корзины в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину, или обновление его количества"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную, и сохраняем
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины, и сохраняем результат"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """Для отображения списка товаров, нужно иметь возможность проходить
        в цикле по обьектам Product, для этого используем данный метод"""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину
        products = Product.objects.filter(id__in=product_ids)
        # Создаем копию обьекта корзины
        cart = self.cart.copy()
        # Получаем сохраненные товары сохраненные в корзине
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            # Получаем price и преобразуем его в decimal
            item['price'] = Decimal(item['price'])
            # Считаем общую стоимость всех товаров
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Отображение корзины"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Получение общего количества товаров"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        self.save()