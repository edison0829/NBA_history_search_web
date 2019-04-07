import sys
input_file = sys.argv[1]
f = open(input_file, 'r')
out = open('new.csv','w')
for line in f.readlines():
    a = line.strip().split(",")
    b=a[1].split("\\")
    a[1]=b[0]
    x=','.join(a)+"\n"
    out.writelines(x)
f.close()
out.close()
        # items = line.strip().split(',')
        # for i in items[1]:
        #
        # print(','.join(items[:2]+items[3:]), file=writer)
