from myapp.models import Product
from decimal import Decimal

# Ova klasa upravlja korpom koja je spremljena u sesiji: dodaje proizvode, mijenja količine, briše stavke i računa cijenu. Ona nije Django model i ne pravi novu tabelu.
class Cart():
    def __init__(self,request): # inicijalizacija korpe
        self.session = request.session # pristup sesiji
        cart = request.session.get('cart') # uzima postojeću korpu iz sesije. Ako ključ 'cart' ne postoji, .get() vraća None.
        # Ako korpa ne postoji u sesiji, kreira se prazna korpa i sprema u sesiju.
        if 'cart' not in request.session:
            cart = self.session['cart']={}
        self.cart = cart # čuva pristup rječniku klase Cart u self.cart za lakši pristup. 
    
    # broj komada u korpi    
    def __len__(self):
        return sum (int(item['qty']) for item in self.cart.values())
    
    # ukupna vrijednost korpe
    def get_total_price(self):
        return sum(Decimal(item['price']) * Decimal(item['qty']) for item in self.cart.values())

    # iteracija kroz proizvode u korpi
    def __iter__(self):
        product_ids = self.cart.keys() # uzima sve ključeve iz rječnika korpe, koji su ID-evi proizvoda
        products = Product.objects.filter(id__in=product_ids) # uzima sve proizvode iz baze podataka čiji su ID-evi u listi product_ids
        cart = self.cart.copy() # pravi kopiju rječnika korpe da bi se izbjeglo mijenjanje originalnog rječnika dok se iterira kroz njega

        # Dodaje proizvodne objekte u rječnik korpe tako da se mogu koristiti u šablonima. Svaki proizvod se dodaje u rječnik pod ključem koji je njegov ID.
        for product in products:
            cart[str(product.id)]['product']=product 

        # Iterira kroz stavke u korpi i računa ukupnu cijenu za svaku stavku. Svaka stavka se vraća kao rječnik koji sadrži proizvod, cijenu, količinu i ukupnu cijenu.
        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['qty']=Decimal(item['qty'])
            item['total']=item['price']*item['qty']
            yield item

        


    # dodavanje proizvoda u korpu ili mijenjanje njegove količine
    def add(self,product,product_qty):
        product_id = product.id
        if product_id in self.cart:
            self.cart[product_id]['qty']= product_qty
            
        else:
            self.cart[product_id]={'price':str(product.price),'qty':product_qty}
            
        self.session.modified=True            
    
    # brisanje proizvoda iz korpe
    def delete(self,product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True

    # mijenjanje količine proizvoda u korpi
    def update(self,product,qty):
        product_id = str(product)
        product_quantity = qty
        if product_id in self.cart:
            self.cart[product_id]['qty']=product_quantity
        self.session.modified=True 
