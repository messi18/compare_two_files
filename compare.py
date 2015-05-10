import sys

field_names=['id','ccy1','ccy2','settle_date']
field_key_index=0
field_separator=','

def save_diffs(f,line_no,cmp_results):
  f.write(str(line_no)+';')
  f.write(';'.join(["%s(%s,%s)" % (n,l,r) for n,l,r in cmp_results]))
  f.write('\n')

def save_report(f,diff_cnt):
  f.write("-------------------\n")
  f.write("different count:%s" % diff_cnt)
  f.write("\n")

def compare_line(line1,line2):
  same,diff=[],[]
  if len(line1) == 0:
    items1=[]
  else:
    items1=line1.split(field_separator)

  if len(line2) == 0:
    items2=[]
  else:
    items2=line2.split(field_separator)

  if len(items1) != len(items2):
    return (False,[("field_count",len(items1),len(items2))])
  if items1[field_key_index] != items2[field_key_index]:
    return (False,[(field_names[field_key_index],items1[field_key_index],items2[field_key_index])])

  for i,(v1,v2) in enumerate(zip(items1,items2)):
    if v1 == v2:
      same.append((i,v1,v2))
    else:
      diff.append((field_names[i],v1,v2))
  if len(same) == len(items1):
    return (True,[])
  else:
    return (False,diff)


file1,file2,output=sys.argv[1],sys.argv[2],sys.argv[3]
with open(file1) as f1, open (file2) as f2, open(output,'w') as output_f:
  diff_cnt=0
  line_cnt=0
  while True:
    line1,line2=f1.readline(),f2.readline()
    line_cnt += 1

    if not line1 and not line2:
      print 'Reach EOF of two files'
      break
    elif not line1:
      print 'Read EOF of left file' 
    elif not line2:
      print 'Reach EOF of right file'

    match,cmp_results=compare_line(line1.rstrip(),line2.rstrip())
    if not match:
      diff_cnt += len(cmp_results)
      save_diffs(output_f,line_cnt,cmp_results)
  save_report(output_f,diff_cnt)
  print "\nComparation finished."
