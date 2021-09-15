from rest_framework.test import APITestCase

from .models import Articulo


class ArticuloTestCases(APITestCase):
    def setUp(self):
        Articulo.objects.create(identificador="QQQ", nombre="Lapicero", 
            descripcion="Lapiz marca bic", unidades=15, precio_sin_impuestos=1000)

    def test_get_article(self):
        response = self.client.get("/Articulo/")
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['nombre'], "Lapicero")

    def test_add_article(self):
        data = {
            "identificador": "AAA",
            "nombre": "Reloj",
            "descripcion": "Reloj marca Q&Q",
            "unidades": 12,
            "precio_sin_impuestos": 145
        }
        response = self.client.post("/Articulo/", data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['nombre'], "Reloj")
    
    def test_update_article(self):
        data = {
            "unidades": 55
        }
        response = self.client.patch("/Articulo/QQQ/", data)    
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['unidades'], 55)

    def test_delete_article(self):
        response_delete = self.client.delete("/Articulo/QQQ/")
        response_get = self.client.get("/Articulo/QQQ/")  

        self.assertEqual(response_delete.status_code, 204)
        self.assertEqual(response_get.status_code, 404)

class PedidoTestCases(APITestCase):
    def setUp(self):
        Articulo.objects.create(identificador="QQQ", nombre="Lapicero", 
            descripcion="Lapiz marca bic", unidades=15, precio_sin_impuestos=1000)
        Articulo.objects.create(identificador="WWW", nombre="Cuaderno", 
            descripcion="Cuaderno marca norma", unidades=32, precio_sin_impuestos=2500)
        
        data = {
            "numero": 1,
            "porcentaje_impuesto": 5,
            "moneda": "COP",
            "articulos": ['QQQ']
        }

        self.client.post("/PedidoList/", data)
    
    def test_get_pedido(self):
        response = self.client.get("/PedidoList/")
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['precio_sin_impuestos'], 1000)

    def test_add_pedido(self):
        data = {
            "numero": 2,
            "porcentaje_impuesto": 10,
            "moneda": "COP",
            "articulos": ['QQQ','WWW']
        }
        response = self.client.post("/PedidoList/", data)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        # Testeando el calculo automatico del precio sin impuesto 
        self.assertEqual(result['precio_sin_impuestos'], 3500)
        # Testeando el calculo automatico del precio total (es decir con impuesto)
        self.assertEqual(result['precio_total'], 3850)

    def test_update_pedido(self):
        #Se actualizo el % de impuesto y se agrego un segundo articulo
        data = {
            "numero": 1,
            "porcentaje_impuesto": 15,
            "moneda": "COP",
            "articulos": ['QQQ','WWW']
        }
        response = self.client.put("/PedidoList/1/", data)    
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['porcentaje_impuesto'], 15)
        self.assertEqual(result['articulos'], ['QQQ','WWW'])
        self.assertEqual(result['precio_sin_impuestos'], 3500)
        self.assertEqual(result['precio_total'], 4025)

    def test_delete_pedido(self):
        response_delete = self.client.delete("/PedidoList/1/")
        response_get = self.client.get("/PedidoList/1/")  

        self.assertEqual(response_delete.status_code, 204)
        self.assertEqual(response_get.status_code, 404)

class FiltroPedidoTestCases(APITestCase):
    def setUp(self):
        Articulo.objects.create(identificador="QQQ", nombre="Lapicero", 
            descripcion="Lapiz marca bic", unidades=15, precio_sin_impuestos=1000)
        Articulo.objects.create(identificador="WWW", nombre="Cuaderno", 
            descripcion="Cuaderno marca norma", unidades=32, precio_sin_impuestos=2500)
        
        data = {
            "numero": 1,
            "porcentaje_impuesto": 5,
            "moneda": "COP",
            "articulos": ['QQQ']
        }

        self.client.post("/PedidoList/", data)

        data2 = {
            "numero": 11,
            "porcentaje_impuesto": 5,
            "moneda": "COP",
            "articulos": ['QQQ']
        }

        self.client.post("/PedidoList/", data2)
    
    def test_filtro_id_pedido(self):
        #testeando que devuelva exactamente el pedido con el id(numero) 1
        response = self.client.get("/PedidoList/?id=1")
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['numero'], 1)

class PedidoPorArticuloTestCases(APITestCase):
    def setUp(self):
        Articulo.objects.create(identificador="QQQ", nombre="Lapicero", 
            descripcion="Lapiz marca bic", unidades=15, precio_sin_impuestos=1000)
        Articulo.objects.create(identificador="WWW", nombre="Cuaderno", 
            descripcion="Cuaderno marca norma", unidades=32, precio_sin_impuestos=2500)
        
        data = {
            "numero": 1,
            "porcentaje_impuesto": 5,
            "moneda": "COP",
            "articulos": ['QQQ']
        }

        self.client.post("/PedidoList/", data)

        data2 = {
            "numero": 2,
            "porcentaje_impuesto": 5,
            "moneda": "COP",
            "articulos": ['QQQ','WWW']
        }

        self.client.post("/PedidoList/", data2)
    
    def test_filtro_id_pedido(self):
        #testeando que devuelva exactamente el pedido con el id(numero) 1
        responseOne = self.client.get("/PedidoList/articulos/1/")
        responseTwo = self.client.get("/PedidoList/articulos/2/")
        resultOne = responseOne.json()
        resultTwo = responseTwo.json()
        self.assertEqual(responseOne.status_code, 200)
        self.assertEqual(responseTwo.status_code, 200)
        self.assertEqual(resultOne, ['QQQ'])
        self.assertEqual(resultTwo, ['QQQ','WWW'])
    
