# Calculate body fat percentage and return the same
    :age: age of user ot patient
    :gender: Male or Female
    :BMI: Body mass index
    :return: percentage of body fat

# equation information

    Body fat percentage (BFP) formula for adult males:
    BFP = 1.20 × BMI + 0.23 × Age - 16.2

    Body fat percentage (BFP) formula for adult females:
    BFP = 1.20 × BMI + 0.23 × Age - 5.4

    Body fat percentage (BFP) formula for boys:
    BFP = 1.51 × BMI - 0.70 × Age - 2.2

    Body fat percentage (BFP) formula for girls:
    BFP = 1.51 × BMI - 0.70 × Age + 1.4
    
# Example code
   
    from BodyfatCalculator.bodyfat_calculator import body_fat
    
    
    percentage = (age=27,gender="Male",BMI=22.22)
    
    
    print(percentage)
    
    
    
    
    
    output: 16.673999999999996

