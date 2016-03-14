from flask import Flask, Blueprint, render_template, request
import pandas as pd
from data import inds, cocktails

cock_calc = Blueprint('cocktail_calculator', __name__,
                        template_folder='templates')
class VARS:
    def __init__(self):
        self.inds = inds
        self.cocktails = cocktails
        self.Num = 2
        self.spirit_abv = 40
        self.spirit_amount = 0
        self.amounts = [0, 0]
        self.ingredients = ['Carpano', 'Carpano']
    def update(self):
        self.spirit_abv = float(request.form.get('base_abv'))
        self.spirit_amount = float(request.form.get('a_base'))
        self.ingredients = [request.form.get('in'+ str(n)) for n in range(1, 1+G.Num)]
        self.amounts = [float(request.form.get('a'+ str(n))) for n in range(1, 1+G.Num)]

if 'G' not in vars():
    G = VARS()

@cock_calc.route('/Calculate', methods=['POST'])
def calc():
    if request.form['submit'] == 'Less':
        G.Num -=1
        G.update()
    elif request.form['submit'] == 'More':
        G.update()
        G.Num += 1
        G.amounts.append(0)
        G.ingredients.append('Carpano')
    else:
        G.update()
        total = sum(G.amounts)+float(G.spirit_amount)
        sugar = 0
        acid = 0
        abv = float(G.spirit_abv)*G.spirit_amount/total
        for i, a in zip(G.ingredients, G.amounts):
            i = i.replace('_', ' ')
            sugar+=G.inds.query('Ingredient == @i').Sweetness.values[0]*a/total
            acid+=G.inds.query('Ingredient == @i').Acid.values[0]*a/total
            abv+=G.inds.query('Ingredient == @i').Ethanol.values[0]*a/total
        dil = -1.21*((abv/100)**2) + 1.246*(abv/100) + 1.145
        total_fin = total*dil
        G.sugar = sugar/dil
        G.acid = acid/dil
        G.abv = abv/dil
    return render_template('cocktail_calculator.html', G=G)