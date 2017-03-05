from django.db.models.aggregates import Sum
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.template.loader import  get_template
from django.template import Context
from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from models import Shop, Product, ProductsReceipt, Receipt
import pandas as pd
import datetime as dt

def three(request):
    # select = int(request.GET["select"])
    # time = int(request.GET["time"])
    # data = Receipt.objects.extra(select=({'receipt_date': "strftime('%H:%M', receipt_date)"})).values('date_new', 'receipt_week_day','receipt_items_qty' )
    data = Receipt.objects.values('receipt_date', 'receipt_week_day','receipt_items_qty' )
    data = pd.DataFrame.from_records(data)
    print  data
    # data = data.annotate(sum_total_price=Sum())
    # ser = data.to_datetime(data.index, format='%H:%M')
    print data.info()
    # data.index = pd.to_datetime(data.index, format='%H:%M:%S').dt.time
    data = data.resample('30min', on='receipt_date').sum() #.dropna('receipt_date')
    print dir(data)
    # data = data.pivot_table('receipt_week_day', index=data.index, columns='receipt_items_qty')
    # #
    # print data
    # return HttpResponse('1')

    return render_to_response('index.html', {'data': data.to_html()})


def form_select(request):
    shops = Shop.objects.filter(client_id=64).values('name').distinct()
    shop = []
    for item in shops:
        shop.append(item['name'])
    offset = pd.Timedelta('0 days')
    form = form_select(request.GET)
    if request.method == 'GET' and form.is_valid():
        datefrom = form.cleaned_data['date_from']
        dateto = form.cleaned_data['date_to']
        days = dateto - datefrom
        # for item in shops:
        #     shop[item['name']] = form.cleaned_data[item['name']]
    else:
        date_from = pd.to_datetime('2015-01-01')
        date_to = pd.to_datetime('2015-30-12')
        days = date_to - date_from
    print shops
    if days.days == 0:
        offset = pd.Timedelta('1 days')
    select = int(request.GET["select"])
    time = int(request.GET["select_time"])
    # select = 1
    # time = 3
    times = ["cast(strftime('%H', receipt_date) AS TEXT)|| ':'|| cast(strftime('%M', receipt_date)/10*10 AS TEXT)", "cast(strftime('%H', receipt_date) AS TEXT)|| ':'|| cast(strftime('%M', receipt_date)/30*30 AS TEXT)", "cast(strftime('%H', receipt_date) AS TEXT)|| ':'|| cast(strftime('%M', receipt_date)/60*60 AS TEXT)", "cast(strftime('%H', receipt_date)/2*2 AS TIME)", "cast(strftime('%H', receipt_date)/4*4 AS TIME)"]
    selects = ['receipt_items_qty', 'receipt_total_price', 'productsreceipt__qty']
    date = Receipt.objects.extra(select=({'date_new': times[time]})).order_by('date_new')
    receipt_select = date.values('date_new', 'receipt_week_day').annotate(sum_total_price=Sum(selects[select]))
    pandas_select = pd.DataFrame.from_records(receipt_select)
    data = pandas_select.pivot_table('sum_total_price', index='date_new', columns='receipt_week_day')
    data = data.rename(columns={'date_new':'Date','receipt_week_day':'Day', 0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'})
    data['sum'] = data.sum(axis=1)
    new = pd.DataFrame([data.sum()], index=['sum weeek day'])
    data = pd.concat([data, new], axis=0)
    return render_to_response('index.html', {'data': data.to_html()})


    # times = [['', '/10 * 10'], ['', '/30 *30'], ['', '/60 * 60'], ['/2 *2', '/60 * 60'], ['/4 * 4', '/60 * 60']]
    # select_time = "cast(strftime('%H', receipt_date) AS TIME)|| ':'|| cast(strftime('%M', receipt_date){1} AS TIME)".format(times[time][0], times[time][1])
    # # print select_time

    # select_time = "cast(strftime('%H', receipt_date)/4*4 AS TIME)"
    # data = data.add(ser, axis=0)
    # print data
    # print new
    # ser = ser[0].iloc[0:3]
    # ser = ser[0].iloc(1)
    # ser = ser[0].T
    # ser = pd.Series(ser)
    # print ser.index.values
    # print ser.columns, 'EEEEE'

    # print ser[0]
    # ser = ser.pivot(index=RangeIndex(start=0, stop=1, step=1) , columns=ser.index, values=ser.values)
    # print ser
    # ser = pd.DataFrame(pd.Series([17158.0, 17412.0, 17161.0, 20607.0, 20206.0, 17974.0, 14424.0, 124942.0]), index=['0'], columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'sum'])
    # print ser
    # print data.index
    # print data
    # data.index = pd.to_datetime(data.index).dt.time

    # data = data.sort_index(axis='index')
    # data = data.add(ser, axis='index')











    # ser = data.sum(axis=0).to_frame()
    # ser = ser.pivot_table(0, index=0, columns=[0,1,2,3,4,5,6])
    # print ser
    # print data
    # data[index: 'new_sum'] = data.sum(axis=0)
    # data = data.sort_index(['date_new'])
    # print data.info()
    # data = data.sort_index(axis='index', ascending=True, inplace=False, kind='quicksort', na_position='last')




    # print data.sum(axis=({index('data_new'[0]), columns('receipt_week_day')}))
    # data = pandas_select.groupby(['date_new', 'receipt_week_day'])['sum_total_price'].aggregate('mean').unstack()
    # print data
    # select_time = "cast(strftime('%H', receipt_date)/4*4 AS TEXT)|| ':'|| cast(strftime('%M', receipt_date)/ 60 * 60 AS TEXT)"
    # return render(request, 'select/index.html')
    # return render_to_response('select/index.html', args)
    # return HttpResponse(data.to_html())
    # return JsonResponse({'word': select})


def slq_first(request):
    pass
# def form_secelt(select, time):
#     time = ['30 * 30'=30min, '60 * 60' =1h, '10 * 10' = 10min ]

# Create your views here.
# def slq_first(request):

    # data = Receipt.objects.values('receipt_date').extra()
    # print ProductsReceipt.values('receipt__receipt_shop_id').annotate(Sum('receipt__productsreceipt__qty'))
    # suma = ProductsReceipt.objects.values('receipt__productsreceipt','receipt__receipt_shop_id', 'receipt__productsreceipt__product_id').annotate('receipt__productsreceipt' = )
    # shops = Shop.objects.all().values_list()
    # , suma=Sum('receipt__productsreceipt__product_id'))
    # suma = ProductsReceipt.objects.aggregate(Sum('qty'))
    # pubs = ProductsReceipt.objects.aggregate('receipt_id'=Receipt('id'), 'product_id'=Product('id'), suma=Sum('product__productsreceipt__qty')).group_by('receipt__receipt_week_day','product_id') #.annotate(receipt_id=Receipt('id')).group_by('receipt__receipt_week_day','product_id')
    # pubs = ProductsReceipt.objects.aggregate('receipt_id', 'product_id', suma=Sum('product__productsreceipt__qty')).group_by('receipt__receipt_week_day','product_id') #.annotate(receipt_id=Receipt('id')).group_by('receipt__receipt_week_day','product_id')
    # pubs = ProductsReceipt.objects.values('receipt_id','receipt__receipt_week_day').aggregate('receipt__receipt_week_day') #, 'product__product_name') #.annotate('receipt_id', 'product_id', suma=Sum('product__productsreceipt__qty')).group_by('receipt__receipt_week_day','product_id') #.annotate(receipt_id=Receipt('id')).group_by('receipt__receipt_week_day','product_id')
    # pubs = ProductsReceipt.objects.values('receipt_id').filter('week_day'=3)
    #.aggregate('receipt__receipt_week_day') #, 'product__product_name') #.annotate('receipt_id', 'product_id', suma=Sum('product__productsreceipt__qty')).group_by('receipt__receipt_week_day','product_id') #.annotate(receipt_id=Receipt('id')).group_by('receipt__receipt_week_day','product_id')
    # pubs = Receipt.objects.values('receipt_shop__shop_name', 'receipt_week_day').annotate(Sum('receipt_items_qty'))
    # data = Receipt.objects.values('receipt_date', 'productsreceipt__product__product_name').annotate(suma=Sum('receipt_shop__receipt__receipt_items_qty'))
    # print pubs
    # return HttpResponse('1')

def sel_second(request):
    # sel = Receipt.objects.all().select_related('receipt_shop').filter(receipt_shop_id=595).values('receipt_date', 'receipt_shop__shop_name')
    # product = ProductsReceipt.objects.all() #.select_related('product_id').annotate(suma=Sum('qty')) #.order_by('product_id')
    # for s in sel:
    #     print s['receipt_shop__shop_name'], s['receipt_date']
    # print sel
    # print product
    receipt = Receipt.objects.all().values('id')
    print receipt
    a = ProductsReceipt.objects.filter(receipt_id__in=receipt.values()).values('product_id', 'product__product_name', 'receipt_id')
    print a
    for b in a:
        print b['product_id'], b['product__product_name'], b['receipt_id']

    return HttpResponse('1')

# def three(request):
#     receipt = Receipt.objects.values('productsreceipt__product__product_name', 'receipt_shop__shop_name').annotate(qty=Sum('productsreceipt__qty'))
#     pad = pd.DataFrame.from_records(receipt)
#     qq = pad.groupby('receipt_shop__shop_name')['qty'].idxmin()
#     print pad.ix[qq]
#     return HttpResponse('1')

def four(request):
    receipt = Receipt.objects.values('productsreceipt__product__product_name', 'receipt_week_day').annotate(qty=Sum('productsreceipt__qty'))
    pad = pd.DataFrame.from_records(receipt)
    qq = pad.groupby('receipt_week_day')['qty'].idxmax()
    print pad.ix[qq]
    return HttpResponse('1')

# def five(request):
#     receipt_date = Receipt.objects.extra(select=({'date_new': "cast(strftime('%H', receipt_date) AS TEXT)|| ':'|| cast(strftime('%M', receipt_date) / 30 * 30 AS TEXT)"})) #.groupby('date_new')
#     receipt_total_price = receipt_date.values('date_new','receipt_week_day').annotate(suma_total_price=Sum('receipt_total_price'))
#     # receipt_items_qty = receipt_date.values('date_new').annotate(suma_items_qty=Sum('receipt_items_qty'))
#     # pandas_item_qty = pd.DataFrame.from_records(receipt_items_qty)
#     # print receipt_total_price
#     # data = {}
#     # for row in receipt_total_price:
#     #     data[row['date_new']] = [row['receipt_week_day'], row['suma_total_price']]
#     #     print data
#     pandas_total_price = pd.DataFrame.from_records(receipt_total_price)
#     a = pandas_total_price.groupby('date_new')['suma_total_price'].sum()
#     print a
#     # print pandas_total_price
#     # print pandas_total_price['date_new'].head()
#     # arr = pandas_total_price.replace({'\n': '<br>'}, regex=True)
#     # print arr
#         # print row #, row['receipt_week_day'], row['suma_total_price']
#     # html = """<div class="row"><div class="col-md-1">'{1}'</div><div class="col-md-1">'{2}'</div><div class="col-md-1">'{3}'</div><div class="col-md-1">'{4}'</div></div>"""\
#     #     .format(pandas_total_price['date_new'].head())
#     return HttpResponse(pandas_total_price.to_html())
#     # return render_to_response(pandas_total_price.to_html)

def five(request):
    receipt_date = Receipt.objects.extra(select=({'date_new': "cast(strftime('%H', receipt_date) AS TEXT)|| ':'|| cast(strftime('%M', receipt_date) / 30 * 30 AS TEXT)"}))

    receipt_total_price = receipt_date.values('date_new', 'receipt_week_day').annotate(sum_total_price=Sum('receipt_total_price'))
    receipt_items_qty = receipt_date.values('date_new', 'receipt_week_day').annotate(sum_items_qty=Sum('receipt_items_qty'))
    receipt_qty = receipt_date.values('date_new', 'receipt_week_day').annotate(sum_qty=Sum('productsreceipt__qty'))

    pandas_total_price = pd.DataFrame.from_records(receipt_total_price)
    print pandas_total_price.info()
    print pandas_total_price.groupby(['date_new', 'receipt_week_day'])['sum_total_price'].aggregate('mean').unstack()
    data = pandas_total_price.pivot_table('sum_total_price', index='date_new', columns='receipt_week_day')
    # print data
    # data = pandas_total_price.iloc[pandas_total_price['receipt_total_price']]
    # data = pandas_total_price.reindex(index=receipt_total_price['receipt_week_day'], columns=['date_new', 'sum_total_price'])
    # print data

    # pandas_item_qty = pd.DataFrame.from_records(receipt_items_qty)
    # pandas_qty = pd.DataFrame.from_records(receipt_qty)
    # loc = pandas_total_price['receipt_week_day'].reindex()
    # print loc
    # pandas_total_price.unstack()
    # uns = loc.unstack(level=-1)
    # print uns
    # f = pandas_total_price.unstack(level=-1)
    # print pandas_total_price
    # groupby('date_new')
    # pandas_total_price_sum_date = pandas_total_price.groupby('date_new')['sum_total_price'].sum()
    # pandas_items_qty_sum_date = pandas_item_qty.groupby('date_new')['sum_items_qty'].sum()
    # pandas_qty_sum_date = pandas_qty.groupby('date_new')['sum_qty'].sum()
    #
    # pandas_total_price_sum_day = pandas_total_price.groupby('receipt_week_day')['sum_total_price'].sum()
    # pandas_items_qty_sum_day = pandas_item_qty.groupby('receipt_week_day')['sum_items_qty'].sum()
    # pandas_qty_sum_date_day = pandas_qty.groupby('receipt_week_day')['sum_qty'].sum()

    # print pandas_total_price_sum_date
    # print pandas_total_price_sum_day
    # print pandas_total_price[(pandas_total_price.receipt_week_day == 0)]
    # result = pd.merge(a, pandas_total_price, on=['date_new', 'date_new'])
    # print result

    return render_to_response('index.html', {'data': data.to_html()})
    # return HttpResponse(data.to_html())



    # print pandas_total_price[['date_new', 'receipt_week_day', 'suma_total_price']][:48]
    # for row in pandas_total_price['suma_total_price'][:48]:
    #     print html = "'{1}'".format(row.to_html())
    # pandas_total_price
    # c = a.split('\n')
    # print c
    # receipt_data_first = Receipt.objects.values('receipt_date')[:1]
    # receipt_data_end = list(Receipt.objects.values('receipt_date'))[-1]
    # range_data = pd.date_range(receipt_data_first[0]['receipt_date'], receipt_data_end['receipt_date'], freq='30min')
    # range_data = range_data.map(lambda x: x.strftime('%Y-%m-%d-%h-%M'))
    # print range_data
    # print receipt

    # receipt_date = Receipt.objects.extra(select=({'date':"cast(DATE(receipt_date) || ' ' || strftime('%H', receipt_date) AS TEXT) || ':' || cast(strftime('%M', receipt_date) / 30 * 30 AS TEXT)"} ))


    # pad = pd.DataFrame.from_records(Receipt.objects.all())

    # print receipt_date
    # pad.groupby(receipt_date[0]['data_new'])

    # print receipt_date

    # receipt = Receipt.objects.values('id', 'receipt_date', 'receipt_total_price').filter(receipt_date=receipt_date.values('date'))
    # receipt = Receipt.objects.values('id', 'receipt_date', 'receipt_total_price').order_by(receipt_date.values('date'))

    # receipt = Receipt.objects.values('id', 'receipt_date', 'receipt_total_price').filter(receipt_date=receipt_date.values('date'))
    # print data.values('date')[0]['date']
    # print data
    # print receipt_date.values('date')
    # print receipt

    # for a in receipt_date.values('date'):
    #     print a['date']







def new(request):
    path = 'data.json'
    with open(path) as data_file:
        data = json.load(data_file)
        print 'open'
    shops = []
    products = []
    receipts = []
    productsreceipts = []

    for row in data:
        for prod in row['products']:
            productsreceipts.append((row['id'], prod['order_no'],  prod['qty'], prod['price'], prod['product_id']))
        shops.append((row['shop_id'], row['shop__name']))
        receipts.append((row['id'], row['date'], row['items_qty'], row['week_day'], row['total_price'], row['shop_id']))
        products.append((row['products'][0]['product_id'], row['products'][0]['product__name']))

    shops = set(shops)
    products = set(products)
    receipts = set(receipts)

    shops_db = [Shop(id=shop[0], shop_name=shop[1]) for shop in shops]
    products_db = [Product(id=product[0], product_name=product[1]) for product in products]
    receipts_db = [Receipt(id=receipt[0], receipt_date=receipt[1], receipt_items_qty=receipt[2], receipt_week_day=receipt[3], receipt_total_price=receipt[4],receipt_shop_id=receipt[5]) for receipt in receipts]
    products_receipt = [ProductsReceipt(receipt_id=products_r[0], order_no=products_r[1], qty=products_r[2], price=products_r[3], product_id=products_r[4]) for products_r in productsreceipts]
    Shop.objects.bulk_create(shops_db)
    Receipt.objects.bulk_create(receipts_db)
    Product.objects.bulk_create(products_db)
    ProductsReceipt.objects.bulk_create(products_receipt)

    return HttpResponse('hi')


# def readFile(request):
#     path = 'data.json'
#     with open(path) as data_file:
#         data = json.load(data_file)
#         print 'open'
#     shops = {}
#     receipts = {}

    # products =  [('product_id'=products[0], 'product_name' = products[1])]
    # shops = [('id'=shops[0],'shop_name'=shops[1])]
    # receipts = [('id'= receipts[0], 'receipt_date'=receipts[1], 'receipt_items_qty'=receipts[2], 'receipt_week_day'=receipts[3], 'receipt_total_price'=receipts[4],'receipt_shop_id'=receipts[5])]
    # product = {}
    # products =[] # id =
    # for row in data:
    #     for prod in row['products']:
    #         products.append((row['id'], order_no'], product_id'], qty'], price']))
    #     if row['shop_id'] not in shops.keys():
    #         # shops[Shop.id = row['shop_id']] = (row['shop_id'], row['shop__name'] )
    #         # Shop.objects.name = row['shop__name']
    #         shops[row['shop_id']] = (row['shop_id'], row['shop__name'])
    #     if row['id'] not in receipts.keys():
    #         receipts[row['id']] = (
    #             row['id'], row['date'], row['items_qty'], row['week_day'], row['total_price'], row['shop_id'])
    #     if row['products'][0]['product_id'] not in product.keys():
    #         product[row['products'][0]['product_id']] = (
    #             row['products'][0]['product_id'], row['products'][0]['product__name'])

    # print shops
    # print receipts
    # print product

    # Shop.objects.bulk_create(shops.values())
    # Receipt.objects.bulk_create(receipts.values())
    # Product.objects.bulk_create(product.values())
    # ProductsReceipt.objects.bulk_create(products)
    # print 'exit'
    # return HttpResponse('hi')


def index(request):
    return render_to_response('index.html')
