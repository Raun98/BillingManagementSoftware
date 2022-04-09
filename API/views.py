from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os, csv
from datetime import datetime
from .forms import BillForm
import pandas as pd

# Create your views here.
def HomeView(request):
    #print(os.getcwd())
    return render(request, 'index.html')

@api_view(['GET'])
def show_bill(request):
    #df = pd.read_csv("temp_data.csv")
    #sorted_df = df.sort_values(by=["item"], ascending=False)
    with open('temp_data.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        total_bill_price = 0
        result = {}
        time = datetime.now()
        dayAndTime = time.strftime('%Y-%m-%d %H:%M:%S')
        result['dayAndTime'] = dayAndTime


        for row in reader:
            print(row)
            results_dict = {}
            price=int(row[3])
            quantity=int(row[2])
            results_dict['item name'] = row[0]
            total_price = quantity * price
            results_dict['total price'] = total_price
            if row[1] == "Medicine" or row[1] == "Food":
                tax = 0.05*total_price
                tax_rate = "5%"
            elif row[1] == "Clothes":
                if total_price < 1000:
                    tax = 0.05*total_price
                    tax_rate = "5%"
                elif total_price > 1200:
                    tax= 0.12*total_price
                    tax_rate = "12%"
            elif row[1] == "Music":
                tax = 0.03*total_price
                tax_rate = "3%"
            elif row[1] == "Imported":
                tax = 0.18*total_price
                tax_rate = "18%"
            total_bill_price += total_price+tax
            results_dict['tax'] = tax
            results_dict['tax rate'] = tax_rate
            result[row[0]] = results_dict
        result['totalAmountPayable'] = total_bill_price
        if total_bill_price > 2000:
            discount = total_bill_price - (0.05*total_bill_price)
        result['Price After Discount'] = discount
        print("Final Bill Price : ",total_bill_price)
    os.remove("temp_data.csv")
    return Response(result)

def calculate_bill(request):
    print(request.body)
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            print("form is valid")
            item = form.cleaned_data['item']
            itemCategory = form.cleaned_data['itemCategory']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            form = BillForm()
            if itemCategory == "option-1":
                itemCategory = "Medicine"
            elif itemCategory == "option-2":
                itemCategory = "Food"
            elif itemCategory == "option-3":
                itemCategory = "Book"
            elif itemCategory == "option-4":
                itemCategory = "Imported"
            elif itemCategory == "option-5":
                itemCategory = "Music"
            elif itemCategory == "option-6":
                itemCategory = "Clothes"


            print(item,itemCategory,price,quantity)
            itemlist = [item,itemCategory,price,quantity]

            with open('temp_data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(itemlist)
            return redirect('/')
        print("form is not valid")
    return render(request, 'index.html',)