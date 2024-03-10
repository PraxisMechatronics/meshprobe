import random
import csv

with open("test.csv", "wt") as f:
    writer = csv.writer(f)
    # company name, tech name, machine type, sn, x dim, y dim, mode
    test_info = ("company", "mike dillio", "vf2", "sn1104234", 12, 8, 0)
    writer.writerow(test_info)
    """for i in range(test_info[5]):
        row = []
        for x in range(test_info[4]):
            if x < 0:
                row.append("{:.4f}".format(random.randint(0, 20) * 0))
            else:
                row.append("{:.4f}".format(random.randint(-20, 20) * 0.0001))
        writer.writerow(row)"""
print(open("test.csv", "rt").read())
