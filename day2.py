# Rame_height = 1.3
# Raja_height = 1.7
# if Rame_height > Raja_height:
#     print("rame is taller")
# else:
#     print("raja is taller")
total = float(input("Enter tptal purchase amount: "))
if total >= 1000:
    discount = total * 0.10
    final_amount = total - discount
    print("discount applied:", discount)
    print("final amount:", final_amount)
else:
    print("No discount applied")
    print("total amount: total")
