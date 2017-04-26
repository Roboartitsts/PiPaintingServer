import stepper

for k in range(3):
    p = stepper.Stepper(k+1)
    p.run(8,500,1)
